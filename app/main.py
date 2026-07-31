from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.schemas import (
    AIEvaluationResponse,
    BatchEvaluationRequest,
    BatchEvaluationResponse,
    EvaluationCase,
    EvaluationResult,
)
from app.services.deepseek_client import (
    DEFAULT_MODEL,
    DeepSeekAPIError,
    DeepSeekClient,
)
from app.services.report_service import ReportService
from app.services.rubric_engine import RubricEngine

ROOT_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="EvalPilot：规则引擎 + DeepSeek 双层评测平台",
    description="先用透明规则评分，再用 DeepSeek 进行独立复核。",
    version="0.2.0",
)

engine = RubricEngine()
report_service = ReportService()


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(ROOT_DIR / "frontend" / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "EvalPilot"}


@app.get("/ai-status")
def ai_status() -> dict:
    return {
        "configured": bool(os.environ.get("DEEPSEEK_API_KEY", "").strip()),
        "provider": "DeepSeek",
        "model": os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL),
    }


@app.post("/evaluate", response_model=EvaluationResult)
def evaluate(case: EvaluationCase) -> EvaluationResult:
    return engine.evaluate(case)


@app.post("/ai-evaluate", response_model=AIEvaluationResponse)
def ai_evaluate(case: EvaluationCase) -> AIEvaluationResponse:
    rule_result = engine.evaluate(case)
    try:
        client = DeepSeekClient.from_environment()
        review = client.review(case, rule_result)
    except DeepSeekAPIError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return AIEvaluationResponse(
        case_id=case.case_id,
        provider="DeepSeek",
        model=client.model,
        rule_result=rule_result,
        ai_review=review,
    )


@app.post("/batch-evaluate", response_model=BatchEvaluationResponse)
def batch_evaluate(request: BatchEvaluationRequest) -> BatchEvaluationResponse:
    results = [engine.evaluate(case) for case in request.cases]
    report = report_service.build_report(results)
    return BatchEvaluationResponse(results=results, report=report)


@app.get("/demo-report")
def demo_report() -> dict:
    demo_cases = [
        EvaluationCase(
            case_id="prime_001",
            task="判断整数是否为质数",
            model_output="质数是大于 1 且只能被 1 和自身整除。n <= 1 返回 false，n == 2 返回 true，并检查到 sqrt(n)。",
            required_keywords=["大于 1", "sqrt", "false", "true"],
            fail_patterns=["1 是质数", "只判断奇偶"],
        ),
        EvaluationCase(
            case_id="prime_002",
            task="判断整数是否为质数",
            model_output="奇数就是质数，1 是质数。",
            required_keywords=["大于 1", "sqrt", "false", "true"],
            fail_patterns=["1 是质数", "奇数就是质数"],
        ),
    ]
    results = [engine.evaluate(case) for case in demo_cases]
    return {"results": results, "report": report_service.build_report(results)}

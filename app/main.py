from __future__ import annotations

from fastapi import FastAPI

from app.schemas import BatchEvaluationRequest, BatchEvaluationResponse, EvaluationCase, EvaluationResult
from app.services.report_service import ReportService
from app.services.rubric_engine import RubricEngine

app = FastAPI(
    title="EvalPilot LLM Evaluation Platform",
    description="A lightweight platform for rubric-based LLM answer evaluation.",
    version="0.1.0",
)

engine = RubricEngine()
report_service = ReportService()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "EvalPilot"}


@app.post("/evaluate", response_model=EvaluationResult)
def evaluate(case: EvaluationCase) -> EvaluationResult:
    return engine.evaluate(case)


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

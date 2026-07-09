"""Simple rubric evaluator demo.

This script is not a replacement for human review or real LLM evaluation.
It demonstrates how to turn rubric dimensions into a structured output that is easy to audit.

Usage:
    python tools/evaluate_submission.py examples/evaluation_cases.jsonl
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class EvaluationResult:
    case_id: str
    score: int
    level: str
    error_types: list[str]
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "score": self.score,
            "level": self.level,
            "error_types": self.error_types,
            "suggestion": self.suggestion,
        }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))
    return cases


def evaluate_case(case: dict[str, Any]) -> EvaluationResult:
    output = str(case.get("model_output", ""))
    required_keywords = case.get("required_keywords", [])
    fail_patterns = case.get("fail_patterns", [])

    score = 10
    error_types: list[str] = []

    missing_keywords = [keyword for keyword in required_keywords if keyword not in output]
    triggered_fail_patterns = [pattern for pattern in fail_patterns if pattern in output]

    if missing_keywords:
        score -= min(4, len(missing_keywords) * 2)
        error_types.append("incomplete_answer")

    if triggered_fail_patterns:
        score -= min(6, len(triggered_fail_patterns) * 3)
        error_types.append("logic_error")

    if "sqrt" not in output and "平方根" not in output and "根号" not in output:
        score -= 1
        if "missing_edge_case" not in error_types:
            error_types.append("missing_edge_case")

    score = max(score, 0)

    if score >= 8:
        level = "pass"
        suggestion = "答案覆盖了核心逻辑、边界条件和复杂度说明。"
    elif score >= 5:
        level = "partial"
        suggestion = "答案部分正确，但还需要补充关键边界条件、优化思路或更明确的输出格式。"
    else:
        level = "fail"
        suggestion = "答案存在明显逻辑错误，建议重新检查质数定义、边界条件和判定流程。"

    return EvaluationResult(
        case_id=str(case.get("case_id", "unknown")),
        score=score,
        level=level,
        error_types=sorted(set(error_types)),
        suggestion=suggestion,
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/evaluate_submission.py examples/evaluation_cases.jsonl")

    path = Path(sys.argv[1])
    cases = load_jsonl(path)

    for case in cases:
        result = evaluate_case(case)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

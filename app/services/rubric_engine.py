from __future__ import annotations

from app.schemas import EvaluationCase, EvaluationResult


class RubricEngine:
    """Rule-based LLM evaluation engine.

    The engine is intentionally transparent: every deduction has an evidence item.
    This matches real LLM evaluation work where score consistency and auditability
    are more important than simply returning a number.
    """

    def evaluate(self, case: EvaluationCase) -> EvaluationResult:
        score = 10
        evidence: list[str] = []
        error_types: set[str] = set()

        output = case.model_output.strip()
        if not output:
            return EvaluationResult(
                case_id=case.case_id,
                score=0,
                level="fail",
                error_types=["empty_answer"],
                evidence=["模型回答为空，无法评测。"],
                suggestion="需要补充完整回答，并覆盖题目要求。",
            )

        missing_keywords = [kw for kw in case.required_keywords if kw not in output]
        matched_keywords = [kw for kw in case.required_keywords if kw in output]
        triggered_patterns = [pattern for pattern in case.fail_patterns if pattern in output]

        for kw in matched_keywords:
            evidence.append(f"覆盖关键点：{kw}")

        if missing_keywords:
            deduction = min(4, len(missing_keywords) * 2)
            score -= deduction
            error_types.add("incomplete_answer")
            evidence.append(f"缺失关键点：{', '.join(missing_keywords)}，扣 {deduction} 分。")

        if triggered_patterns:
            deduction = min(6, len(triggered_patterns) * 3)
            score -= deduction
            error_types.add("logic_error")
            evidence.append(f"命中错误模式：{', '.join(triggered_patterns)}，扣 {deduction} 分。")

        if self._looks_unstructured(output):
            score -= 1
            error_types.add("format_error")
            evidence.append("回答结构较弱，缺少清晰步骤或结论，扣 1 分。")

        if self._missing_edge_case_signal(output):
            score -= 1
            error_types.add("missing_edge_case")
            evidence.append("未明显体现边界条件意识，扣 1 分。")

        score = max(0, min(score, 10))
        level = self._score_to_level(score)

        return EvaluationResult(
            case_id=case.case_id,
            score=score,
            level=level,
            error_types=sorted(error_types),
            evidence=evidence or ["未发现明显问题，但建议人工复核。"],
            suggestion=self._suggestion(level, error_types),
        )

    @staticmethod
    def _score_to_level(score: int) -> str:
        if score >= 8:
            return "pass"
        if score >= 5:
            return "partial"
        return "fail"

    @staticmethod
    def _looks_unstructured(output: str) -> bool:
        separators = ["\n", "1.", "2.", "-", "：", ":"]
        return len(output) > 120 and not any(token in output for token in separators)

    @staticmethod
    def _missing_edge_case_signal(output: str) -> bool:
        edge_case_words = ["边界", "特殊", "n <=", "小于", "等于", "空", "异常", "edge"]
        return not any(word in output for word in edge_case_words)

    @staticmethod
    def _suggestion(level: str, error_types: set[str]) -> str:
        if level == "pass":
            return "答案整体可用，建议保留人工抽检以确认边界情况。"
        if "logic_error" in error_types:
            return "优先修正核心逻辑错误，再补充边界条件和输出格式。"
        if "incomplete_answer" in error_types:
            return "补充缺失关键点，并用 Gold Answer 对照检查覆盖率。"
        return "建议增强解释结构，补充证据、边界条件和最终结论。"

from __future__ import annotations

from collections import Counter

from app.schemas import EvaluationResult


class ReportService:
    """Aggregate evaluation results into a report for reviewers."""

    def build_report(self, results: list[EvaluationResult]) -> dict:
        if not results:
            return {
                "total": 0,
                "average_score": 0,
                "pass_rate": 0,
                "level_distribution": {},
                "error_distribution": {},
                "low_score_cases": [],
            }

        total = len(results)
        average_score = round(sum(item.score for item in results) / total, 2)
        pass_count = sum(1 for item in results if item.level == "pass")
        level_distribution = Counter(item.level for item in results)
        error_distribution = Counter(error for item in results for error in item.error_types)
        low_score_cases = [
            {
                "case_id": item.case_id,
                "score": item.score,
                "level": item.level,
                "error_types": item.error_types,
            }
            for item in results
            if item.score < 6
        ]

        return {
            "total": total,
            "average_score": average_score,
            "pass_rate": round(pass_count / total, 2),
            "level_distribution": dict(level_distribution),
            "error_distribution": dict(error_distribution),
            "low_score_cases": low_score_cases,
        }

from app.schemas import AIReview
from app.services.deepseek_client import DeepSeekClient


def test_strips_json_code_fence():
    content = '```json\n{"score": 8}\n```'
    assert DeepSeekClient._strip_code_fence(content) == '{"score": 8}'


def test_ai_review_schema_accepts_expected_result():
    review = AIReview.model_validate(
        {
            "score": 8,
            "level": "pass",
            "error_types": [],
            "evidence": ["覆盖核心关键点"],
            "suggestion": "补充边界条件。",
            "review_summary": "整体正确。",
        }
    )
    assert review.score == 8

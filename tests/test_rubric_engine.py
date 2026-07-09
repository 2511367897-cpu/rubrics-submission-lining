from app.schemas import EvaluationCase
from app.services.rubric_engine import RubricEngine


def test_pass_case_scores_high():
    engine = RubricEngine()
    case = EvaluationCase(
        case_id="prime_001",
        task="判断整数是否为质数",
        model_output="质数是大于 1 且只能被 1 和自身整除。n <= 1 返回 false，并检查到 sqrt(n)。最终输出 true 或 false。",
        required_keywords=["大于 1", "sqrt", "false", "true"],
        fail_patterns=["1 是质数", "奇数就是质数"],
    )
    result = engine.evaluate(case)
    assert result.level == "pass"
    assert result.score >= 8


def test_logic_error_scores_low():
    engine = RubricEngine()
    case = EvaluationCase(
        case_id="prime_002",
        task="判断整数是否为质数",
        model_output="奇数就是质数，1 是质数。",
        required_keywords=["大于 1", "sqrt", "false", "true"],
        fail_patterns=["1 是质数", "奇数就是质数"],
    )
    result = engine.evaluate(case)
    assert result.level == "fail"
    assert "logic_error" in result.error_types

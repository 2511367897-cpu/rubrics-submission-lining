from __future__ import annotations

import json
import os
import ssl
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.schemas import AIReview, EvaluationCase, EvaluationResult


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"


class DeepSeekAPIError(RuntimeError):
    """A user-safe DeepSeek API error that never includes the API key."""


@dataclass(frozen=True)
class DeepSeekClient:
    api_key: str
    model: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL
    timeout: int = 60

    @classmethod
    def from_environment(cls) -> "DeepSeekClient":
        api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            raise DeepSeekAPIError(
                "未找到 DEEPSEEK_API_KEY。请通过 start_macos.command 启动项目。"
            )
        return cls(
            api_key=api_key,
            model=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
            base_url=os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        )

    def review(self, case: EvaluationCase, rule_result: EvaluationResult) -> AIReview:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是一名严格、可复核的大模型回答评测员。"
                        "请结合题目、必需关键点、禁止错误模式和规则引擎结果进行独立复核。"
                        "只输出合法 JSON，不要输出 Markdown。"
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_prompt(case, rule_result),
                },
            ],
            "response_format": {"type": "json_object"},
            "thinking": {"type": "disabled"},
            "max_tokens": 1200,
            "stream": False,
        }
        data = self._post_json("/chat/completions", payload)
        try:
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(self._strip_code_fence(content))
            return AIReview.model_validate(parsed)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            raise DeepSeekAPIError("DeepSeek 返回内容无法解析为评测结果。") from exc

    def _post_json(self, path: str, payload: dict) -> dict:
        request = Request(
            self.base_url + path,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(
                request,
                timeout=self.timeout,
                context=self._ssl_context(),
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = self._safe_http_error(exc)
            raise DeepSeekAPIError(f"DeepSeek API 请求失败（HTTP {exc.code}）：{detail}") from exc
        except URLError as exc:
            raise DeepSeekAPIError("无法连接 DeepSeek API，请检查网络后重试。") from exc
        except TimeoutError as exc:
            raise DeepSeekAPIError("DeepSeek API 响应超时，请稍后重试。") from exc

    @staticmethod
    def _safe_http_error(exc: HTTPError) -> str:
        try:
            data = json.loads(exc.read().decode("utf-8"))
            return str(data.get("error", {}).get("message", "未知错误"))[:300]
        except Exception:
            return "未知错误"

    @staticmethod
    def _ssl_context() -> ssl.SSLContext:
        system_bundle = Path("/etc/ssl/cert.pem")
        if system_bundle.exists():
            return ssl.create_default_context(cafile=str(system_bundle))
        return ssl.create_default_context()

    @staticmethod
    def _strip_code_fence(content: str) -> str:
        text = content.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text.strip()

    @staticmethod
    def _build_prompt(case: EvaluationCase, rule_result: EvaluationResult) -> str:
        return (
            "请用 JSON 复核下面的模型回答。\n\n"
            f"题目：{case.task}\n"
            f"模型回答：{case.model_output}\n"
            f"必需关键点：{json.dumps(case.required_keywords, ensure_ascii=False)}\n"
            f"禁止错误模式：{json.dumps(case.fail_patterns, ensure_ascii=False)}\n"
            f"规则引擎结果：{json.dumps(rule_result.model_dump(), ensure_ascii=False)}\n\n"
            "JSON 必须严格包含：\n"
            "{\n"
            '  "score": 0到10的整数,\n'
            '  "level": "pass、partial 或 fail",\n'
            '  "error_types": ["错误类型"],\n'
            '  "evidence": ["直接来自回答的证据"],\n'
            '  "suggestion": "具体修改建议",\n'
            '  "review_summary": "一句话复核结论"\n'
            "}\n"
            "不要因为规则引擎给了分就机械照抄；如果不同意，应在证据中说明。"
        )

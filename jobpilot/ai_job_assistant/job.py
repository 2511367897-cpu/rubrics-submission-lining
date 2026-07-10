from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


SKILL_KEYWORDS = {
    "python": ["python"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "html": ["html"],
    "css": ["css"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "api": ["api", "apis"],
    "rest": ["rest", "restful"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "json": ["json"],
    "markdown": ["markdown"],
    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],
    "linux": ["linux"],
    "pytest": ["pytest"],
    "jinja2": ["jinja2", "jinja"],
    "llm": ["llm", "large language model", "large language models", "大语言模型", "大模型"],
    "prompt engineering": ["prompt engineering", "prompt", "提示词工程", "提示词"],
    "llm evaluation": ["llm evaluation", "model evaluation", "模型评测", "大模型评测", "evaluation"],
    "rubric": ["rubric", "rubrics", "scoring rules", "评分标准", "评分规则"],
    "rag": ["rag", "retrieval augmented generation", "检索增强生成"],
    "agent": ["agent", "agents", "智能体"],
    "machine learning": ["machine learning", "机器学习"],
    "deep learning": ["deep learning", "深度学习"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "vue": ["vue", "vue3"],
    "react": ["react", "reactjs"],
    "spring boot": ["spring boot", "springboot"],
}  # type: Dict[str, List[str]]


@dataclass
class Job:
    title: str
    company: Optional[str]
    description: str
    requirements: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)


def _alias_present(text: str, alias: str) -> bool:
    """Match English aliases as complete tokens and Chinese aliases as phrases."""
    if re.search(r"[\u4e00-\u9fff]", alias):
        return alias.lower() in text.lower()
    pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def _extract_known_skills(text: str) -> List[str]:
    found = []  # type: List[str]
    for canonical, aliases in SKILL_KEYWORDS.items():
        if any(_alias_present(text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(set(found))


def parse_job_description(text: str) -> Job:
    """Parse a plain-text Chinese or English job description."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Job description is empty")

    normalised = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in normalised.split("\n") if line.strip()]
    title = lines[0]
    company = None  # type: Optional[str]
    if len(lines) > 1 and not lines[1].startswith(("-", "*", "•")):
        company = lines[1]
        body_lines = lines[2:]
    else:
        body_lines = lines[1:]

    bullet_pattern = re.compile(r"^[\-*•]\s*")
    requirements = []  # type: List[str]
    description_parts = []  # type: List[str]

    for line in body_lines:
        if bullet_pattern.match(line):
            requirements.append(bullet_pattern.sub("", line))
        else:
            description_parts.append(line)

    return Job(
        title=title,
        company=company,
        description="\n".join(description_parts),
        requirements=requirements,
        skills=_extract_known_skills(text),
    )

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

SKILL_KEYWORDS = {
    "python": [r"\bpython\b"],
    "javascript": [r"\bjavascript\b", r"\bjs\b"],
    "html": [r"\bhtml5?\b"],
    "css": [r"\bcss3?\b"],
    "fastapi": [r"\bfastapi\b"],
    "flask": [r"\bflask\b"],
    "api": [r"\bapi(?:s)?\b"],
    "rest": [r"\brest(?:ful)?\b"],
    "json": [r"\bjson\b"],
    "markdown": [r"\bmarkdown\b"],
    "git": [r"\bgit\b"],
    "github": [r"\bgithub\b"],
    "jinja2": [r"\bjinja2?\b"],
    "llm": [r"\bllm(?:s)?\b", r"large language model(?:s)?"],
    "prompt engineering": [r"prompt engineering", r"\bprompt(?:s)?\b"],
    "llm evaluation": [r"llm evaluation", r"model evaluation", r"\bevaluation\b"],
    "rubric": [r"\brubric(?:s)?\b", r"scoring rules?"],
    "rag": [r"\brag\b", r"retrieval[- ]augmented generation"],
    "agent": [r"\bagent(?:s)?\b"],
    "vue": [r"\bvue(?:3)?\b"],
    "spring boot": [r"spring[ -]?boot"],
    "mysql": [r"\bmysql\b"],
}  # type: Dict[str, List[str]]


@dataclass
class Job:
    title: str
    company: Optional[str]
    description: str
    requirements: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)


def _extract_known_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for canonical, patterns in SKILL_KEYWORDS.items():
        if any(re.search(pattern, text_lower, flags=re.IGNORECASE) for pattern in patterns):
            found.append(canonical)
    return sorted(set(found))


def parse_job_description(text: str) -> Job:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Job description is empty.")
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n") if line.strip()]
    title = lines[0]
    company = None
    body_lines = lines[1:]
    if len(lines) > 1 and len(lines[1]) <= 80 and not lines[1].startswith(("-", "*", "•")):
        company = lines[1]
        body_lines = lines[2:]

    bullet_pattern = re.compile(r"^[\-*•]\s*")
    requirements = []  # type: List[str]
    description_parts = []  # type: List[str]
    for line in body_lines:
        if bullet_pattern.match(line):
            requirements.append(bullet_pattern.sub("", line).strip())
        else:
            description_parts.append(line)

    return Job(
        title=title,
        company=company,
        description="\n".join(description_parts),
        requirements=requirements,
        skills=_extract_known_skills(text),
    )

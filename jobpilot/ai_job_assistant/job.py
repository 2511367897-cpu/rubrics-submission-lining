from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


SKILL_KEYWORDS = {
    "python": ["python"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "api": ["api", "apis"],
    "rest": ["rest", "restful"],
    "json": ["json"],
    "markdown": ["markdown"],
    "git": ["git"],
    "github": ["github"],
    "jinja2": ["jinja2", "jinja"],
    "llm": ["llm", "large language model", "large language models"],
    "prompt engineering": ["prompt engineering", "prompt"],
    "llm evaluation": ["llm evaluation", "model evaluation", "evaluate", "evaluation"],
    "rubric": ["rubric", "rubrics", "scoring rules"],
    "rag": ["rag", "retrieval augmented generation"],
    "agent": ["agent", "agents"],
    "vue": ["vue", "vue3"],
    "spring boot": ["spring boot", "springboot"],
    "mysql": ["mysql"],
}  # type: Dict[str, List[str]]


@dataclass
class Job:
    title: str
    company: Optional[str]
    description: str
    requirements: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)


def _alias_present(text: str, alias: str) -> bool:
    """Match aliases as complete tokens or phrases, not arbitrary substrings.

    This avoids false positives such as matching the skill ``rest`` inside the
    word ``interested``.
    """
    pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def _extract_known_skills(text: str) -> List[str]:
    found = []  # type: List[str]
    for canonical, aliases in SKILL_KEYWORDS.items():
        if any(_alias_present(text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(set(found))


def parse_job_description(text: str) -> Job:
    """Parse a plain-text job description into structured data."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise ValueError("Job description is empty")

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

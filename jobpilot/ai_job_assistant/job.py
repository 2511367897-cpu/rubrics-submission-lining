from __future__ import annotations

import re
from dataclasses import dataclass, field


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
}


@dataclass
class Job:
    title: str
    company: str | None
    description: str
    requirements: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


def _extract_known_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for canonical, aliases in SKILL_KEYWORDS.items():
        if any(alias in text_lower for alias in aliases):
            found.append(canonical)
    return sorted(set(found))


def parse_job_description(text: str) -> Job:
    """Parse a plain text job description into structured data.

    The parser is intentionally conservative: it extracts a curated set of
    technical and AI-related keywords instead of treating every English word as
    a skill. This keeps the fit report readable for resume use.
    """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise ValueError("Empty job description")

    title = lines[0]
    company = None
    if len(lines) > 1 and re.match(r"^[A-Za-z][A-Za-z0-9 &.,'-]+$", lines[1]):
        company = lines[1]
        body_lines = lines[2:]
    else:
        body_lines = lines[1:]

    bullet_pattern = re.compile(r"^[\-*•]\s*")
    requirements: list[str] = []
    description_parts: list[str] = []

    for line in body_lines:
        if bullet_pattern.match(line):
            requirements.append(bullet_pattern.sub("", line))
        else:
            description_parts.append(line)

    skills = _extract_known_skills(text)

    return Job(
        title=title,
        company=company,
        description="\n".join(description_parts),
        requirements=requirements,
        skills=skills,
    )

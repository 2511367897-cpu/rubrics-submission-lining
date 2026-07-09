from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Job:
    title: str
    company: str | None
    description: str
    requirements: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


def parse_job_description(text: str) -> Job:
    """Parse a plain text job description into structured data."""
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

    words = re.findall(r"[A-Za-z]+", text.lower())
    skills = sorted(set(words))

    return Job(
        title=title,
        company=company,
        description="\n".join(description_parts),
        requirements=requirements,
        skills=skills,
    )

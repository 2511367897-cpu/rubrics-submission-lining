from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

from .evaluator import evaluate_fit
from .job import Job
from .profile import Profile

PathLike = Union[str, Path]


def _write_text(output_path: PathLike, content: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content.rstrip() + "\n", encoding="utf-8")


def _try_jinja_render(template_path: PathLike, context: Dict[str, Any]) -> Optional[str]:
    template = Path(template_path)
    if not template.exists():
        return None
    try:
        from jinja2 import Environment, FileSystemLoader
    except ModuleNotFoundError:
        return None
    environment = Environment(loader=FileSystemLoader(str(template.parent)), autoescape=False)
    return environment.get_template(template.name).render(**context)


def _built_in_cv(profile: Profile, job: Optional[Job]) -> str:
    lines = [
        "# " + profile.name,
        "",
        "**Email:** " + profile.email + "  ",
        "**Phone:** " + profile.phone,
        "",
        "## Summary",
        "",
        profile.summary,
    ]
    if job is not None:
        fit = evaluate_fit(profile, job)
        lines.extend([
            "",
            "## Target Role Match: " + job.title,
            "",
            "**Fit score:** " + str(fit["score"]) + "%",
            "",
            "**Matched skills:** " + (", ".join(fit["matched_skills"]) or "None"),
            "",
            "**Skills to improve:** " + (", ".join(fit["missing_skills"]) or "None"),
        ])
    lines.extend(["", "## Skills", ""])
    lines.extend("- " + skill for skill in profile.skills)
    lines.extend(["", "## Experience", ""])
    if not profile.experience:
        lines.append("- No experience added yet.")
    for item in profile.experience:
        end_year = str(item.end_year) if item.end_year is not None else "Present"
        lines.extend([
            "### {0}｜{1}（{2} - {3}）".format(item.role, item.company, item.start_year or "", end_year),
            "",
            item.description,
            "",
        ])
    lines.extend(["## Education", ""])
    if not profile.education:
        lines.append("- No education added yet.")
    for item in profile.education:
        end_year = str(item.end_year) if item.end_year is not None else "Present"
        lines.append(
            "- **{0}**｜{1}｜{2}（{3} - {4}）".format(
                item.institution, item.degree, item.field, item.start_year or "", end_year
            )
        )
    return "\n".join(lines)


def _built_in_cover_letter(profile: Profile, job: Job) -> str:
    fit = evaluate_fit(profile, job)
    company = job.company or "your company"
    matched = ", ".join(fit["matched_skills"]) or "relevant transferable skills"
    missing = ", ".join(fit["missing_skills"][:5]) or "no major gaps identified"
    return "\n".join([
        profile.name,
        profile.email + " | " + profile.phone,
        "",
        "Dear Hiring Manager,",
        "",
        "I am writing to express my interest in the **{0}** position at **{1}**.".format(job.title, company),
        "",
        profile.summary,
        "",
        "JobPilot estimates a fit score of **{0}%**. My most relevant skills are: {1}.".format(fit["score"], matched),
        "",
        "To strengthen my fit further, I am continuing to improve: {0}.".format(missing),
        "",
        "Thank you for your time and consideration.",
        "",
        "Sincerely,",
        "",
        profile.name,
    ])


def render_cv(profile: Profile, job: Optional[Job], template_path: PathLike, output_path: PathLike) -> None:
    fit = evaluate_fit(profile, job) if job is not None else None
    rendered = _try_jinja_render(template_path, {"profile": profile, "job": job, "fit": fit})
    _write_text(output_path, rendered if rendered is not None else _built_in_cv(profile, job))


def render_cover_letter(profile: Profile, job: Job, template_path: PathLike, output_path: PathLike) -> None:
    fit = evaluate_fit(profile, job)
    rendered = _try_jinja_render(template_path, {"profile": profile, "job": job, "fit": fit})
    _write_text(output_path, rendered if rendered is not None else _built_in_cover_letter(profile, job))

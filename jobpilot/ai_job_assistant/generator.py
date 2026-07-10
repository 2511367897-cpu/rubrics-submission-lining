from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from jinja2 import Environment, FileSystemLoader

from .evaluator import evaluate_fit
from .job import Job
from .profile import Profile

PathLike = Union[str, Path]


def _environment(template_dir: PathLike) -> Environment:
    return Environment(loader=FileSystemLoader(str(template_dir)), autoescape=False)


def render_cv(profile: Profile, job: Optional[Job], template_path: PathLike, output_path: PathLike) -> None:
    template_path = Path(template_path)
    env = _environment(template_path.parent)
    template = env.get_template(template_path.name)
    fit = evaluate_fit(profile, job) if job else None
    rendered = template.render(profile=profile, job=job, fit=fit)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")


def render_cover_letter(profile: Profile, job: Job, template_path: PathLike, output_path: PathLike) -> None:
    template_path = Path(template_path)
    env = _environment(template_path.parent)
    template = env.get_template(template_path.name)
    fit = evaluate_fit(profile, job)
    rendered = template.render(profile=profile, job=job, fit=fit)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

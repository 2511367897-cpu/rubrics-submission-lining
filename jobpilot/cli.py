#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import load_profile


def default_profile_data() -> Dict[str, Any]:
    return {
        "name": "Li Ning",
        "email": "2511367897@qq.com",
        "phone": "13163586952",
        "summary": "Artificial intelligence undergraduate focused on Prompt Engineering, LLM evaluation, Python tooling and AI-assisted productivity workflows.",
        "skills": ["python", "llm", "prompt engineering", "llm evaluation", "rubric", "json", "markdown", "git"],
        "experience": [{
            "company": "TalentsAI",
            "role": "Prompt / Rubric Evaluation Specialist",
            "description": "Built and reviewed coding tasks, designed scoring rubrics, checked model outputs and improved evaluation consistency.",
            "start_year": 2025,
            "end_year": None,
        }],
        "education": [{
            "institution": "Henan Institute of Technology",
            "degree": "Bachelor",
            "field": "Artificial Intelligence",
            "start_year": 2024,
            "end_year": 2028,
        }],
    }


def _read_text_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError("File not found: {0}".format(file_path))
    return file_path.read_text(encoding="utf-8")


def init_profile(args: argparse.Namespace) -> None:
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise FileExistsError("Profile already exists: {0}. Use --force to overwrite.".format(output))
    output.write_text(json.dumps(default_profile_data(), indent=2, ensure_ascii=False), encoding="utf-8")
    print("Created profile skeleton: {0}".format(output))


def evaluate_job(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job))
    report = evaluate_fit(profile, job)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("Saved fit report: {0}".format(output))
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))


def generate_cv(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job)) if args.job else None
    render_cv(profile, job, args.cv_template, args.output)
    print("Generated CV: {0}".format(args.output))


def generate_cover_letter(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job))
    render_cover_letter(profile, job, args.letter_template, args.output)
    print("Generated cover letter: {0}".format(args.output))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JobPilot AI Career Copilot")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("init-profile", help="Create a profile JSON template")
    p.add_argument("--output", required=True)
    p.add_argument("--force", action="store_true", help="Overwrite an existing profile file")
    p.set_defaults(func=init_profile)

    p = sub.add_parser("evaluate-job", help="Evaluate job fit")
    p.add_argument("--profile", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--output")
    p.set_defaults(func=evaluate_job)

    p = sub.add_parser("generate-cv", help="Generate a tailored CV")
    p.add_argument("--profile", required=True)
    p.add_argument("--job")
    p.add_argument("--cv-template", default="templates/cv_template.md")
    p.add_argument("--output", required=True)
    p.set_defaults(func=generate_cv)

    p = sub.add_parser("generate-cover-letter", help="Generate a cover letter")
    p.add_argument("--profile", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--letter-template", default="templates/cover_letter_template.md")
    p.add_argument("--output", required=True)
    p.set_defaults(func=generate_cover_letter)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    try:
        args.func(args)
        return 0
    except (FileNotFoundError, FileExistsError, ValueError, OSError) as exc:
        print("ERROR: {0}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import load_profile


def _fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def _read_text_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        _fail(f"File not found: {file_path}. Please check the path and current directory.")
    return file_path.read_text(encoding="utf-8")


def init_profile(args: argparse.Namespace) -> None:
    skeleton = {
        "name": "Li Ning",
        "email": "2511367897@qq.com",
        "phone": "13163586952",
        "summary": "Artificial intelligence undergraduate focused on Prompt Engineering, LLM evaluation, Python tooling and AI-assisted productivity workflows.",
        "skills": [
            "python",
            "javascript",
            "llm",
            "prompt engineering",
            "llm evaluation",
            "rubric",
            "json",
            "markdown",
            "git",
        ],
        "experience": [
            {
                "company": "TalentsAI",
                "role": "Prompt / Rubric Evaluation Specialist",
                "description": "Built and reviewed coding tasks, designed scoring rubrics, checked model outputs and improved evaluation consistency.",
                "start_year": 2025,
                "end_year": None,
            }
        ],
        "education": [
            {
                "institution": "Henan Institute of Technology",
                "degree": "Bachelor",
                "field": "Artificial Intelligence",
                "start_year": 2024,
                "end_year": 2028,
            }
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(skeleton, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created profile skeleton: {output}")


def evaluate_job(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job))
    report = evaluate_fit(profile, job)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved fit report: {output}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))


def generate_cv(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job)) if args.job else None
    render_cv(profile, job, args.cv_template, args.output)
    print(f"Generated CV: {args.output}")


def generate_cover_letter(args: argparse.Namespace) -> None:
    profile = load_profile(args.profile)
    job = parse_job_description(_read_text_file(args.job))
    render_cover_letter(profile, job, args.letter_template, args.output)
    print(f"Generated cover letter: {args.output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="JobPilot AI Career Copilot")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init-profile", help="Create a profile JSON template")
    p.add_argument("--output", required=True)
    p.set_defaults(func=init_profile)

    p = sub.add_parser("evaluate-job", help="Evaluate job fit")
    p.add_argument("--profile", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--output")
    p.set_defaults(func=evaluate_job)

    p = sub.add_parser("generate-cv", help="Generate a tailored CV")
    p.add_argument("--profile", required=True)
    p.add_argument("--job")
    p.add_argument("--cv-template", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=generate_cv)

    p = sub.add_parser("generate-cover-letter", help="Generate a tailored cover letter")
    p.add_argument("--profile", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--letter-template", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=generate_cover_letter)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

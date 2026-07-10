#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import Profile
from cli import default_profile_data

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PROFILE_PATH = OUTPUT_DIR / "demo_profile.json"
REPORT_PATH = OUTPUT_DIR / "report.json"
CV_PATH = OUTPUT_DIR / "cv.md"
LETTER_PATH = OUTPUT_DIR / "letter.md"
JOB_PATH = BASE_DIR / "sample_data" / "sample_job.md"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    profile_data = default_profile_data()
    PROFILE_PATH.write_text(json.dumps(profile_data, indent=2, ensure_ascii=False), encoding="utf-8")
    profile = Profile.from_dict(profile_data)
    job = parse_job_description(JOB_PATH.read_text(encoding="utf-8"))
    report = evaluate_fit(profile, job)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    render_cv(profile, job, BASE_DIR / "templates" / "cv_template.md", CV_PATH)
    render_cover_letter(profile, job, BASE_DIR / "templates" / "cover_letter_template.md", LETTER_PATH)

    required_files = [PROFILE_PATH, REPORT_PATH, CV_PATH, LETTER_PATH]
    missing = [str(path) for path in required_files if not path.exists() or path.stat().st_size == 0]
    if missing:
        raise RuntimeError("Quickstart did not create valid files: " + ", ".join(missing))

    print("SUCCESS: JobPilot completed without errors.")
    for path in required_files:
        print("- " + str(path.relative_to(BASE_DIR)))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

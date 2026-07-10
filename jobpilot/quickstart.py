#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PROFILE_PATH = OUTPUT_DIR / "demo_profile.json"
REPORT_PATH = OUTPUT_DIR / "report.json"
CV_PATH = OUTPUT_DIR / "cv.md"
LETTER_PATH = OUTPUT_DIR / "letter.md"
JOB_PATH = BASE_DIR / "sample_data" / "sample_job.md"


def run(command: list[str]) -> None:
    print("\n$ " + " ".join(command))
    subprocess.run(command, cwd=BASE_DIR, check=True)


def ensure_dependencies() -> None:
    try:
        import jinja2  # noqa: F401
    except ModuleNotFoundError:
        print("Jinja2 not found. Installing requirements...")
        run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ensure_dependencies()

    run([sys.executable, "cli.py", "init-profile", "--output", str(PROFILE_PATH)])
    run([sys.executable, "cli.py", "evaluate-job", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--output", str(REPORT_PATH)])
    run([sys.executable, "cli.py", "generate-cv", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--cv-template", "templates/cv_template.md", "--output", str(CV_PATH)])
    run([sys.executable, "cli.py", "generate-cover-letter", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--letter-template", "templates/cover_letter_template.md", "--output", str(LETTER_PATH)])

    print("\nDone. Generated files:")
    for path in [PROFILE_PATH, REPORT_PATH, CV_PATH, LETTER_PATH]:
        print(f"- {path.relative_to(BASE_DIR)}")

    print("\nFit report preview:")
    print(json.dumps(json.loads(REPORT_PATH.read_text(encoding="utf-8")), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

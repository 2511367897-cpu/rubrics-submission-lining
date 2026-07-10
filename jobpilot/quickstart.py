#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PROFILE_PATH = OUTPUT_DIR / "demo_profile.json"
REPORT_PATH = OUTPUT_DIR / "report.json"
CV_PATH = OUTPUT_DIR / "cv.md"
LETTER_PATH = OUTPUT_DIR / "letter.md"
JOB_PATH = BASE_DIR / "sample_data" / "sample_job.md"


def run(command: List[str]) -> None:
    print("\n$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=str(BASE_DIR), check=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run([sys.executable, "cli.py", "init-profile", "--output", str(PROFILE_PATH)])
    run([sys.executable, "cli.py", "evaluate-job", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--output", str(REPORT_PATH)])
    run([sys.executable, "cli.py", "generate-cv", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--cv-template", "templates/cv_template.md", "--output", str(CV_PATH)])
    run([sys.executable, "cli.py", "generate-cover-letter", "--profile", str(PROFILE_PATH), "--job", str(JOB_PATH), "--letter-template", "templates/cover_letter_template.md", "--output", str(LETTER_PATH)])

    required_files = [PROFILE_PATH, REPORT_PATH, CV_PATH, LETTER_PATH]
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        raise RuntimeError("Quickstart did not create expected files: " + ", ".join(missing))

    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    print("\nSUCCESS: JobPilot completed without errors.")
    print("Generated files:")
    for path in required_files:
        print("- " + str(path.relative_to(BASE_DIR)))
    print("\nFit report preview:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

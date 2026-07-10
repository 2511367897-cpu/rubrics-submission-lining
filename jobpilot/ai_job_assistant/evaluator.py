from __future__ import annotations

from typing import Any

from .job import Job
from .profile import Profile


def _normalise_skill(skill: str) -> str:
    return skill.strip().lower().replace("_", "-")


def compute_skill_overlap(profile: Profile, job: Job) -> tuple[float, list[str], list[str]]:
    """Return overlap ratio, matched skills and missing skills.

    The job parser already extracts a curated skill list, so this evaluator only
    compares canonical skill names. That makes the report stable and avoids
    noisy words like company names being shown as missing skills.
    """
    profile_skills = {_normalise_skill(skill) for skill in profile.skills}
    job_skills = {_normalise_skill(skill) for skill in job.skills}

    matched = sorted(profile_skills & job_skills)
    missing = sorted(job_skills - profile_skills)
    denominator = len(job_skills) if job_skills else 1
    return len(matched) / denominator, matched, missing


def evaluate_fit(profile: Profile, job: Job) -> dict[str, Any]:
    ratio, matched, missing = compute_skill_overlap(profile, job)
    score = round(ratio * 100, 2)
    recommendations = [
        f"补充或强化 {skill}，可以进一步提高该岗位匹配度。"
        for skill in missing[:5]
    ]
    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
    }

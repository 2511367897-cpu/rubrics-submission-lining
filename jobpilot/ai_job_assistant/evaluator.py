from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .job import Job
from .profile import Profile


def _normalise_skill(skill: str) -> str:
    return " ".join(skill.strip().lower().replace("_", " ").replace("-", " ").split())


def compute_skill_overlap(profile: Profile, job: Job) -> Tuple[float, List[str], List[str]]:
    profile_skills = {_normalise_skill(skill) for skill in profile.skills}
    job_skills = {_normalise_skill(skill) for skill in job.skills}
    matched = sorted(profile_skills & job_skills)
    missing = sorted(job_skills - profile_skills)
    if not job_skills:
        return 0.0, matched, missing
    return len(matched) / len(job_skills), matched, missing


def evaluate_fit(profile: Profile, job: Job) -> Dict[str, Any]:
    ratio, matched, missing = compute_skill_overlap(profile, job)
    score = round(ratio * 100, 2)
    if not job.skills:
        summary = "No supported technical keywords were detected in the job description."
    elif score >= 80:
        summary = "Strong match based on detected skills."
    elif score >= 50:
        summary = "Partial match; several skills can be strengthened."
    else:
        summary = "Low keyword match; review the job requirements before applying."
    recommendations = [
        "补充或强化 {0}，可以进一步提高该岗位匹配度。".format(skill)
        for skill in missing[:5]
    ]
    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
        "summary": summary,
        "detected_job_skills": sorted(job.skills),
    }

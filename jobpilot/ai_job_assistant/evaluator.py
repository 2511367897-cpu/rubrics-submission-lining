from __future__ import annotations

from typing import Any

from .job import Job
from .profile import Profile

STOPWORDS = {
    "a", "an", "and", "or", "the", "to", "with", "in", "on", "for", "of", "that", "this",
    "is", "are", "by", "from", "at", "our", "your", "will", "be", "as", "it", "you", "we",
    "have", "has", "can", "should", "if", "but", "into", "about", "join", "seeking", "ideal",
    "candidate", "team", "company", "role", "work", "using", "assist", "communicate",
}


def compute_skill_overlap(profile: Profile, job: Job) -> tuple[float, list[str], list[str]]:
    profile_skills = {skill.lower() for skill in profile.skills}
    job_keywords = {word for word in job.skills if len(word) > 2 and word not in STOPWORDS}

    matched = sorted(profile_skills & job_keywords)
    missing = sorted(job_keywords - profile_skills)
    denominator = len(job_keywords) if job_keywords else 1
    return len(matched) / denominator, matched, missing


def evaluate_fit(profile: Profile, job: Job) -> dict[str, Any]:
    ratio, matched, missing = compute_skill_overlap(profile, job)
    score = round(ratio * 100, 2)
    recommendations = [
        f"Consider learning or improving your '{skill}' skills to better match this job."
        for skill in missing[:5]
    ]
    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
    }

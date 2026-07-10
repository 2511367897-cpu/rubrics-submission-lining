from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

PathLike = Union[str, Path]


@dataclass
class Experience:
    company: str
    role: str
    description: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None


@dataclass
class Education:
    institution: str
    degree: str
    field: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None


@dataclass
class Profile:
    name: str
    email: str
    phone: str
    summary: str
    skills: List[str] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profile":
        if not isinstance(data, dict):
            raise ValueError("Profile JSON must be an object.")
        required = ["name", "email", "phone", "summary"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError("Profile is missing required fields: " + ", ".join(missing))
        if not isinstance(data.get("skills", []), list):
            raise ValueError("Profile field 'skills' must be a list.")
        try:
            experience = [Experience(**item) for item in data.get("experience", [])]
            education = [Education(**item) for item in data.get("education", [])]
        except TypeError as exc:
            raise ValueError("Invalid experience or education item: {0}".format(exc)) from exc
        return cls(
            name=str(data.get("name", "")).strip(),
            email=str(data.get("email", "")).strip(),
            phone=str(data.get("phone", "")).strip(),
            summary=str(data.get("summary", "")).strip(),
            skills=[str(skill).strip().lower() for skill in data.get("skills", []) if str(skill).strip()],
            experience=experience,
            education=education,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_profile(path: PathLike) -> Profile:
    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError("Profile not found: {0}".format(profile_path))
    try:
        with profile_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Profile JSON is invalid at line {0}, column {1}: {2}".format(
                exc.lineno, exc.colno, exc.msg
            )
        ) from exc
    return Profile.from_dict(data)


def save_profile(profile: Profile, path: PathLike) -> None:
    profile_path = Path(path)
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    with profile_path.open("w", encoding="utf-8") as file:
        json.dump(profile.to_dict(), file, indent=2, ensure_ascii=False)

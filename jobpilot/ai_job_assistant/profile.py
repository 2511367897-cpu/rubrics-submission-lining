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
        experience = [Experience(**item) for item in data.get("experience", [])]
        education = [Education(**item) for item in data.get("education", [])]
        return cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            summary=data.get("summary", ""),
            skills=[str(skill).lower() for skill in data.get("skills", [])],
            experience=experience,
            education=education,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_profile(path: PathLike) -> Profile:
    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    with profile_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return Profile.from_dict(data)


def save_profile(profile: Profile, path: PathLike) -> None:
    profile_path = Path(path)
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    with profile_path.open("w", encoding="utf-8") as file:
        json.dump(profile.to_dict(), file, indent=2, ensure_ascii=False)

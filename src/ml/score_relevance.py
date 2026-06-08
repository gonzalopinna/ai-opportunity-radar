from dataclasses import dataclass
from datetime import date

import pandas as pd

from src.processing.clean_text import clean_text


@dataclass(frozen=True)
class StudentProfile:
    interests: tuple[str, ...]
    skills: tuple[str, ...]
    preferred_categories: dict[str, int]
    preferred_remote_statuses: tuple[str, ...]
    target_difficulties: tuple[str, ...]


DEFAULT_STUDENT_PROFILE = StudentProfile(
    interests=(
        "machine learning",
        "artificial intelligence",
        "ai",
        "python",
        "software engineering",
        "startups",
        "research",
        "hackathons",
        "international",
        "quant",
    ),
    skills=(
        "python",
        "machine learning",
        "pandas",
        "scikit-learn",
        "data preprocessing",
        "algorithms",
        "statistics",
        "git",
    ),
    preferred_categories={
        "internship": 15,
        "research": 14,
        "hackathon": 13,
        "startup": 12,
        "scholarship": 10,
        "competition": 8,
        "graduate_program": 7,
        "online_course": 7,
        "other": 3,
    },
    preferred_remote_statuses=("remote", "hybrid"),
    target_difficulties=("beginner", "intermediate"),
)

AI_ML_KEYWORDS = (
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data science",
    "model evaluation",
    "scikit-learn",
)


def split_skills(value: object) -> set[str]:
    """Split a normalized skills string into a set of lowercase skills."""
    text = clean_text(value).lower()
    if not text:
        return set()

    return {clean_text(skill).lower() for skill in text.split(";") if clean_text(skill)}


def build_search_text(row: pd.Series) -> str:
    """Combine opportunity fields used by the baseline scorer."""
    fields = [
        "title",
        "organization",
        "description",
        "category",
        "location",
        "required_skills",
    ]
    return " ".join(clean_text(row.get(field, "")).lower() for field in fields)


def score_interest_match(row: pd.Series, profile: StudentProfile) -> tuple[int, str]:
    search_text = build_search_text(row)
    matches = [interest for interest in profile.interests if interest in search_text]

    if not matches:
        return 0, "No strong profile interest match"

    score = round((len(matches) / len(profile.interests)) * 25)
    return min(score, 25), f"Interest match: {', '.join(matches[:4])}"


def score_skill_overlap(row: pd.Series, profile: StudentProfile) -> tuple[int, str]:
    required_skills = split_skills(row.get("required_skills", ""))
    profile_skills = set(profile.skills)

    if not required_skills:
        return 0, "No required skills listed"

    matches = sorted(required_skills & profile_skills)
    if not matches:
        return 0, "No direct skill overlap"

    score = round((len(matches) / len(required_skills)) * 25)
    return min(score, 25), f"Skill overlap: {', '.join(matches[:4])}"


def score_category(row: pd.Series, profile: StudentProfile) -> tuple[int, str]:
    category = clean_text(row.get("category", "")).lower()
    score = profile.preferred_categories.get(category, 0)

    if score:
        return score, f"Preferred category: {category}"

    return 0, "Category is not a current priority"


def score_difficulty(row: pd.Series, profile: StudentProfile) -> tuple[int, str]:
    difficulty = clean_text(row.get("difficulty", "")).lower()

    if difficulty in profile.target_difficulties:
        return 10, f"Suitable difficulty: {difficulty}"

    if difficulty == "advanced":
        return 4, "Advanced difficulty may be challenging"

    return 5, "Difficulty is unknown or partially suitable"


def score_remote_fit(row: pd.Series, profile: StudentProfile) -> tuple[int, str]:
    remote_status = clean_text(row.get("remote_or_onsite", "")).lower()

    if remote_status in profile.preferred_remote_statuses:
        return 10, f"Good location fit: {remote_status}"

    if remote_status == "onsite":
        return 4, "Onsite opportunity may require relocation"

    return 2, "Location fit is unknown"


def score_deadline(row: pd.Series, today: date | None = None) -> tuple[int, str]:
    current_date = today or date.today()
    parsed_deadline = pd.to_datetime(row.get("deadline", ""), errors="coerce")

    if pd.isna(parsed_deadline):
        return 0, "Deadline is missing or invalid"

    days_remaining = (parsed_deadline.date() - current_date).days

    if days_remaining < 0:
        return 0, "Deadline has passed"

    if days_remaining <= 7:
        return 10, "Deadline is soon"

    if days_remaining <= 30:
        return 8, "Deadline is within a month"

    if days_remaining <= 60:
        return 5, "Deadline has a comfortable timeline"

    return 2, "Deadline is far away"


def score_ai_ml_relevance(row: pd.Series) -> tuple[int, str]:
    search_text = build_search_text(row)
    matches = [keyword for keyword in AI_ML_KEYWORDS if keyword in search_text]

    if matches:
        return 5, f"AI/ML relevance: {', '.join(matches[:3])}"

    return 0, "No explicit AI/ML signal"


def score_opportunity(
    row: pd.Series,
    profile: StudentProfile = DEFAULT_STUDENT_PROFILE,
    today: date | None = None,
) -> tuple[int, str]:
    """Score one opportunity from 0 to 100 and explain the main reasons."""
    scoring_steps = [
        score_interest_match(row, profile),
        score_skill_overlap(row, profile),
        score_category(row, profile),
        score_difficulty(row, profile),
        score_remote_fit(row, profile),
        score_deadline(row, today),
        score_ai_ml_relevance(row),
    ]

    total_score = sum(score for score, _ in scoring_steps)
    reasons = [reason for score, reason in scoring_steps if score > 0]

    return min(total_score, 100), " | ".join(reasons)


def apply_relevance_scores(
    dataframe: pd.DataFrame,
    profile: StudentProfile = DEFAULT_STUDENT_PROFILE,
    today: date | None = None,
) -> pd.DataFrame:
    """Add baseline relevance score columns and sort by highest match first."""
    scored = dataframe.copy()
    scored_results = scored.apply(
        lambda row: score_opportunity(row, profile=profile, today=today),
        axis=1,
    )

    scored["match_score"] = [score for score, _ in scored_results]
    scored["match_reasons"] = [reasons for _, reasons in scored_results]
    scored = scored.sort_values(
        by=["match_score", "deadline"],
        ascending=[False, True],
    )

    return scored.reset_index(drop=True)

from datetime import date

import pandas as pd

from src.processing.clean_text import clean_text


HIGH_VALUE_ORGANIZATION_KEYWORDS = (
    "ai lab",
    "university",
    "foundation",
    "startup",
    "systems",
    "institute",
)


def days_until_deadline(row: pd.Series, today: date | None = None) -> int | None:
    """Return days until deadline, or None when the date is unavailable."""
    current_date = today or date.today()
    parsed_deadline = pd.to_datetime(row.get("deadline", ""), errors="coerce")

    if pd.isna(parsed_deadline):
        return None

    return (parsed_deadline.date() - current_date).days


def is_high_value_organization(row: pd.Series) -> bool:
    """Detect organizations that look especially valuable for the student profile."""
    organization = clean_text(row.get("organization", "")).lower()
    return any(keyword in organization for keyword in HIGH_VALUE_ORGANIZATION_KEYWORDS)


def summarize_flags(flags: list[str]) -> str:
    """Serialize anomaly flags in a readable CSV-friendly format."""
    return "; ".join(flags)


def detect_opportunity_signals(
    row: pd.Series,
    category_counts: dict[str, int],
    today: date | None = None,
) -> dict:
    """Detect urgency and unusual signals for one opportunity."""
    flags = []
    reasons = []
    urgency_score = 0

    days_remaining = days_until_deadline(row, today)
    if days_remaining is not None:
        if days_remaining < 0:
            flags.append("deadline_passed")
            reasons.append("Deadline has already passed")
        elif days_remaining <= 7:
            flags.append("deadline_soon")
            reasons.append(f"Deadline is in {days_remaining} days")
            urgency_score += 50
        elif days_remaining <= 14:
            flags.append("deadline_approaching")
            reasons.append(f"Deadline is in {days_remaining} days")
            urgency_score += 35

    match_score = int(row.get("match_score", 0))
    if match_score >= 80:
        flags.append("very_high_match")
        reasons.append(f"Very high match score: {match_score}")
        urgency_score += 25
    elif match_score >= 70:
        flags.append("high_match")
        reasons.append(f"High match score: {match_score}")
        urgency_score += 15

    category = clean_text(row.get("predicted_category", "") or row.get("category", ""))
    if category_counts.get(category, 0) == 1 and len(category_counts) > 1:
        flags.append("rare_category")
        reasons.append(f"Rare category in current run: {category}")
        urgency_score += 10

    status = clean_text(row.get("status", "")).lower()
    if status in {"new", "updated"} and is_high_value_organization(row):
        flags.append("new_or_updated_high_value_organization")
        reasons.append("New or updated opportunity from a high-value organization")
        urgency_score += 15

    is_urgent = "deadline_soon" in flags or urgency_score >= 50
    high_match = match_score >= 75

    if urgency_score >= 75:
        priority_level = "high"
    elif urgency_score >= 35:
        priority_level = "medium"
    else:
        priority_level = "low"

    return {
        "is_urgent": is_urgent,
        "high_match": high_match,
        "urgency_score": min(urgency_score, 100),
        "priority_level": priority_level,
        "anomaly_flags": summarize_flags(flags),
        "urgency_reasons": summarize_flags(reasons),
    }


def apply_urgency_detection(
    dataframe: pd.DataFrame,
    today: date | None = None,
) -> pd.DataFrame:
    """Add urgency and anomaly detection columns to the opportunities dataset."""
    detected = dataframe.copy()
    category_column = (
        "predicted_category" if "predicted_category" in detected.columns else "category"
    )
    category_counts = detected[category_column].value_counts().to_dict()

    results = detected.apply(
        lambda row: detect_opportunity_signals(row, category_counts, today=today),
        axis=1,
    )

    detected["is_urgent"] = [result["is_urgent"] for result in results]
    detected["high_match"] = [result["high_match"] for result in results]
    detected["urgency_score"] = [result["urgency_score"] for result in results]
    detected["priority_level"] = [result["priority_level"] for result in results]
    detected["anomaly_flags"] = [result["anomaly_flags"] for result in results]
    detected["urgency_reasons"] = [result["urgency_reasons"] for result in results]

    return detected

from dataclasses import dataclass
import re

import pandas as pd

from src.processing.clean_text import clean_text


SUPPORTED_CATEGORIES = (
    "internship",
    "scholarship",
    "hackathon",
    "research",
    "startup",
    "graduate_program",
    "online_course",
    "competition",
    "other",
)

CATEGORY_KEYWORDS = {
    "internship": (
        "internship",
        "intern",
        "trainee",
        "work experience",
    ),
    "scholarship": (
        "scholarship",
        "grant",
        "funding",
        "financial aid",
        "tuition",
    ),
    "hackathon": (
        "hackathon",
        "build weekend",
        "prototype",
        "team challenge",
    ),
    "research": (
        "research",
        "lab",
        "publication",
        "experiment",
        "research program",
    ),
    "startup": (
        "startup",
        "early-stage",
        "founder",
        "venture",
        "product thinking",
    ),
    "graduate_program": (
        "graduate program",
        "masters",
        "master's",
        "phd",
        "postgraduate",
    ),
    "online_course": (
        "online course",
        "course",
        "certificate",
        "curriculum",
        "learning path",
    ),
    "competition": (
        "competition",
        "contest",
        "challenge",
        "quant",
        "leaderboard",
    ),
}

CATEGORY_PRIORITY = {
    "internship": 1,
    "research": 2,
    "hackathon": 3,
    "startup": 4,
    "scholarship": 5,
    "competition": 6,
    "graduate_program": 7,
    "online_course": 8,
    "other": 9,
}

STRONG_CATEGORY_KEYWORDS = {
    "internship": ("internship", "intern"),
    "scholarship": ("scholarship",),
    "hackathon": ("hackathon",),
    "startup": ("startup", "early-stage"),
    "online_course": ("online course", "course"),
    "competition": ("competition", "contest", "quant"),
    "graduate_program": ("graduate program", "masters", "master's", "phd"),
}


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    confidence: float
    reason: str


def build_classification_text(row: pd.Series) -> str:
    """Combine text fields used by the rule-based category classifier."""
    fields = [
        "title",
        "organization",
        "description",
        "location",
        "required_skills",
    ]
    return " ".join(clean_text(row.get(field, "")).lower() for field in fields)


def keyword_matches(search_text: str, keyword: str) -> bool:
    """Return True when a keyword appears as a phrase, not inside another word."""
    pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
    return re.search(pattern, search_text) is not None


def classify_opportunity(row: pd.Series) -> ClassificationResult:
    """Classify one opportunity using a transparent keyword baseline."""
    search_text = build_classification_text(row)

    for category, keywords in STRONG_CATEGORY_KEYWORDS.items():
        matches = [keyword for keyword in keywords if keyword_matches(search_text, keyword)]
        if matches:
            confidence = min(0.7 + (0.1 * len(matches)), 0.95)
            return ClassificationResult(
                category=category,
                confidence=round(confidence, 2),
                reason=f"Matched strong {category} keywords: {', '.join(matches[:4])}",
            )

    category_matches = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        matches = [keyword for keyword in keywords if keyword_matches(search_text, keyword)]
        if matches:
            category_matches[category] = matches

    if not category_matches:
        return ClassificationResult(
            category="other",
            confidence=0.3,
            reason="No category-specific keywords matched",
        )

    best_category = sorted(
        category_matches,
        key=lambda category: (
            -len(category_matches[category]),
            CATEGORY_PRIORITY[category],
        ),
    )[0]
    matches = category_matches[best_category]
    confidence = min(0.5 + (0.15 * len(matches)), 0.95)

    return ClassificationResult(
        category=best_category,
        confidence=round(confidence, 2),
        reason=f"Matched {best_category} keywords: {', '.join(matches[:4])}",
    )


def apply_category_classification(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add predicted category columns without overwriting the normalized category."""
    classified = dataframe.copy()
    results = classified.apply(classify_opportunity, axis=1)

    classified["predicted_category"] = [result.category for result in results]
    classified["category_confidence"] = [result.confidence for result in results]
    classified["category_reason"] = [result.reason for result in results]

    return classified

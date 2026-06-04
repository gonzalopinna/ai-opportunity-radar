from src.processing.clean_text import clean_text


VALID_CATEGORIES = {
    "internship",
    "scholarship",
    "hackathon",
    "research",
    "startup",
    "graduate_program",
    "online_course",
    "competition",
    "other",
}

CATEGORY_ALIASES = {
    "graduate program": "graduate_program",
    "graduate-program": "graduate_program",
    "grad program": "graduate_program",
    "online course": "online_course",
    "online-course": "online_course",
    "course": "online_course",
    "startup role": "startup",
    "startup_roles": "startup",
    "research program": "research",
    "contest": "competition",
}

VALID_REMOTE_STATUSES = {"remote", "onsite", "hybrid", "unknown"}

REMOTE_ALIASES = {
    "on site": "onsite",
    "on-site": "onsite",
    "in person": "onsite",
    "in-person": "onsite",
    "online": "remote",
    "virtual": "remote",
    "mixed": "hybrid",
}

VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced", "unknown"}

DIFFICULTY_ALIASES = {
    "easy": "beginner",
    "entry": "beginner",
    "entry level": "beginner",
    "medium": "intermediate",
    "mid": "intermediate",
    "hard": "advanced",
}


def normalize_label(value: object) -> str:
    """Normalize a label-like value into lowercase words separated by underscores."""
    text = clean_text(value).lower()
    text = text.replace("-", " ").replace("_", " ")
    return "_".join(text.split())


def normalize_category(value: object) -> str:
    """Normalize opportunity categories into the supported project labels."""
    raw_text = clean_text(value).lower()
    alias_key = raw_text.replace("_", " ").replace("-", " ")
    normalized = CATEGORY_ALIASES.get(alias_key, normalize_label(value))

    if normalized in VALID_CATEGORIES:
        return normalized

    return "other"


def normalize_remote_status(value: object) -> str:
    """Normalize remote, onsite, and hybrid values."""
    raw_text = clean_text(value).lower()
    alias_key = raw_text.replace("_", " ").replace("-", " ")
    normalized = REMOTE_ALIASES.get(alias_key, normalize_label(value))

    if normalized in VALID_REMOTE_STATUSES:
        return normalized

    return "unknown"


def normalize_required_skills(value: object) -> str:
    """Normalize a skills field into a semicolon-separated lowercase string."""
    text = clean_text(value)
    if not text:
        return ""

    separators_normalized = text.replace(",", ";")
    skills = []
    seen = set()

    for item in separators_normalized.split(";"):
        skill = clean_text(item).lower()
        if skill and skill not in seen:
            skills.append(skill)
            seen.add(skill)

    return "; ".join(skills)


def normalize_difficulty(value: object) -> str:
    """Normalize opportunity difficulty values when the column is available."""
    raw_text = clean_text(value).lower()
    alias_key = raw_text.replace("_", " ").replace("-", " ")
    normalized = DIFFICULTY_ALIASES.get(alias_key, normalize_label(value))

    if normalized in VALID_DIFFICULTIES:
        return normalized

    return "unknown"

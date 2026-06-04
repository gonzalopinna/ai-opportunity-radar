from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_DIR, SAMPLE_DATA_DIR
from src.processing.clean_text import clean_text_columns
from src.processing.deadline_parser import parse_deadline
from src.processing.normalize import (
    normalize_category,
    normalize_difficulty,
    normalize_remote_status,
    normalize_required_skills,
)


DEFAULT_INPUT_PATH = SAMPLE_DATA_DIR / "opportunities_sample.csv"
DEFAULT_OUTPUT_PATH = PROCESSED_DATA_DIR / "opportunities_processed.csv"

REQUIRED_COLUMNS = {
    "id",
    "title",
    "organization",
    "description",
    "category",
    "location",
    "remote_or_onsite",
    "deadline",
    "url",
    "source",
    "required_skills",
    "created_at",
    "first_seen_date",
    "last_seen_date",
}

TEXT_COLUMNS = ["title", "organization", "description", "location"]


def load_opportunities(path: Path = DEFAULT_INPUT_PATH) -> pd.DataFrame:
    """Load the sample opportunities dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Input dataset not found: {path}")

    return pd.read_csv(path)


def validate_required_columns(dataframe: pd.DataFrame) -> None:
    """Raise a clear error if the dataset is missing required columns."""
    missing_columns = sorted(REQUIRED_COLUMNS - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")


def preprocess_opportunities(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the opportunities dataset."""
    validate_required_columns(dataframe)
    processed = dataframe.copy()

    for column in TEXT_COLUMNS:
        processed[column] = processed[column].apply(clean_text_columns)

    processed["category"] = processed["category"].apply(normalize_category)
    processed["remote_or_onsite"] = processed["remote_or_onsite"].apply(
        normalize_remote_status
    )
    processed["deadline"] = processed["deadline"].apply(parse_deadline)
    processed["required_skills"] = processed["required_skills"].apply(
        normalize_required_skills
    )

    if "difficulty" in processed.columns:
        processed["difficulty"] = processed["difficulty"].apply(normalize_difficulty)

    return processed


def save_processed_opportunities(
    dataframe: pd.DataFrame,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """Save the processed dataset as a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    return output_path


def run_preprocessing_pipeline(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> tuple[pd.DataFrame, Path]:
    """Load, validate, preprocess, and save the opportunities dataset."""
    raw_opportunities = load_opportunities(input_path)
    processed_opportunities = preprocess_opportunities(raw_opportunities)
    saved_path = save_processed_opportunities(processed_opportunities, output_path)

    return processed_opportunities, saved_path

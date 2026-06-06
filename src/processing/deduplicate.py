import hashlib
import json

import pandas as pd

from src.processing.clean_text import clean_text


CONTENT_HASH_COLUMNS = [
    "title",
    "organization",
    "description",
    "category",
    "location",
    "remote_or_onsite",
    "deadline",
    "url",
    "required_skills",
    "difficulty",
]


def make_identity_key(row: pd.Series) -> str:
    """Create a stable key used to identify the same opportunity across runs."""
    url = clean_text(row.get("url", "")).lower()
    if url:
        return f"url::{url}"

    title = clean_text(row.get("title", "")).lower()
    organization = clean_text(row.get("organization", "")).lower()
    return f"title_org::{title}::{organization}"


def make_content_hash(row: pd.Series) -> str:
    """Create a hash of fields that should mark an opportunity as updated."""
    content = {
        column: clean_text(row.get(column, "")).lower()
        for column in CONTENT_HASH_COLUMNS
        if column in row.index
    }
    serialized = json.dumps(content, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def add_tracking_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add identity and content tracking fields to a processed dataset."""
    tracked = dataframe.copy()
    tracked["identity_key"] = tracked.apply(make_identity_key, axis=1)
    tracked["content_hash"] = tracked.apply(make_content_hash, axis=1)
    return tracked


def deduplicate_opportunities(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate opportunities from the current run."""
    tracked = add_tracking_columns(dataframe)
    tracked["duplicate_count"] = tracked.groupby("identity_key")["identity_key"].transform(
        "size"
    )

    deduplicated = tracked.drop_duplicates(subset=["identity_key"], keep="first")
    return deduplicated.reset_index(drop=True)

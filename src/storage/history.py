from datetime import date
from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_DIR


DEFAULT_HISTORY_PATH = PROCESSED_DATA_DIR / "opportunities_history.csv"


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> pd.DataFrame:
    """Load historical opportunities if the history file already exists."""
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def compare_with_history(
    current_opportunities: pd.DataFrame,
    history: pd.DataFrame,
    run_date: str | None = None,
) -> pd.DataFrame:
    """Mark current opportunities as new, already seen, or updated."""
    today = run_date or date.today().isoformat()
    compared = current_opportunities.copy()

    if history.empty:
        compared["status"] = "new"
        compared["first_seen_date"] = compared["first_seen_date"].fillna(today)
        compared["last_seen_date"] = today
        return compared

    history_by_key = history.drop_duplicates(subset=["identity_key"], keep="last")
    history_by_key = history_by_key.set_index("identity_key")

    statuses = []
    first_seen_dates = []

    for _, row in compared.iterrows():
        identity_key = row["identity_key"]

        if identity_key not in history_by_key.index:
            statuses.append("new")
            first_seen_dates.append(row.get("first_seen_date") or today)
            continue

        historical_row = history_by_key.loc[identity_key]
        first_seen_dates.append(historical_row.get("first_seen_date") or today)

        if row["content_hash"] != historical_row.get("content_hash"):
            statuses.append("updated")
        else:
            statuses.append("already_seen")

    compared["status"] = statuses
    compared["first_seen_date"] = first_seen_dates
    compared["last_seen_date"] = today
    return compared


def save_history(
    current_opportunities: pd.DataFrame,
    previous_history: pd.DataFrame,
    path: Path = DEFAULT_HISTORY_PATH,
) -> Path:
    """Save the latest current records while keeping older unseen records."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if previous_history.empty:
        updated_history = current_opportunities.copy()
    else:
        current_keys = set(current_opportunities["identity_key"])
        older_unseen = previous_history[
            ~previous_history["identity_key"].isin(current_keys)
        ]
        updated_history = pd.concat(
            [older_unseen, current_opportunities],
            ignore_index=True,
        )

    updated_history.to_csv(path, index=False)
    return path


def run_history_comparison(
    current_opportunities: pd.DataFrame,
    history_path: Path = DEFAULT_HISTORY_PATH,
    run_date: str | None = None,
) -> tuple[pd.DataFrame, Path]:
    """Compare current opportunities with history and save the updated history."""
    previous_history = load_history(history_path)
    compared = compare_with_history(current_opportunities, previous_history, run_date)
    saved_path = save_history(compared, previous_history, history_path)
    return compared, saved_path

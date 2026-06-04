import pandas as pd


def parse_deadline(value: object) -> str:
    """Parse a deadline safely and return an ISO date string or an empty value."""
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return ""

    return parsed.date().isoformat()

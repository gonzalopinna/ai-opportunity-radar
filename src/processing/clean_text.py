import re


def clean_text(value: object) -> str:
    """Return a readable text value with extra whitespace removed."""
    if value is None:
        return ""

    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def clean_text_columns(row_value: object) -> str:
    """Alias used by dataframe pipelines to make the cleaning step explicit."""
    return clean_text(row_value)

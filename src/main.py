from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample" / "opportunities_sample.csv"


def load_sample_opportunities(path: Path = SAMPLE_DATA_PATH) -> pd.DataFrame:
    """Load the Sprint 1 sample opportunity dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Sample dataset not found: {path}")

    return pd.read_csv(path)


def run_placeholder_pipeline() -> None:
    """Run the initial placeholder pipeline for Sprint 1."""
    opportunities = load_sample_opportunities()

    print("AI Opportunity Radar - Sprint 1 placeholder pipeline")
    print(f"Loaded {len(opportunities)} sample opportunities.")
    print()
    print("Opportunities by category:")

    category_counts = opportunities["category"].value_counts().sort_index()
    for category, count in category_counts.items():
        print(f"- {category}: {count}")

    print()
    print("Next sprint: implement data loading, cleaning, and normalization.")


if __name__ == "__main__":
    run_placeholder_pipeline()

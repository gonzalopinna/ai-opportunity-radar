from src.processing.preprocess_dataset import run_preprocessing_pipeline


def run_pipeline() -> None:
    """Run the Sprint 2 preprocessing pipeline."""
    processed_opportunities, saved_path = run_preprocessing_pipeline()

    print("AI Opportunity Radar - Sprint 2 preprocessing pipeline")
    print(f"Processed {len(processed_opportunities)} opportunities.")
    print(f"Saved cleaned dataset to: {saved_path}")


if __name__ == "__main__":
    run_pipeline()

from src.ml.classify_opportunities import apply_category_classification
from src.ml.evaluate_classification import run_classification_evaluation
from src.ml.score_relevance import apply_relevance_scores
from src.processing.deduplicate import deduplicate_opportunities
from src.processing.preprocess_dataset import (
    DEFAULT_OUTPUT_PATH,
    run_preprocessing_pipeline,
    save_processed_opportunities,
)
from src.storage.history import run_history_comparison


def run_pipeline() -> None:
    """Run the data pipeline with category classification and relevance scoring."""
    processed_opportunities, _ = run_preprocessing_pipeline()
    deduplicated_opportunities = deduplicate_opportunities(processed_opportunities)
    compared_opportunities, history_path = run_history_comparison(
        deduplicated_opportunities
    )
    classified_opportunities = apply_category_classification(compared_opportunities)
    evaluation_results, evaluation_path = run_classification_evaluation(
        classified_opportunities
    )
    scored_opportunities = apply_relevance_scores(classified_opportunities)
    saved_path = save_processed_opportunities(scored_opportunities, DEFAULT_OUTPUT_PATH)

    removed_duplicates = len(processed_opportunities) - len(deduplicated_opportunities)

    print("AI Opportunity Radar - classification and relevance pipeline")
    print(f"Processed {len(scored_opportunities)} opportunities.")
    print(f"Removed {removed_duplicates} duplicate opportunities.")
    print("Status counts:")

    for status, count in scored_opportunities["status"].value_counts().items():
        print(f"- {status}: {count}")

    print("Predicted category counts:")

    for category, count in scored_opportunities["predicted_category"].value_counts().items():
        print(f"- {category}: {count}")

    print(
        "Classification evaluation: "
        f"accuracy={evaluation_results['accuracy']}, "
        f"f1_macro={evaluation_results['f1_macro']}"
    )

    top_opportunity = scored_opportunities.iloc[0]
    print(
        "Top match: "
        f"{top_opportunity['title']} ({top_opportunity['match_score']}/100)"
    )
    print(f"Saved current processed dataset to: {saved_path}")
    print(f"Saved updated opportunity history to: {history_path}")
    print(f"Saved classification evaluation to: {evaluation_path}")


if __name__ == "__main__":
    run_pipeline()

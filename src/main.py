from src.ml.classify_opportunities import apply_category_classification
from src.ml.cluster_opportunities import apply_opportunity_clustering
from src.ml.detect_anomalies import apply_urgency_detection
from src.ml.evaluate_classification import run_classification_evaluation
from src.ml.score_relevance import apply_relevance_scores
from src.processing.deduplicate import deduplicate_opportunities
from src.processing.preprocess_dataset import (
    DEFAULT_OUTPUT_PATH,
    run_preprocessing_pipeline,
    save_processed_opportunities,
)
from src.reports.generate_report import save_daily_reports
from src.storage.history import run_history_comparison


def run_pipeline() -> None:
    """Run the data pipeline with classification, clustering, and scoring."""
    processed_opportunities, _ = run_preprocessing_pipeline()
    deduplicated_opportunities = deduplicate_opportunities(processed_opportunities)
    compared_opportunities, history_path = run_history_comparison(
        deduplicated_opportunities
    )
    classified_opportunities = apply_category_classification(compared_opportunities)
    evaluation_results, evaluation_path = run_classification_evaluation(
        classified_opportunities
    )
    clustered_opportunities = apply_opportunity_clustering(classified_opportunities)
    scored_opportunities = apply_relevance_scores(clustered_opportunities)
    final_opportunities = apply_urgency_detection(scored_opportunities)
    saved_path = save_processed_opportunities(final_opportunities, DEFAULT_OUTPUT_PATH)
    markdown_report_path, html_report_path = save_daily_reports(final_opportunities)

    removed_duplicates = len(processed_opportunities) - len(deduplicated_opportunities)

    print("AI Opportunity Radar - classification, clustering, and relevance pipeline")
    print(f"Processed {len(final_opportunities)} opportunities.")
    print(f"Removed {removed_duplicates} duplicate opportunities.")
    print("Status counts:")

    for status, count in final_opportunities["status"].value_counts().items():
        print(f"- {status}: {count}")

    print("Predicted category counts:")

    for category, count in final_opportunities["predicted_category"].value_counts().items():
        print(f"- {category}: {count}")

    print("Cluster counts:")

    for cluster_label, count in final_opportunities["cluster_label"].value_counts().items():
        print(f"- {cluster_label}: {count}")

    urgent_count = int(final_opportunities["is_urgent"].sum())
    high_match_count = int(final_opportunities["high_match"].sum())
    print(f"Urgent opportunities: {urgent_count}")
    print(f"High-match opportunities: {high_match_count}")

    print(
        "Classification evaluation: "
        f"accuracy={evaluation_results['accuracy']}, "
        f"f1_macro={evaluation_results['f1_macro']}"
    )

    top_opportunity = final_opportunities.iloc[0]
    print(
        "Top match: "
        f"{top_opportunity['title']} ({top_opportunity['match_score']}/100)"
    )
    print(f"Saved current processed dataset to: {saved_path}")
    print(f"Saved updated opportunity history to: {history_path}")
    print(f"Saved classification evaluation to: {evaluation_path}")
    print(f"Saved Markdown report to: {markdown_report_path}")
    print(f"Saved HTML report to: {html_report_path}")


if __name__ == "__main__":
    run_pipeline()

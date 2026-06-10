import json
from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_DIR
from src.ml.classify_opportunities import SUPPORTED_CATEGORIES


DEFAULT_EVALUATION_PATH = PROCESSED_DATA_DIR / "classification_evaluation.json"


def round_metric(value: float) -> float:
    """Round metrics to a readable number of decimal places."""
    return round(float(value), 3)


def safe_divide(numerator: float, denominator: float) -> float:
    """Divide safely and return zero when the denominator is zero."""
    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_category_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    labels: tuple[str, ...] = SUPPORTED_CATEGORIES,
) -> dict:
    """Calculate precision, recall, F1, and support for each category."""
    per_category = {}

    for label in labels:
        true_positive = int(((y_true == label) & (y_pred == label)).sum())
        false_positive = int(((y_true != label) & (y_pred == label)).sum())
        false_negative = int(((y_true == label) & (y_pred != label)).sum())
        support = int((y_true == label).sum())

        precision = safe_divide(true_positive, true_positive + false_positive)
        recall = safe_divide(true_positive, true_positive + false_negative)
        f1 = safe_divide(2 * precision * recall, precision + recall)

        per_category[label] = {
            "precision": round_metric(precision),
            "recall": round_metric(recall),
            "f1": round_metric(f1),
            "support": support,
        }

    return per_category


def average_metric(
    per_category: dict,
    metric_name: str,
    labels: tuple[str, ...],
) -> float:
    """Calculate a macro average across all supported categories."""
    values = [per_category[label][metric_name] for label in labels]
    return round_metric(sum(values) / len(values))


def weighted_average_metric(per_category: dict, metric_name: str) -> float:
    """Calculate a support-weighted average across supported categories."""
    total_support = sum(metrics["support"] for metrics in per_category.values())
    if total_support == 0:
        return 0.0

    weighted_sum = sum(
        metrics[metric_name] * metrics["support"]
        for metrics in per_category.values()
    )
    return round_metric(weighted_sum / total_support)


def evaluate_category_predictions(
    dataframe: pd.DataFrame,
    true_column: str = "category",
    predicted_column: str = "predicted_category",
) -> dict:
    """Evaluate predicted opportunity categories against labeled sample data."""
    if true_column not in dataframe.columns:
        raise ValueError(f"Missing true label column: {true_column}")

    if predicted_column not in dataframe.columns:
        raise ValueError(f"Missing predicted label column: {predicted_column}")

    evaluation_data = dataframe[[true_column, predicted_column]].dropna()
    if evaluation_data.empty:
        raise ValueError("No labeled rows available for classification evaluation.")

    y_true = evaluation_data[true_column].astype(str)
    y_pred = evaluation_data[predicted_column].astype(str)
    active_labels = tuple(
        label
        for label in SUPPORTED_CATEGORIES
        if ((y_true == label).any() or (y_pred == label).any())
    )
    per_category = calculate_category_metrics(y_true, y_pred)
    correct_predictions = int((y_true == y_pred).sum())

    return {
        "model_type": "rule_based_keyword_baseline",
        "label_column": true_column,
        "prediction_column": predicted_column,
        "num_examples": int(len(evaluation_data)),
        "accuracy": round_metric(correct_predictions / len(evaluation_data)),
        "precision_macro": average_metric(per_category, "precision", active_labels),
        "recall_macro": average_metric(per_category, "recall", active_labels),
        "f1_macro": average_metric(per_category, "f1", active_labels),
        "precision_weighted": weighted_average_metric(per_category, "precision"),
        "recall_weighted": weighted_average_metric(per_category, "recall"),
        "f1_weighted": weighted_average_metric(per_category, "f1"),
        "per_category": per_category,
    }


def save_evaluation_results(
    evaluation_results: dict,
    output_path: Path = DEFAULT_EVALUATION_PATH,
) -> Path:
    """Save classification evaluation metrics as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(evaluation_results, indent=2),
        encoding="utf-8",
    )
    return output_path


def run_classification_evaluation(
    dataframe: pd.DataFrame,
    output_path: Path = DEFAULT_EVALUATION_PATH,
) -> tuple[dict, Path]:
    """Evaluate category predictions and save the metrics."""
    evaluation_results = evaluate_category_predictions(dataframe)
    saved_path = save_evaluation_results(evaluation_results, output_path)
    return evaluation_results, saved_path

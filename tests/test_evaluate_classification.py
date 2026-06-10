import unittest
from pathlib import Path

import pandas as pd

from src.ml.evaluate_classification import (
    evaluate_category_predictions,
    run_classification_evaluation,
)


class EvaluateClassificationTests(unittest.TestCase):
    def test_evaluate_category_predictions_returns_core_metrics(self):
        dataframe = pd.DataFrame(
            [
                {"category": "internship", "predicted_category": "internship"},
                {"category": "scholarship", "predicted_category": "scholarship"},
                {"category": "hackathon", "predicted_category": "startup"},
            ]
        )

        results = evaluate_category_predictions(dataframe)

        self.assertEqual(results["num_examples"], 3)
        self.assertEqual(results["accuracy"], 0.667)
        self.assertIn("precision_macro", results)
        self.assertIn("recall_macro", results)
        self.assertIn("f1_macro", results)
        self.assertIn("hackathon", results["per_category"])

    def test_evaluate_category_predictions_requires_label_columns(self):
        dataframe = pd.DataFrame([{"category": "internship"}])

        with self.assertRaises(ValueError):
            evaluate_category_predictions(dataframe)

    def test_run_classification_evaluation_saves_json_file(self):
        dataframe = pd.DataFrame(
            [
                {"category": "internship", "predicted_category": "internship"},
                {"category": "startup", "predicted_category": "startup"},
            ]
        )

        output_path = Path("data/processed/test_classification_evaluation.json")
        results, saved_path = run_classification_evaluation(dataframe, output_path)

        self.assertEqual(saved_path, output_path)
        self.assertTrue(output_path.exists())
        self.assertEqual(results["accuracy"], 1.0)
        self.assertEqual(results["f1_macro"], 1.0)


if __name__ == "__main__":
    unittest.main()

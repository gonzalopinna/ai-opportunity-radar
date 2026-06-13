from datetime import date
import unittest

import pandas as pd

from src.ml.detect_anomalies import (
    apply_urgency_detection,
    days_until_deadline,
    detect_opportunity_signals,
    is_high_value_organization,
)


class DetectAnomaliesTests(unittest.TestCase):
    def test_days_until_deadline_returns_remaining_days(self):
        row = pd.Series({"deadline": "2026-06-20"})

        self.assertEqual(days_until_deadline(row, today=date(2026, 6, 13)), 7)

    def test_is_high_value_organization_detects_keywords(self):
        row = pd.Series({"organization": "Global AI Lab"})

        self.assertTrue(is_high_value_organization(row))

    def test_detect_opportunity_signals_marks_soon_deadline_as_urgent(self):
        row = pd.Series(
            {
                "deadline": "2026-06-20",
                "match_score": 65,
                "predicted_category": "competition",
                "status": "already_seen",
                "organization": "Market Systems Group",
            }
        )

        result = detect_opportunity_signals(
            row,
            category_counts={"competition": 1, "internship": 2},
            today=date(2026, 6, 13),
        )

        self.assertTrue(result["is_urgent"])
        self.assertIn("deadline_soon", result["anomaly_flags"])
        self.assertGreaterEqual(result["urgency_score"], 50)

    def test_detect_opportunity_signals_marks_high_match(self):
        row = pd.Series(
            {
                "deadline": "2026-08-01",
                "match_score": 82,
                "predicted_category": "internship",
                "status": "new",
                "organization": "Global AI Lab",
            }
        )

        result = detect_opportunity_signals(
            row,
            category_counts={"internship": 1, "hackathon": 1},
            today=date(2026, 6, 13),
        )

        self.assertTrue(result["high_match"])
        self.assertIn("very_high_match", result["anomaly_flags"])
        self.assertIn("new_or_updated_high_value_organization", result["anomaly_flags"])

    def test_apply_urgency_detection_adds_expected_columns(self):
        dataframe = pd.DataFrame(
            [
                {
                    "title": "Quant Competition",
                    "deadline": "2026-06-20",
                    "match_score": 70,
                    "predicted_category": "competition",
                    "status": "new",
                    "organization": "Market Systems Group",
                }
            ]
        )

        detected = apply_urgency_detection(dataframe, today=date(2026, 6, 13))

        self.assertIn("is_urgent", detected.columns)
        self.assertIn("high_match", detected.columns)
        self.assertIn("urgency_score", detected.columns)
        self.assertIn("anomaly_flags", detected.columns)
        self.assertTrue(bool(detected.iloc[0]["is_urgent"]))


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

import pandas as pd

from src.processing.normalize import (
    normalize_category,
    normalize_difficulty,
    normalize_remote_status,
    normalize_required_skills,
)
from src.processing.preprocess_dataset import (
    preprocess_opportunities,
    run_preprocessing_pipeline,
)


class NormalizeTests(unittest.TestCase):
    def test_normalize_category_uses_supported_labels(self):
        self.assertEqual(normalize_category("Online Course"), "online_course")
        self.assertEqual(normalize_category("Graduate Program"), "graduate_program")
        self.assertEqual(normalize_category("Unexpected Value"), "other")

    def test_normalize_remote_status_uses_supported_labels(self):
        self.assertEqual(normalize_remote_status("On-site"), "onsite")
        self.assertEqual(normalize_remote_status("Virtual"), "remote")
        self.assertEqual(normalize_remote_status("Unknown value"), "unknown")

    def test_normalize_required_skills_returns_consistent_string(self):
        skills = normalize_required_skills(" Python; python, Machine Learning ")
        self.assertEqual(skills, "python; machine learning")

    def test_normalize_difficulty_uses_supported_labels(self):
        self.assertEqual(normalize_difficulty("Entry Level"), "beginner")
        self.assertEqual(normalize_difficulty("Hard"), "advanced")
        self.assertEqual(normalize_difficulty("Not sure"), "unknown")


class PreprocessDatasetTests(unittest.TestCase):
    def test_preprocess_opportunities_cleans_and_normalizes_fields(self):
        dataframe = pd.DataFrame(
            [
                {
                    "id": "opp-001",
                    "title": "  AI   Internship ",
                    "organization": " Global   AI Lab ",
                    "description": " Build   ML tools. ",
                    "category": "Online Course",
                    "location": " Remote ",
                    "remote_or_onsite": "Virtual",
                    "deadline": "2026-07-15",
                    "url": "https://example.com",
                    "source": "manual",
                    "required_skills": "Python, Machine Learning; Python",
                    "difficulty": "Entry Level",
                    "created_at": "2026-06-03",
                    "first_seen_date": "2026-06-03",
                    "last_seen_date": "2026-06-03",
                }
            ]
        )

        processed = preprocess_opportunities(dataframe)
        row = processed.iloc[0]

        self.assertEqual(row["title"], "AI Internship")
        self.assertEqual(row["organization"], "Global AI Lab")
        self.assertEqual(row["description"], "Build ML tools.")
        self.assertEqual(row["category"], "online_course")
        self.assertEqual(row["remote_or_onsite"], "remote")
        self.assertEqual(row["deadline"], "2026-07-15")
        self.assertEqual(row["required_skills"], "python; machine learning")
        self.assertEqual(row["difficulty"], "beginner")

    def test_preprocess_opportunities_rejects_missing_required_columns(self):
        dataframe = pd.DataFrame([{"id": "opp-001"}])

        with self.assertRaises(ValueError):
            preprocess_opportunities(dataframe)

    def test_run_preprocessing_pipeline_saves_output_file(self):
        input_path = Path("data/sample/opportunities_sample.csv")
        output_path = Path("data/processed/test_opportunities_processed.csv")

        processed, saved_path = run_preprocessing_pipeline(input_path, output_path)

        self.assertEqual(saved_path, output_path)
        self.assertTrue(output_path.exists())
        self.assertEqual(len(processed), 6)


if __name__ == "__main__":
    unittest.main()

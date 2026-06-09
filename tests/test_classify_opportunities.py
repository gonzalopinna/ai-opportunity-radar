import unittest

import pandas as pd

from src.ml.classify_opportunities import (
    apply_category_classification,
    classify_opportunity,
)


class ClassifyOpportunitiesTests(unittest.TestCase):
    def test_classify_opportunity_detects_internship(self):
        row = pd.Series(
            {
                "title": "AI Research Internship",
                "organization": "Global AI Lab",
                "description": "Summer internship with applied machine learning work.",
                "required_skills": "python; machine learning",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "internship")
        self.assertGreaterEqual(result.confidence, 0.65)
        self.assertIn("internship", result.reason)

    def test_classify_opportunity_detects_online_course(self):
        row = pd.Series(
            {
                "title": "Applied AI Online Course",
                "organization": "Open Learning Institute",
                "description": "Project-based online course with a certificate.",
                "required_skills": "python",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "online_course")

    def test_classify_opportunity_prefers_internship_for_research_internship(self):
        row = pd.Series(
            {
                "title": "AI Research Internship",
                "organization": "Global AI Lab",
                "description": "Work with researchers on applied experiments.",
                "required_skills": "python; machine learning",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "internship")

    def test_classify_opportunity_detects_quant_competition_signal(self):
        row = pd.Series(
            {
                "title": "Quant Software Summer Program",
                "organization": "Market Systems Group",
                "description": "Introductory program for quantitative systems.",
                "required_skills": "python; algorithms; statistics",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "competition")

    def test_classify_opportunity_does_not_treat_international_as_internship(self):
        row = pd.Series(
            {
                "title": "International CS Scholarship",
                "organization": "Future Engineers Foundation",
                "description": "Scholarship for international study.",
                "required_skills": "programming",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "scholarship")

    def test_classify_opportunity_returns_other_without_keyword_match(self):
        row = pd.Series(
            {
                "title": "Student Opportunity",
                "organization": "Example Organization",
                "description": "General announcement for students.",
                "required_skills": "",
            }
        )

        result = classify_opportunity(row)

        self.assertEqual(result.category, "other")
        self.assertEqual(result.confidence, 0.3)

    def test_apply_category_classification_adds_prediction_columns(self):
        dataframe = pd.DataFrame(
            [
                {
                    "title": "Machine Learning Hackathon",
                    "organization": "Tech University",
                    "description": "Build a prototype during a weekend hackathon.",
                    "required_skills": "python; teamwork",
                    "category": "hackathon",
                }
            ]
        )

        classified = apply_category_classification(dataframe)

        self.assertIn("predicted_category", classified.columns)
        self.assertIn("category_confidence", classified.columns)
        self.assertIn("category_reason", classified.columns)
        self.assertEqual(classified.iloc[0]["predicted_category"], "hackathon")


if __name__ == "__main__":
    unittest.main()

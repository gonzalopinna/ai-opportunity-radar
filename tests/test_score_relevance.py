from datetime import date
import unittest

import pandas as pd

from src.ml.score_relevance import (
    apply_relevance_scores,
    score_deadline,
    score_opportunity,
    split_skills,
)


class ScoreRelevanceTests(unittest.TestCase):
    def test_split_skills_returns_lowercase_set(self):
        skills = split_skills("Python; Machine Learning; python")

        self.assertEqual(skills, {"python", "machine learning"})

    def test_score_deadline_rewards_near_future_deadline(self):
        row = pd.Series({"deadline": "2026-06-12"})

        score, reason = score_deadline(row, today=date(2026, 6, 8))

        self.assertEqual(score, 10)
        self.assertEqual(reason, "Deadline is soon")

    def test_score_opportunity_returns_score_and_reasons(self):
        row = pd.Series(
            {
                "title": "AI Research Internship",
                "organization": "Global AI Lab",
                "description": "Applied machine learning and model evaluation work.",
                "category": "internship",
                "location": "Remote",
                "remote_or_onsite": "remote",
                "deadline": "2026-07-15",
                "required_skills": "python; machine learning; pandas",
                "difficulty": "intermediate",
            }
        )

        score, reasons = score_opportunity(row, today=date(2026, 6, 8))

        self.assertGreaterEqual(score, 70)
        self.assertIn("Skill overlap", reasons)
        self.assertIn("Preferred category", reasons)

    def test_apply_relevance_scores_adds_columns_and_sorts(self):
        dataframe = pd.DataFrame(
            [
                {
                    "title": "General Scholarship",
                    "organization": "Example Foundation",
                    "description": "Funding for students.",
                    "category": "scholarship",
                    "location": "Onsite",
                    "remote_or_onsite": "onsite",
                    "deadline": "2026-09-01",
                    "required_skills": "essay writing",
                    "difficulty": "unknown",
                },
                {
                    "title": "AI Research Internship",
                    "organization": "Global AI Lab",
                    "description": "Applied machine learning work.",
                    "category": "internship",
                    "location": "Remote",
                    "remote_or_onsite": "remote",
                    "deadline": "2026-07-15",
                    "required_skills": "python; machine learning; pandas",
                    "difficulty": "intermediate",
                },
            ]
        )

        scored = apply_relevance_scores(dataframe, today=date(2026, 6, 8))

        self.assertIn("match_score", scored.columns)
        self.assertIn("match_reasons", scored.columns)
        self.assertEqual(scored.iloc[0]["title"], "AI Research Internship")
        self.assertGreater(scored.iloc[0]["match_score"], scored.iloc[1]["match_score"])


if __name__ == "__main__":
    unittest.main()

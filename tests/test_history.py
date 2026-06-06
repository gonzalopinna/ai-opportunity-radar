import unittest

import pandas as pd

from src.processing.deduplicate import deduplicate_opportunities
from src.storage.history import compare_with_history


def sample_current_opportunity(description: str = "Applied ML work.") -> pd.DataFrame:
    return deduplicate_opportunities(
        pd.DataFrame(
            [
                {
                    "id": "opp-001",
                    "title": "AI Internship",
                    "organization": "Global AI Lab",
                    "description": description,
                    "category": "internship",
                    "location": "Remote",
                    "remote_or_onsite": "remote",
                    "deadline": "2026-07-15",
                    "url": "https://example.com/apply",
                    "required_skills": "python",
                    "difficulty": "intermediate",
                    "first_seen_date": "2026-06-03",
                }
            ]
        )
    )


class HistoryTests(unittest.TestCase):
    def test_compare_with_empty_history_marks_all_current_records_new(self):
        current = sample_current_opportunity()

        compared = compare_with_history(current, pd.DataFrame(), run_date="2026-06-06")

        self.assertEqual(compared.iloc[0]["status"], "new")
        self.assertEqual(compared.iloc[0]["last_seen_date"], "2026-06-06")

    def test_compare_with_history_marks_unchanged_records_already_seen(self):
        current = sample_current_opportunity()
        history = current.copy()
        history["status"] = "new"
        history["last_seen_date"] = "2026-06-03"

        compared = compare_with_history(current, history, run_date="2026-06-06")

        self.assertEqual(compared.iloc[0]["status"], "already_seen")
        self.assertEqual(compared.iloc[0]["first_seen_date"], "2026-06-03")

    def test_compare_with_history_marks_changed_records_updated(self):
        current = sample_current_opportunity("Updated ML work.")
        history = sample_current_opportunity("Old ML work.")
        history["status"] = "new"
        history["last_seen_date"] = "2026-06-03"

        compared = compare_with_history(current, history, run_date="2026-06-06")

        self.assertEqual(compared.iloc[0]["status"], "updated")


if __name__ == "__main__":
    unittest.main()

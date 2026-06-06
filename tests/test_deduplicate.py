import unittest

import pandas as pd

from src.processing.deduplicate import (
    deduplicate_opportunities,
    make_content_hash,
    make_identity_key,
)


class DeduplicateTests(unittest.TestCase):
    def test_make_identity_key_prefers_url(self):
        row = pd.Series(
            {
                "title": "AI Internship",
                "organization": "Global AI Lab",
                "url": "https://example.com/apply",
            }
        )

        self.assertEqual(make_identity_key(row), "url::https://example.com/apply")

    def test_make_identity_key_falls_back_to_title_and_organization(self):
        row = pd.Series(
            {
                "title": "AI Internship",
                "organization": "Global AI Lab",
                "url": "",
            }
        )

        self.assertEqual(
            make_identity_key(row),
            "title_org::ai internship::global ai lab",
        )

    def test_make_content_hash_changes_when_content_changes(self):
        row = pd.Series(
            {
                "title": "AI Internship",
                "organization": "Global AI Lab",
                "description": "Original description",
            }
        )
        changed_row = row.copy()
        changed_row["description"] = "Updated description"

        self.assertNotEqual(make_content_hash(row), make_content_hash(changed_row))

    def test_deduplicate_opportunities_keeps_one_record_per_identity_key(self):
        dataframe = pd.DataFrame(
            [
                {
                    "id": "opp-001",
                    "title": "AI Internship",
                    "organization": "Global AI Lab",
                    "description": "First record",
                    "category": "internship",
                    "location": "Remote",
                    "remote_or_onsite": "remote",
                    "deadline": "2026-07-15",
                    "url": "https://example.com/apply",
                    "required_skills": "python",
                    "difficulty": "intermediate",
                },
                {
                    "id": "opp-002",
                    "title": "AI Internship duplicate",
                    "organization": "Global AI Lab",
                    "description": "Duplicate record",
                    "category": "internship",
                    "location": "Remote",
                    "remote_or_onsite": "remote",
                    "deadline": "2026-07-15",
                    "url": "https://example.com/apply",
                    "required_skills": "python",
                    "difficulty": "intermediate",
                },
            ]
        )

        deduplicated = deduplicate_opportunities(dataframe)

        self.assertEqual(len(deduplicated), 1)
        self.assertEqual(deduplicated.iloc[0]["duplicate_count"], 2)


if __name__ == "__main__":
    unittest.main()

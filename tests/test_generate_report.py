import unittest
from pathlib import Path

import pandas as pd

from src.reports.generate_report import (
    generate_html_report,
    generate_markdown_report,
    save_daily_reports,
    select_top_opportunities,
    summarize_opportunities,
)


def sample_report_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "title": "AI Internship",
                "predicted_category": "internship",
                "match_score": 90,
                "priority_level": "high",
                "deadline": "2026-06-20",
                "status": "new",
                "url": "https://example.com/ai-internship",
                "is_urgent": True,
                "high_match": True,
                "match_reasons": "Strong AI and Python match",
                "urgency_reasons": "Deadline is soon",
                "category_reason": "Matched internship keywords",
            },
            {
                "title": "General Course",
                "predicted_category": "online_course",
                "match_score": 40,
                "priority_level": "low",
                "deadline": "2026-09-01",
                "status": "already_seen",
                "url": "https://example.com/course",
                "is_urgent": False,
                "high_match": False,
                "match_reasons": "Some skill overlap",
                "urgency_reasons": "",
                "category_reason": "Matched course keywords",
            },
        ]
    )


class GenerateReportTests(unittest.TestCase):
    def test_summarize_opportunities_counts_key_values(self):
        summary = summarize_opportunities(sample_report_dataframe())

        self.assertEqual(summary["total_opportunities"], 2)
        self.assertEqual(summary["new_opportunities"], 1)
        self.assertEqual(summary["urgent_opportunities"], 1)
        self.assertEqual(summary["high_match_opportunities"], 1)

    def test_select_top_opportunities_prioritizes_urgent_and_high_score(self):
        top = select_top_opportunities(sample_report_dataframe(), top_n=1)

        self.assertEqual(top.iloc[0]["title"], "AI Internship")

    def test_generate_markdown_report_contains_summary_and_top_item(self):
        report = generate_markdown_report(
            sample_report_dataframe(),
            report_date="2026-06-14",
        )

        self.assertIn("AI Opportunity Radar Daily Report - 2026-06-14", report)
        self.assertIn("Total opportunities scanned: 2", report)
        self.assertIn("AI Internship", report)

    def test_generate_html_report_contains_html_and_escaped_content(self):
        report = generate_html_report(
            sample_report_dataframe(),
            report_date="2026-06-14",
        )

        self.assertIn("<html", report)
        self.assertIn("AI Internship", report)
        self.assertIn("Top Recommended Opportunities", report)

    def test_save_daily_reports_creates_markdown_and_html_files(self):
        output_dir = Path("reports/daily/test_reports")

        markdown_path, html_path = save_daily_reports(
            sample_report_dataframe(),
            output_dir=output_dir,
            report_date="2026-06-14",
        )

        self.assertTrue(markdown_path.exists())
        self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()

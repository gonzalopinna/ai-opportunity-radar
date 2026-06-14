from datetime import date
from html import escape
from pathlib import Path

import pandas as pd

from src.config import DAILY_REPORTS_DIR
from src.processing.clean_text import clean_text


def get_report_date(report_date: str | None = None) -> str:
    """Return the report date as an ISO date string."""
    return report_date or date.today().isoformat()


def count_true_values(dataframe: pd.DataFrame, column: str) -> int:
    """Count true boolean values in a dataframe column."""
    if column not in dataframe.columns:
        return 0

    return int(dataframe[column].fillna(False).astype(bool).sum())


def summarize_opportunities(dataframe: pd.DataFrame) -> dict:
    """Build a compact summary for the daily report."""
    status_counts = dataframe.get("status", pd.Series(dtype=str)).value_counts()

    return {
        "total_opportunities": int(len(dataframe)),
        "new_opportunities": int(status_counts.get("new", 0)),
        "updated_opportunities": int(status_counts.get("updated", 0)),
        "urgent_opportunities": count_true_values(dataframe, "is_urgent"),
        "high_match_opportunities": count_true_values(dataframe, "high_match"),
        "average_match_score": round(
            float(dataframe.get("match_score", pd.Series(dtype=float)).mean() or 0),
            1,
        ),
    }


def select_top_opportunities(dataframe: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Select the strongest opportunities for the report."""
    if dataframe.empty:
        return dataframe.copy()

    sort_columns = ["is_urgent", "match_score", "deadline"]
    available_sort_columns = [column for column in sort_columns if column in dataframe]
    ascending = [False if column != "deadline" else True for column in available_sort_columns]

    return dataframe.sort_values(
        by=available_sort_columns,
        ascending=ascending,
    ).head(top_n)


def format_markdown_table(top_opportunities: pd.DataFrame) -> str:
    """Format top opportunities as a Markdown table."""
    lines = [
        "| Rank | Title | Category | Score | Priority | Deadline | Status | Link |",
        "| --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]

    for rank, (_, row) in enumerate(top_opportunities.iterrows(), start=1):
        title = clean_text(row.get("title", "Untitled"))
        category = clean_text(row.get("predicted_category", row.get("category", "")))
        score = row.get("match_score", "")
        priority = clean_text(row.get("priority_level", ""))
        deadline = clean_text(row.get("deadline", ""))
        status = clean_text(row.get("status", ""))
        url = clean_text(row.get("url", ""))
        link = f"[Apply]({url})" if url else ""
        lines.append(
            f"| {rank} | {title} | {category} | {score} | "
            f"{priority} | {deadline} | {status} | {link} |"
        )

    return "\n".join(lines)


def format_recommendation_reasons(top_opportunities: pd.DataFrame) -> str:
    """Create a Markdown list with recommendation reasons."""
    lines = []

    for rank, (_, row) in enumerate(top_opportunities.iterrows(), start=1):
        title = clean_text(row.get("title", "Untitled"))
        match_reasons = clean_text(row.get("match_reasons", ""))
        urgency_reasons = clean_text(row.get("urgency_reasons", ""))
        category_reason = clean_text(row.get("category_reason", ""))

        lines.append(f"{rank}. **{title}**")
        if match_reasons:
            lines.append(f"   - Match: {match_reasons}")
        if urgency_reasons:
            lines.append(f"   - Priority: {urgency_reasons}")
        if category_reason:
            lines.append(f"   - Category: {category_reason}")

    return "\n".join(lines)


def generate_markdown_report(
    dataframe: pd.DataFrame,
    report_date: str | None = None,
    top_n: int = 10,
) -> str:
    """Generate a Markdown daily opportunity report."""
    current_date = get_report_date(report_date)
    summary = summarize_opportunities(dataframe)
    top_opportunities = select_top_opportunities(dataframe, top_n=top_n)

    return "\n\n".join(
        [
            f"# AI Opportunity Radar Daily Report - {current_date}",
            "## Summary",
            "\n".join(
                [
                    f"- Total opportunities scanned: {summary['total_opportunities']}",
                    f"- New opportunities: {summary['new_opportunities']}",
                    f"- Updated opportunities: {summary['updated_opportunities']}",
                    f"- Urgent opportunities: {summary['urgent_opportunities']}",
                    f"- High-match opportunities: {summary['high_match_opportunities']}",
                    f"- Average match score: {summary['average_match_score']}",
                ]
            ),
            "## Top Recommended Opportunities",
            format_markdown_table(top_opportunities),
            "## Recommendation Reasons",
            format_recommendation_reasons(top_opportunities),
        ]
    )


def generate_html_report(
    dataframe: pd.DataFrame,
    report_date: str | None = None,
    top_n: int = 10,
) -> str:
    """Generate an HTML daily opportunity report."""
    current_date = get_report_date(report_date)
    summary = summarize_opportunities(dataframe)
    top_opportunities = select_top_opportunities(dataframe, top_n=top_n)

    table_rows = []
    reason_items = []

    for rank, (_, row) in enumerate(top_opportunities.iterrows(), start=1):
        title = clean_text(row.get("title", "Untitled"))
        category = clean_text(row.get("predicted_category", row.get("category", "")))
        score = clean_text(row.get("match_score", ""))
        priority = clean_text(row.get("priority_level", ""))
        deadline = clean_text(row.get("deadline", ""))
        status = clean_text(row.get("status", ""))
        url = clean_text(row.get("url", ""))
        link = f'<a href="{escape(url)}">Apply</a>' if url else ""

        table_rows.append(
            "<tr>"
            f"<td>{rank}</td>"
            f"<td>{escape(title)}</td>"
            f"<td>{escape(category)}</td>"
            f"<td>{escape(score)}</td>"
            f"<td>{escape(priority)}</td>"
            f"<td>{escape(deadline)}</td>"
            f"<td>{escape(status)}</td>"
            f"<td>{link}</td>"
            "</tr>"
        )

        reasons = " | ".join(
            clean_text(row.get(column, ""))
            for column in ["match_reasons", "urgency_reasons", "category_reason"]
            if clean_text(row.get(column, ""))
        )
        reason_items.append(
            f"<li><strong>{escape(title)}</strong><br>{escape(reasons)}</li>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Opportunity Radar Daily Report - {escape(current_date)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; color: #1f2933; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #d9e2ec; padding: 0.5rem; text-align: left; }}
    th {{ background: #f0f4f8; }}
    .summary {{ background: #f8fafc; padding: 1rem; border: 1px solid #d9e2ec; }}
  </style>
</head>
<body>
  <h1>AI Opportunity Radar Daily Report - {escape(current_date)}</h1>
  <section class="summary">
    <h2>Summary</h2>
    <ul>
      <li>Total opportunities scanned: {summary['total_opportunities']}</li>
      <li>New opportunities: {summary['new_opportunities']}</li>
      <li>Updated opportunities: {summary['updated_opportunities']}</li>
      <li>Urgent opportunities: {summary['urgent_opportunities']}</li>
      <li>High-match opportunities: {summary['high_match_opportunities']}</li>
      <li>Average match score: {summary['average_match_score']}</li>
    </ul>
  </section>
  <h2>Top Recommended Opportunities</h2>
  <table>
    <thead>
      <tr>
        <th>Rank</th><th>Title</th><th>Category</th><th>Score</th>
        <th>Priority</th><th>Deadline</th><th>Status</th><th>Link</th>
      </tr>
    </thead>
    <tbody>
      {''.join(table_rows)}
    </tbody>
  </table>
  <h2>Recommendation Reasons</h2>
  <ol>
    {''.join(reason_items)}
  </ol>
</body>
</html>
"""


def save_daily_reports(
    dataframe: pd.DataFrame,
    output_dir: Path = DAILY_REPORTS_DIR,
    report_date: str | None = None,
) -> tuple[Path, Path]:
    """Save Markdown and HTML daily reports."""
    current_date = get_report_date(report_date)
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / f"opportunity_report_{current_date}.md"
    html_path = output_dir / f"opportunity_report_{current_date}.html"

    markdown_path.write_text(
        generate_markdown_report(dataframe, report_date=current_date),
        encoding="utf-8",
    )
    html_path.write_text(
        generate_html_report(dataframe, report_date=current_date),
        encoding="utf-8",
    )

    return markdown_path, html_path

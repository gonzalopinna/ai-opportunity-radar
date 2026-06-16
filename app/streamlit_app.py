from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "opportunities_processed.csv"
REPORTS_DIR = PROJECT_ROOT / "reports" / "daily"

DISPLAY_COLUMNS = [
    "title",
    "organization",
    "predicted_category",
    "remote_or_onsite",
    "deadline",
    "status",
    "priority_level",
    "match_score",
    "is_urgent",
    "high_match",
    "cluster_label",
    "url",
]


@st.cache_data
def load_opportunities(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load processed opportunity data for the dashboard."""
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def filter_opportunities(
    dataframe: pd.DataFrame,
    categories: list[str],
    statuses: list[str],
    priorities: list[str],
    remote_statuses: list[str],
    min_score: int,
    urgent_only: bool,
) -> pd.DataFrame:
    """Apply dashboard filters to the processed opportunities."""
    filtered = dataframe.copy()

    if categories:
        filtered = filtered[filtered["predicted_category"].isin(categories)]

    if statuses:
        filtered = filtered[filtered["status"].isin(statuses)]

    if priorities:
        filtered = filtered[filtered["priority_level"].isin(priorities)]

    if remote_statuses:
        filtered = filtered[filtered["remote_or_onsite"].isin(remote_statuses)]

    filtered = filtered[filtered["match_score"] >= min_score]

    if urgent_only:
        filtered = filtered[filtered["is_urgent"].astype(bool)]

    return filtered.sort_values(
        by=["is_urgent", "match_score", "deadline"],
        ascending=[False, False, True],
    )


def latest_report_links() -> list[Path]:
    """Return generated report files ordered by latest first."""
    if not REPORTS_DIR.exists():
        return []

    return sorted(REPORTS_DIR.glob("opportunity_report_*.*"), reverse=True)


def render_sidebar_filters(dataframe: pd.DataFrame) -> tuple:
    """Render Streamlit sidebar filters."""
    st.sidebar.header("Filters")

    categories = st.sidebar.multiselect(
        "Category",
        sorted(dataframe["predicted_category"].dropna().unique()),
    )
    statuses = st.sidebar.multiselect(
        "Status",
        sorted(dataframe["status"].dropna().unique()),
    )
    priorities = st.sidebar.multiselect(
        "Priority",
        sorted(dataframe["priority_level"].dropna().unique()),
    )
    remote_statuses = st.sidebar.multiselect(
        "Mode",
        sorted(dataframe["remote_or_onsite"].dropna().unique()),
    )
    min_score = st.sidebar.slider("Minimum match score", 0, 100, 0, 5)
    urgent_only = st.sidebar.checkbox("Urgent only")

    return categories, statuses, priorities, remote_statuses, min_score, urgent_only


def render_metrics(dataframe: pd.DataFrame) -> None:
    """Render top-level dashboard metrics."""
    total = len(dataframe)
    urgent = int(dataframe["is_urgent"].fillna(False).astype(bool).sum())
    high_match = int(dataframe["high_match"].fillna(False).astype(bool).sum())
    average_score = round(float(dataframe["match_score"].mean()), 1) if total else 0

    col_total, col_urgent, col_high_match, col_score = st.columns(4)
    col_total.metric("Opportunities", total)
    col_urgent.metric("Urgent", urgent)
    col_high_match.metric("High match", high_match)
    col_score.metric("Avg score", average_score)


def render_opportunity_detail(row: pd.Series) -> None:
    """Render a selected opportunity detail view."""
    st.subheader(row["title"])

    col_score, col_category, col_priority = st.columns(3)
    col_score.metric("Match score", int(row["match_score"]))
    col_category.metric("Category", row["predicted_category"])
    col_priority.metric("Priority", row["priority_level"])

    st.write(row.get("description", ""))
    st.markdown(f"**Organization:** {row.get('organization', '')}")
    st.markdown(f"**Deadline:** {row.get('deadline', '')}")
    st.markdown(f"**Mode:** {row.get('remote_or_onsite', '')}")
    st.markdown(f"**Cluster:** {row.get('cluster_label', '')}")
    st.markdown(f"**Match reasons:** {row.get('match_reasons', '')}")
    st.markdown(f"**Priority reasons:** {row.get('urgency_reasons', '')}")

    url = row.get("url", "")
    if isinstance(url, str) and url:
        st.link_button("Apply", url)


def main() -> None:
    st.set_page_config(
        page_title="AI Opportunity Radar",
        page_icon="",
        layout="wide",
    )
    st.title("AI Opportunity Radar")

    opportunities = load_opportunities()
    if opportunities.empty:
        st.warning("No processed opportunities found.")
        st.code("python -m src.main")
        return

    filters = render_sidebar_filters(opportunities)
    filtered = filter_opportunities(opportunities, *filters)

    render_metrics(filtered)

    ranking_tab, urgent_tab, clusters_tab, detail_tab, reports_tab = st.tabs(
        ["Ranking", "Urgent", "Clusters", "Details", "Reports"]
    )

    with ranking_tab:
        st.dataframe(
            filtered[[column for column in DISPLAY_COLUMNS if column in filtered]],
            use_container_width=True,
            hide_index=True,
        )

    with urgent_tab:
        urgent = filtered[filtered["is_urgent"].astype(bool)]
        st.dataframe(
            urgent[[column for column in DISPLAY_COLUMNS if column in urgent]],
            use_container_width=True,
            hide_index=True,
        )

    with clusters_tab:
        cluster_counts = (
            filtered["cluster_label"]
            .value_counts()
            .reset_index()
            .rename(columns={"cluster_label": "cluster", "count": "opportunities"})
        )
        st.dataframe(cluster_counts, use_container_width=True, hide_index=True)

    with detail_tab:
        titles = filtered["title"].tolist()
        if titles:
            selected_title = st.selectbox("Opportunity", titles)
            selected_row = filtered[filtered["title"] == selected_title].iloc[0]
            render_opportunity_detail(selected_row)
        else:
            st.info("No opportunities match the selected filters.")

    with reports_tab:
        reports = latest_report_links()
        if reports:
            for report_path in reports[:10]:
                st.markdown(f"- `{report_path.name}`")
        else:
            st.info("No reports generated yet.")


if __name__ == "__main__":
    main()

# AI Opportunity Radar

A daily AI-powered opportunity tracker and recommender for Computer Science students.

AI Opportunity Radar is a machine learning-powered tool that helps Computer Science students discover and prioritize relevant academic and professional opportunities. The system will collect opportunities, classify them, compute a personalized match score, detect urgent deadlines, and generate a daily report with the best opportunities.

## Problem Statement

Computer Science students often need to monitor many sources to find internships, scholarships, hackathons, research programs, startup roles, graduate programs, online courses, and competitions. Important opportunities can be missed because deadlines are scattered across different platforms and the relevance of each opportunity is not always obvious.

This project aims to turn that manual search into a repeatable daily pipeline that can organize, compare, rank, and report opportunities for a student profile focused on AI, machine learning, Python, software engineering, startups, research, hackathons, and international opportunities.

## Why This Project Matters

This project is designed as a practical portfolio project. It shows how machine learning and software engineering concepts can be applied to a real product idea instead of only to isolated notebooks or course exercises.

## Planned Features

- Load opportunities from configured sources or sample datasets.
- Clean and normalize opportunity data.
- Store opportunities in a structured format.
- Compare current opportunities with previous runs.
- Detect new, repeated, updated, urgent, and high-match opportunities.
- Classify opportunities by type.
- Score opportunities against a Computer Science student profile.
- Generate daily Markdown and HTML reports.
- Optionally send reports by email.
- Provide a Streamlit dashboard in a later sprint.
- Run daily through GitHub Actions in a later sprint.

## Tech Stack

- Python
- pandas
- numpy
- scikit-learn
- matplotlib or plotly, if needed later
- Streamlit, planned for the dashboard
- CSV, JSON, SQLite, or another lightweight storage option for early versions
- python-dotenv for environment variables
- smtplib or another safe email method for optional email reports
- GitHub Actions for scheduled execution in a later sprint

## ML Concepts Planned

- Data preprocessing
- Feature engineering
- Text cleaning
- Classification
- Logistic Regression
- Decision Trees
- Random Forest or Gradient Boosting, if useful
- K-Means clustering
- Anomaly or urgency detection
- Content-based recommendation
- Model evaluation with accuracy, precision, recall, and F1-score
- Train/test split where appropriate

## Project Architecture

```text
AI Opportunity Radar/
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── notebooks/
├── src/
│   ├── collectors/
│   ├── processing/
│   ├── ml/
│   ├── storage/
│   ├── reports/
│   ├── config.py
│   └── main.py
├── app/
├── tests/
├── reports/
│   └── daily/
├── README.md
├── DEVELOPMENT_LOG.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Current Sprint

Sprint 1 initializes the repository structure, documentation, environment templates, and a small sample dataset. The current pipeline is intentionally a placeholder and does not implement machine learning, email, dashboard, or automation yet.

## How To Run Locally

1. Create and activate a virtual environment:

```bash
python -m venv .venv
```

2. Activate it.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the placeholder pipeline:

```bash
python -m src.main
```

The pipeline currently loads `data/sample/opportunities_sample.csv` and prints a short summary.

## Email Configuration

Email is planned for a later sprint and is not implemented yet. When implemented, credentials must be provided through environment variables, never hardcoded in the codebase.

Copy `.env.example` to `.env` and fill in real values only on your local machine:

```text
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_TO=
```

If Gmail is used later, use a Gmail App Password instead of the normal account password.

## Example Daily Report

Report generation is planned for a later sprint. Future reports will include:

- Total opportunities scanned
- New opportunities
- High-match opportunities
- Urgent deadlines
- Top recommended opportunities
- Reasons for recommendation
- Links to apply

## Limitations

- The current version only contains project scaffolding and a sample CSV.
- No machine learning models are implemented yet.
- No historical comparison is implemented yet.
- No report generation, email sending, dashboard, or scheduled workflow is implemented yet.

## Future Work

- Implement data loading, cleaning, and normalization.
- Add deduplication and historical comparison.
- Build baseline relevance scoring.
- Add classification, clustering, and urgency detection.
- Generate Markdown and HTML reports.
- Add optional email delivery.
- Build a Streamlit dashboard.
- Add a scheduled GitHub Actions workflow.

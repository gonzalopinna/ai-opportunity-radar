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
- Provide a Streamlit dashboard in a later development stage.
- Run daily through GitHub Actions in a later development stage.

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
- GitHub Actions for scheduled execution in a later development stage

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

## Current Capabilities

The current pipeline includes baseline category classification, classification evaluation, K-Means clustering, relevance scoring, urgency detection, daily report generation, optional email delivery, a Streamlit dashboard, and scheduled automation with GitHub Actions. It loads and preprocesses the sample opportunities, removes duplicate records, compares the current results with history, predicts an opportunity type, evaluates predictions against the labeled sample data, groups similar opportunities, scores each opportunity against a Computer Science student profile, detects urgent or unusual signals, saves ranked results plus Markdown and HTML reports, can email the HTML report when credentials are configured, provides an interactive dashboard for reviewing results, and can run automatically on GitHub.

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

4. Run the data pipeline:

```bash
python -m src.main
```

The pipeline loads `data/sample/opportunities_sample.csv`, cleans and normalizes the data, removes current-run duplicates, compares results with the local opportunity history, adds baseline category predictions, evaluates those predictions, groups similar opportunities with K-Means, adds relevance scores, detects urgent or unusual opportunities, generates daily reports, optionally sends the HTML report by email, and saves:

- `data/processed/opportunities_processed.csv`
- `data/processed/opportunities_history.csv`
- `data/processed/classification_evaluation.json`
- `reports/daily/opportunity_report_YYYY-MM-DD.md`
- `reports/daily/opportunity_report_YYYY-MM-DD.html`

The processed dataset includes `predicted_category`, `category_confidence`, `category_reason`, `cluster_id`, `cluster_label`, `cluster_keywords`, `match_score` from 0 to 100, `match_reasons`, `is_urgent`, `high_match`, `urgency_score`, `priority_level`, `anomaly_flags`, and `urgency_reasons`.

5. Run tests:

```bash
python -m unittest
```

6. Open the dashboard:

```bash
streamlit run app/streamlit_app.py
```

## Automation

The GitHub Actions workflow in `.github/workflows/daily_radar.yml` can run the project automatically every day or manually from the Actions tab. It installs dependencies, runs tests, executes the pipeline, and uploads generated reports and processed data as workflow artifacts.

Email delivery remains optional in GitHub Actions. Add these repository secrets only if you want the workflow to send email:

```text
EMAIL_HOST
EMAIL_PORT
EMAIL_USER
EMAIL_PASSWORD
EMAIL_TO
```

## Email Configuration

Email delivery is optional. If email environment variables are missing, the pipeline skips email sending and still completes successfully. Credentials must be provided through environment variables, never hardcoded in the codebase.

Copy `.env.example` to `.env` and fill in real values only on your local machine:

```text
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_TO=
```

For Gmail, use an App Password instead of the normal account password.

## Example Daily Report

Generated daily reports include:

- Total opportunities scanned
- New opportunities
- Updated opportunities
- High-match opportunities
- Urgent deadlines
- Top recommended opportunities
- Reasons for recommendation
- Links to apply

## Limitations

- The current version uses a simple CSV-based history file.
- Category classification is a transparent keyword baseline because the sample dataset is still small.
- Classification evaluation currently uses the labeled sample dataset, not a train/test split.
- Clustering uses a small deterministic K-Means implementation for educational clarity.
- Relevance scoring is a transparent rule-based baseline, not a trained model.
- Urgency detection is rule-based and should be tuned with more real opportunity data.
- Email sending is optional and depends on local environment variables.
- The dashboard reads the generated processed CSV and does not yet write back changes.
- No machine learning models are implemented yet.
- The automated workflow currently uses the sample dataset.

## Future Work

- Add more real opportunity sources.

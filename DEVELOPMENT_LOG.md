# Development Log

This file tracks meaningful development steps for AI Opportunity Radar. Each entry is written so the project can be reviewed later and explained clearly in interviews.

## 2026-06-03 - Project Initialization

### What Was Implemented

- Created the initial repository folder structure.
- Added project documentation in `README.md`.
- Added `requirements.txt` with the initial planned dependencies.
- Added `.gitignore` for Python, environment, notebook, data, and report artifacts.
- Added `.env.example` with placeholder email environment variables.
- Added a sample opportunity dataset at `data/sample/opportunities_sample.csv`.
- Added `src/main.py` with a simple placeholder pipeline that loads the sample dataset and prints a summary.
- Added package folders for collectors, processing, machine learning, storage, and reports.

### Why It Was Implemented

This update establishes a clean, readable foundation for the project. The goal is to make the repository understandable before adding data processing, machine learning, reporting, email, dashboard, or automation features.

### Related ML or Software Concept

- Project structure
- Reproducible development setup
- Dataset schema design
- Pipeline planning
- Portfolio-ready documentation

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `requirements.txt`
- `.gitignore`
- `.env.example`
- `data/sample/opportunities_sample.csv`
- `src/main.py`
- `src/config.py`
- `src/collectors/__init__.py`
- `src/processing/__init__.py`
- `src/ml/__init__.py`
- `src/storage/__init__.py`
- `src/reports/__init__.py`
- `.gitkeep` files for planned folders

### How To Test It

Install dependencies and run:

```bash
python -m src.main
```

Expected behavior:

- The command loads `data/sample/opportunities_sample.csv`.
- It prints the number of opportunities in the sample dataset.
- It prints counts by category.
- It exits without requiring email credentials or external services.

### Suggested Commit Message

```text
Initialize project scaffold
```

## 2026-06-04 - Data Loading, Cleaning, and Normalization

### What Was Implemented

- Added a preprocessing pipeline for the sample opportunities dataset.
- Added validation for required dataset columns.
- Added text cleaning for title, organization, description, and location.
- Added category normalization into supported project labels.
- Added remote, onsite, hybrid, and unknown normalization.
- Added safe deadline parsing.
- Added required skills normalization into a consistent semicolon-separated format.
- Added difficulty normalization when the column exists.
- Updated `src/main.py` so `python -m src.main` runs the preprocessing pipeline.
- Added unit tests for normalization and preprocessing behavior.
- Updated the README with the preprocessing run and test commands.

### Why It Was Implemented

This update turns the placeholder pipeline into a real data preparation step. Clean and consistent input data is necessary before adding deduplication, historical comparison, scoring, classification, clustering, reports, or dashboard features.

### Related ML or Software Concept

- Data loading
- Data validation
- Text cleaning
- Data preprocessing
- Feature preparation
- Reproducible pipeline design

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/processing/clean_text.py`
- `src/processing/normalize.py`
- `src/processing/deadline_parser.py`
- `src/processing/preprocess_dataset.py`
- `tests/__init__.py`
- `tests/test_preprocess_dataset.py`

### How To Test It

Run the preprocessing pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command loads `data/sample/opportunities_sample.csv`.
- It validates that required columns are present.
- It cleans and normalizes the dataset.
- It saves `data/processed/opportunities_processed.csv`.
- It prints the number of processed opportunities.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add preprocessing pipeline
```

## 2026-06-06 - Deduplication and Historical Comparison

### What Was Implemented

- Added stable opportunity identity keys based on URL when available, with title and organization as a fallback.
- Added content hashes for fields that should mark an opportunity as updated.
- Added current-run deduplication that keeps the first record for each identity key.
- Added CSV-based historical comparison using `data/processed/opportunities_history.csv`.
- Added opportunity status labels for the current run: `new`, `already_seen`, and `updated`.
- Updated `src/main.py` to run preprocessing, deduplication, history comparison, and saving through one command.
- Updated the README to describe the deduplication and history outputs.
- Added tests for deduplication and historical comparison behavior.

### Why It Was Implemented

This update adds memory to the project. The system can now tell whether an opportunity is new, unchanged from a previous run, or changed since it was last seen. This is a necessary foundation before ranking, urgency detection, reporting, and dashboard features.

### Related ML or Software Concept

- Data deduplication
- Entity identity design
- Historical comparison
- Change detection
- Reproducible data pipelines

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/processing/deduplicate.py`
- `src/storage/history.py`
- `tests/test_deduplicate.py`
- `tests/test_history.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It removes duplicate opportunities from the current run.
- It compares the current opportunities with `data/processed/opportunities_history.csv`.
- It saves `data/processed/opportunities_processed.csv`.
- It saves or updates `data/processed/opportunities_history.csv`.
- It prints the number of processed opportunities, removed duplicates, and status counts.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add deduplication and history comparison
```

## 2026-06-08 - Baseline Relevance Scoring

### What Was Implemented

- Added a transparent rule-based student profile for a Computer Science student interested in AI, machine learning, Python, software engineering, startups, research, hackathons, international opportunities, and quant as a secondary interest.
- Added baseline relevance scoring from 0 to 100.
- Added scoring signals for profile interest match, skill overlap, category preference, difficulty fit, remote or hybrid fit, deadline timing, and explicit AI/ML relevance.
- Added `match_score` and `match_reasons` columns to the processed dataset.
- Updated `src/main.py` to run scoring after preprocessing, deduplication, and history comparison.
- Updated the README to describe the scoring output.
- Added tests for skill parsing, deadline scoring, opportunity scoring, and score-based sorting.

### Why It Was Implemented

This update turns the pipeline into a simple recommender baseline. The scoring logic is intentionally readable and explainable so it can be discussed clearly before introducing trained models or more advanced recommendation techniques.

### Related ML or Software Concept

- Feature engineering
- Content-based recommendation
- Rule-based baseline model
- Ranking
- Explainable scoring

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/ml/score_relevance.py`
- `tests/test_score_relevance.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It removes duplicate opportunities from the current run.
- It compares opportunities with history.
- It adds `match_score` and `match_reasons`.
- It saves `data/processed/opportunities_processed.csv`.
- It prints the top match and its score.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add baseline relevance scoring
```

## 2026-06-09 - Baseline Opportunity Classification

### What Was Implemented

- Added a transparent keyword-based opportunity classifier.
- Added supported categories for internship, scholarship, hackathon, research, startup, graduate program, online course, competition, and other.
- Added `predicted_category`, `category_confidence`, and `category_reason` columns to the processed dataset.
- Updated `src/main.py` to classify opportunities before relevance scoring.
- Updated the README to describe classification outputs.
- Removed remaining project-file references to internal development phase labels.
- Added tests for category prediction and classification output columns.

### Why It Was Implemented

The dataset is still too small for a trained classifier to be meaningful. A readable keyword baseline gives the project a working classification layer now and creates a clear comparison point for future model-based classification and evaluation.

### Related ML or Software Concept

- Text feature extraction
- Rule-based classification baseline
- Label prediction
- Explainable classification
- Data pipeline composition

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/ml/classify_opportunities.py`
- `tests/test_classify_opportunities.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It removes duplicate opportunities from the current run.
- It compares opportunities with history.
- It adds `predicted_category`, `category_confidence`, and `category_reason`.
- It adds `match_score` and `match_reasons`.
- It saves `data/processed/opportunities_processed.csv`.
- It prints predicted category counts.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add baseline opportunity classification
```

## 2026-06-10 - Classification Evaluation

### What Was Implemented

- Added classification evaluation for the baseline opportunity classifier.
- Added accuracy, macro precision, macro recall, macro F1, weighted precision, weighted recall, and weighted F1 metrics.
- Added per-category precision, recall, F1, and support.
- Added JSON export for evaluation results at `data/processed/classification_evaluation.json`.
- Updated `src/main.py` to run evaluation after classification and before relevance scoring.
- Updated the README to document the evaluation output.
- Added tests for metric calculation, required columns, and JSON export.

### Why It Was Implemented

Evaluation makes the classifier measurable instead of just functional. Because the dataset is still small, this update evaluates the transparent baseline against the labeled sample data rather than using a train/test split that would be too noisy to interpret.

### Related ML or Software Concept

- Model evaluation
- Accuracy
- Precision
- Recall
- F1-score
- Per-class metrics

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/ml/evaluate_classification.py`
- `tests/test_evaluate_classification.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It classifies opportunities with the baseline classifier.
- It evaluates predictions against the labeled sample categories.
- It saves `data/processed/classification_evaluation.json`.
- It prints accuracy and macro F1.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add classification evaluation metrics
```

## 2026-06-12 - Opportunity Clustering

### What Was Implemented

- Added a simple K-Means clustering module for grouping similar opportunities.
- Added lightweight text tokenization and bag-of-words vectorization.
- Added deterministic centroid initialization for reproducible clustering.
- Added readable cluster descriptions based on the strongest terms in each cluster.
- Added `cluster_id`, `cluster_label`, and `cluster_keywords` columns to the processed dataset.
- Updated `src/main.py` to run clustering before relevance scoring.
- Updated the README to describe the clustering output.
- Added tests for tokenization, vectorization, K-Means labels, and output columns.

### Why It Was Implemented

Clustering helps users inspect groups of similar opportunities instead of only reading a ranked list. The implementation is intentionally small and deterministic so the concept is easy to understand before introducing more advanced vectorization or external ML utilities.

### Related ML or Software Concept

- K-Means clustering
- Bag-of-words features
- Unsupervised learning
- Similarity grouping
- Feature extraction from text

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/ml/cluster_opportunities.py`
- `tests/test_cluster_opportunities.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It classifies and evaluates opportunities.
- It groups opportunities into clusters.
- It adds `cluster_id`, `cluster_label`, and `cluster_keywords`.
- It saves `data/processed/opportunities_processed.csv`.
- It prints cluster counts.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add opportunity clustering
```

## 2026-06-13 - Urgency and Anomaly Detection

### What Was Implemented

- Added rule-based urgency and anomaly detection.
- Added deadline-based signals for soon and approaching deadlines.
- Added high-match detection based on relevance score.
- Added rare-category detection within the current run.
- Added new or updated high-value organization detection.
- Added `is_urgent`, `high_match`, `urgency_score`, `priority_level`, `anomaly_flags`, and `urgency_reasons` columns.
- Updated `src/main.py` to run urgency detection after relevance scoring.
- Updated the README to describe priority and urgency outputs.
- Added tests for deadline distance, high-value organizations, urgency flags, high-match flags, and output columns.

### Why It Was Implemented

The system should help a student notice opportunities that deserve immediate attention. This update adds simple, explainable priority signals before building reports, email delivery, or a dashboard.

### Related ML or Software Concept

- Rule-based anomaly detection
- Urgency detection
- Feature thresholds
- Priority scoring
- Explainable alerts

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/ml/detect_anomalies.py`
- `tests/test_detect_anomalies.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command preprocesses the sample dataset.
- It classifies, evaluates, clusters, and scores opportunities.
- It adds urgency and anomaly columns.
- It saves `data/processed/opportunities_processed.csv`.
- It prints urgent and high-match opportunity counts.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add urgency and anomaly detection
```

## 2026-06-14 - Daily Report Generation

### What Was Implemented

- Added Markdown and HTML report generation.
- Added summary metrics for total, new, updated, urgent, and high-match opportunities.
- Added a top recommended opportunities table.
- Added recommendation reasons using match, urgency, and category explanations.
- Added report saving to `reports/daily/opportunity_report_YYYY-MM-DD.md`.
- Added report saving to `reports/daily/opportunity_report_YYYY-MM-DD.html`.
- Updated `src/main.py` to generate reports after the processed dataset is saved.
- Updated the README to document the report outputs.
- Added tests for summaries, top opportunity selection, Markdown generation, HTML generation, and report file creation.

### Why It Was Implemented

Reports turn the pipeline output into something a student can review quickly. Markdown is useful for GitHub and local inspection, while HTML prepares the project for future email delivery and dashboard-adjacent presentation.

### Related ML or Software Concept

- Recommendation presentation
- Ranking output
- Explainability
- Automated reporting
- Product-oriented pipeline output

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/reports/generate_report.py`
- `tests/test_generate_report.py`

### How To Test It

Run the data pipeline:

```bash
python -m src.main
```

Expected behavior:

- The command processes and ranks opportunities.
- It saves `data/processed/opportunities_processed.csv`.
- It saves `reports/daily/opportunity_report_YYYY-MM-DD.md`.
- It saves `reports/daily/opportunity_report_YYYY-MM-DD.html`.
- It prints the report paths.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add daily report generation
```

## 2026-06-15 - Optional Email Delivery

### What Was Implemented

- Added optional HTML report delivery by email.
- Added environment-based email configuration using `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, and `EMAIL_TO`.
- Added safe skip behavior when email configuration is missing.
- Added HTML email body with Markdown fallback text when available.
- Added SMTP support with TLS for standard ports and SSL for port 465.
- Updated `src/main.py` to attempt email delivery after report generation.
- Updated the README with email setup guidance and Gmail App Password guidance.
- Added tests for missing configuration, config parsing, email message creation, SMTP sending behavior, and skip behavior.

### Why It Was Implemented

Email delivery makes the generated report actionable without requiring the user to manually open local files. The feature is optional and secure by default, so the pipeline remains usable without credentials and does not expose secrets.

### Related Software Concept

- Environment-based configuration
- Secret handling
- Optional integrations
- SMTP email delivery
- Safe fallback behavior

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `src/main.py`
- `src/reports/email_sender.py`
- `tests/test_email_sender.py`

### How To Test It

Run the data pipeline without email credentials:

```bash
python -m src.main
```

Expected behavior:

- The command generates processed data and reports.
- Email sending is skipped with a clear message.
- The pipeline exits successfully.

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- All tests pass.

### Suggested Commit Message

```text
Add optional email delivery
```

## 2026-06-16 - Streamlit Dashboard

### What Was Implemented

- Added a Streamlit dashboard at `app/streamlit_app.py`.
- Added filters for category, status, priority, mode, minimum match score, and urgent-only results.
- Added top-level metrics for total opportunities, urgent opportunities, high-match opportunities, and average score.
- Added tabs for ranked opportunities, urgent opportunities, clusters, opportunity details, and generated reports.
- Added detail view with organization, deadline, mode, cluster, match reasons, priority reasons, and application link.
- Updated the README with the dashboard command.

### Why It Was Implemented

The dashboard makes the project easier to inspect without opening CSV files directly. It turns the pipeline output into an interactive review tool for filtering, ranking, and explaining recommended opportunities.

### Related Software Concept

- Interactive dashboarding
- Data exploration
- Filtering and ranking UI
- Product-oriented presentation
- Local analytics app

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `app/streamlit_app.py`

### How To Test It

Run the data pipeline first:

```bash
python -m src.main
```

Open the dashboard:

```bash
streamlit run app/streamlit_app.py
```

Run the tests:

```bash
python -m unittest
```

Expected behavior:

- The pipeline creates `data/processed/opportunities_processed.csv`.
- The dashboard loads the processed CSV and displays filters, metrics, tables, clusters, details, and report links.
- All tests pass.

### Suggested Commit Message

```text
Add Streamlit dashboard
```

## 2026-06-17 - GitHub Actions Automation

### What Was Implemented

- Added a GitHub Actions workflow at `.github/workflows/daily_radar.yml`.
- Added manual execution with `workflow_dispatch`.
- Added daily scheduled execution.
- Added Python setup and dependency installation.
- Added automated test execution with `python -m unittest`.
- Added pipeline execution with `python -m src.main`.
- Added workflow artifact upload for generated reports and processed data.
- Added optional email configuration through GitHub repository secrets.
- Updated the README with automation and secrets guidance.

### Why It Was Implemented

Automation turns the project from a local-only pipeline into a repeatable daily system. The workflow keeps the project testable in CI, generates fresh outputs, and supports optional email delivery without hardcoding credentials.

### Related Software Concept

- Continuous integration
- Scheduled automation
- Reproducible pipeline execution
- GitHub Actions
- Secret-based configuration

### Files Changed

- `README.md`
- `DEVELOPMENT_LOG.md`
- `.github/workflows/daily_radar.yml`

### How To Test It

Run the local checks:

```bash
python -m unittest
python -m src.main
```

After pushing, open the repository Actions tab and run `Daily AI Opportunity Radar` manually.

Expected behavior:

- The workflow installs dependencies.
- It runs the test suite.
- It runs the opportunity radar pipeline.
- It uploads generated reports and processed files as artifacts.
- Email sending is skipped unless secrets are configured.

### Suggested Commit Message

```text
Add GitHub Actions automation
```

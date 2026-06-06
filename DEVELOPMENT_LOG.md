# Development Log

This file tracks meaningful development steps for AI Opportunity Radar. Each entry is written so the project can be reviewed later and explained clearly in interviews.

## 2026-06-03 - Sprint 1: Project Initialization

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

Sprint 1 establishes a clean, readable foundation for the project. The goal is to make the repository understandable before adding data processing, machine learning, reporting, email, dashboard, or automation features.

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
Initialize Sprint 1 project scaffold
```

## 2026-06-04 - Sprint 2: Data Loading, Cleaning, and Normalization

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
- Updated the README with the Sprint 2 run and test commands.

### Why It Was Implemented

Sprint 2 turns the placeholder pipeline into a real data preparation step. Clean and consistent input data is necessary before adding deduplication, historical comparison, scoring, classification, clustering, reports, or dashboard features.

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
Add Sprint 2 preprocessing pipeline
```

## 2026-06-06 - Sprint 3: Deduplication and Historical Comparison

### What Was Implemented

- Added stable opportunity identity keys based on URL when available, with title and organization as a fallback.
- Added content hashes for fields that should mark an opportunity as updated.
- Added current-run deduplication that keeps the first record for each identity key.
- Added CSV-based historical comparison using `data/processed/opportunities_history.csv`.
- Added opportunity status labels for the current run: `new`, `already_seen`, and `updated`.
- Updated `src/main.py` to run preprocessing, deduplication, history comparison, and saving through one command.
- Updated the README to describe the Sprint 3 pipeline outputs.
- Added tests for deduplication and historical comparison behavior.

### Why It Was Implemented

Sprint 3 adds memory to the project. The system can now tell whether an opportunity is new, unchanged from a previous run, or changed since it was last seen. This is a necessary foundation before ranking, urgency detection, reporting, and dashboard features.

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
Add Sprint 3 deduplication and history comparison
```

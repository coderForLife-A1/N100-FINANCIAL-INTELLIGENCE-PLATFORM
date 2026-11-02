# Nifty 100 Financial Intelligence Platform

A Python-based analytics project for processing Nifty 100 data, calculating financial ratios, generating reports, and exposing results through a dashboard and API.

## Project structure

```text
config/       Screener and application configuration
data/         Generated local database files
docs/         Analyst and acceptance documentation
notebooks/    Exploratory SQL queries
output/       Generated CSV and Excel files
reports/      Generated charts, tearsheets, and test reports
src/          Pipeline, reporting, dashboard, and API code
tests/        Automated tests
```

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Common commands

The project includes a `Makefile` with commands for the main workflows:

```bash
make all        # Run the complete pipeline, tests, and report generation
make test       # Run tests and create reports/pytest_report.html
make report     # Generate reports
make dashboard  # Start the Streamlit dashboard
make api        # Start the FastAPI service on port 8000
make clean      # Remove Python and pytest cache files
```

On Windows, the same commands can be run directly with the corresponding Python tools if `make` is unavailable:

```bash
pytest --html=reports/pytest_report.html --self-contained-html tests/
python src/report_generator.py
streamlit run src/dashboard/app.py
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Generated databases, exports, charts, and test reports are excluded from version control by `.gitignore`.

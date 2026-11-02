.PHONY: all load ratios test report dashboard api clean

all: load ratios test report

load:
	python -c "from src.data_pipeline import run_pipeline; run_pipeline()"

ratios:
	python -c "from src.data_pipeline import run_pipeline; run_pipeline()"

test:
	pytest --html=reports/pytest_report.html --self-contained-html tests/

report:
	python src/report_generator.py

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	rm -rf __pycache__ .pytest_cache src/__pycache__ tests/__pycache__
	rm -rf *.pyc
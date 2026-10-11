PY ?= python3

.PHONY: data test report clean

data:
	$(PY) make_data.py

test:
	$(PY) -m pytest -q

report:
	$(PY) report.py

clean:
	rm -rf data report __pycache__ .pytest_cache
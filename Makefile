.PHONY: install run test lint format notebook

install:
	python -m pip install -e ".[dev,eda]"

run:
	uvicorn main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

notebook:
	jupyter lab analysis/01_initial_eda.ipynb


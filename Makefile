.PHONY: install run test lint format notebook dfd

install:
	python -m pip install -r requirements.txt

run:
	cd fastapi && uvicorn main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

notebook:
	jupyter lab eda/eda.ipynb

dfd:
	python others/generate_dfd.py

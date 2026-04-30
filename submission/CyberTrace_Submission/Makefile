.PHONY: install test lint format

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests
	mypy src

format:
	ruff format src tests
	ruff check --fix src tests

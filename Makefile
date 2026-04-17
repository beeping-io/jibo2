# 🤖 Jibo2 — developer convenience Makefile.
#
# Every target runs through `uv` so the pinned Python 3.12 + dev
# dependencies from pyproject.toml are always used.

.PHONY: help install test test-cov lint format hooks check clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Sync the dev environment (uv sync)
	uv sync

test: ## Run the test suite (pytest)
	uv run pytest -v

test-cov: ## Run tests with coverage report
	uv run pytest --cov=src/jibo2 --cov-report=term-missing --cov-report=xml

lint: ## Ruff lint + format check
	uv run ruff check .
	uv run ruff format --check .

format: ## Ruff format (rewrite files)
	uv run ruff format .

hooks: ## Run all pre-commit hooks on the whole repo
	uv run --with pre-commit pre-commit run --all-files

check: lint test ## Full gate bundle (lint + test) — same as CI

clean: ## Remove Python / ruff / pytest / mypy caches
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -f coverage.xml .coverage

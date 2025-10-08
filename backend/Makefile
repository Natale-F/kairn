.PHONY: help install install-dev lint format format-check check fix test test-unit test-api test-cov clean run dev-setup ci-check

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Code Quality
lint:  ## Run ruff linter
	ruff check src/ tests/

format:  ## Format code with ruff
	ruff format src/ tests/
	ruff check --fix src/ tests/

format-check:  ## Check formatting without modifying files
	ruff format --check src/ tests/

check:  ## Run all checks (lint + format-check)
	ruff check src/ tests/
	ruff format --check src/ tests/

fix:  ## Auto-fix linting issues
	ruff check --fix src/ tests/
	ruff format src/ tests/

# Testing
test:  ## Run all tests
	pytest tests/

test-unit:  ## Run unit tests only
	pytest tests/test_llm_service.py -v

test-api:  ## Run API tests only
	pytest tests/test_api.py -v

test-cov:  ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report: htmlcov/index.html"

# Development
run:  ## Run development server
	cd src && uvicorn main:app --reload --host 0.0.0.0 --port 8000

clean:  ## Clean up generated files
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	rm -rf dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Workflows
dev-setup:  ## Complete development setup
	$(MAKE) install-dev
	$(MAKE) check
	@echo "✅ Development environment ready!"

ci-check:  ## Run all CI checks
	$(MAKE) check
	$(MAKE) test-cov
	@echo "✅ All CI checks passed!"
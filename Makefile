.PHONY: help install install-dev test test-verbose test-coverage lint format type-check clean run-all-checks

# Default target
help:
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make install-dev     - Install development dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-verbose   - Run tests with verbose output"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo "  make lint           - Run code linting (flake8)"
	@echo "  make format         - Format code with black"
	@echo "  make type-check     - Run type checking with mypy"
	@echo "  make clean          - Remove generated files and caches"
	@echo "  make run-all-checks - Run all quality checks (lint, format, type-check, test)"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run all tests
test:
	pytest tests/ -v

# Run tests with verbose output
test-verbose:
	pytest tests/ -vv

# Run tests with coverage report
test-coverage:
	pytest tests/ -v --cov=problems --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Lint code with flake8
lint:
	@echo "Running flake8..."
	flake8 problems/ tests/

# Format code with black
format:
	@echo "Formatting code with black..."
	black problems/ tests/

# Check code formatting (without making changes)
format-check:
	@echo "Checking code formatting..."
	black --check problems/ tests/

# Type check with mypy
type-check:
	@echo "Running mypy type checker..."
	mypy problems/ --ignore-missing-imports

# Clean generated files
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete!"

# Run all quality checks
run-all-checks: format lint type-check test
	@echo ""
	@echo "========================================="
	@echo "All checks passed! ✓"
	@echo "========================================="

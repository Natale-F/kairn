#!/bin/bash
# Quick test runner script

set -e

echo "🧪 Running Backend Tests..."
echo ""

# Check if in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Consider activating venv: source venv/bin/activate"
    echo ""
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    pip install -r requirements-dev.txt
    echo ""
fi

# Run tests based on argument
case "${1:-all}" in
    unit)
        echo "Running unit tests..."
        pytest tests/test_llm_service.py -v
        ;;
    api)
        echo "Running API tests..."
        pytest tests/test_api.py -v
        ;;
    cov|coverage)
        echo "Running tests with coverage..."
        pytest tests --cov=. --cov-report=html --cov-report=term-missing
        echo ""
        echo "📊 Coverage report: htmlcov/index.html"
        ;;
    all|*)
        echo "Running all tests..."
        pytest tests -v
        ;;
esac

echo ""
echo "✅ Tests completed!"

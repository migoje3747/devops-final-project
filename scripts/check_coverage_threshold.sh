#!/usr/bin/env bash
set -euo pipefail

MIN_COVERAGE=${1:-80}   # default minimum coverage = 80%

echo "🔍 Checking coverage threshold (minimum: ${MIN_COVERAGE}%)"

# Run pytest with coverage and capture output
COVERAGE_OUTPUT=$(pytest --cov=app --cov-report=term --quiet 2>&1 || true)

echo "$COVERAGE_OUTPUT"

# Extract coverage percentage
COVERAGE_PERCENT=$(echo "$COVERAGE_OUTPUT" | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

if [[ -z "$COVERAGE_PERCENT" ]]; then
    echo "❌ Could not extract coverage percentage from output"
    exit 1
fi

# Compare coverage
if (( $(echo "$COVERAGE_PERCENT < $MIN_COVERAGE" | bc -l) )); then
    echo "❌ Coverage too low: ${COVERAGE_PERCENT}% (minimum: ${MIN_COVERAGE}%)"
    exit 1
else
    echo "✅ Coverage OK: ${COVERAGE_PERCENT}% (minimum: ${MIN_COVERAGE}%)"
    exit 0
fi
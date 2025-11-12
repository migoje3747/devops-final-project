#!/usr/bin/env bash
set -euo pipefail

MIN_SCORE=${1:-8.0}   # default minimum acceptable score = 8.0 (A)
PYLINT_OUTPUT=$(mktemp)
pylint app.py > "$PYLINT_OUTPUT" || true

# print output for logs
cat "$PYLINT_OUTPUT"

# extract the score line like "Your code has been rated at 7.48/10"
SCORE_LINE=$(grep "Your code has been rated at" "$PYLINT_OUTPUT" || true)
if [[ -z "$SCORE_LINE" ]]; then
  echo "Could not find pylint score in output; failing."
  exit 1
fi

# parse numeric score
SCORE=$(echo "$SCORE_LINE" | sed -E 's/.*rated at ([0-9]+\.[0-9]+)\/10.*/\1/')

# compare (float)
awk -v s="$SCORE" -v m="$MIN_SCORE" 'BEGIN{ if (s+0 < m+0) { print "Pylint score too low: " s "/10 (<" m ")"; exit 1 } else { print "Pylint score OK: " s "/10"; exit 0 } }'
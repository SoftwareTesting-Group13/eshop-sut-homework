#!/usr/bin/env bash
# Scaffold a new feature automation: data JSON + sample UI/API specs.
# Usage: bash new-feature.sh <FR-ID> <tag> [target-dir]
# Example: bash new-feature.sh FR01 fr01   (writes tests/ + data/ under target-dir)
set -euo pipefail
FR="${1:?usage: new-feature.sh <FR-ID> <tag> [target-dir]  (e.g. FR01 fr01)}"
TAG="${2:?usage: new-feature.sh <FR-ID> <tag> [target-dir]  (e.g. FR01 fr01)}"
ROOT="${3:-$(cd "$(dirname "$0")/../.." && pwd)}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

LOWER=$(echo "$FR" | tr '[:upper:]' '[:lower:]')
mkdir -p "$ROOT/tests" "$ROOT/data"

sed -e "s/__TAG_UPPER__/$(echo "$TAG" | tr '[:lower:]' '[:upper:]')/g" \
  "$SKILL_DIR/templates/data.json.template" > "$ROOT/data/${LOWER}.json"
sed -e "s/__FR__/$FR/g; s/__TAG__/$TAG/g; s/__DATA_FILE__/${LOWER}.json/g; s|__START_URL__|/|g" \
  "$SKILL_DIR/templates/spec.ui.ts.template" > "$ROOT/tests/${LOWER}.spec.ts"

command -v node >/dev/null || { echo "node not found"; exit 1; }
node -e "JSON.parse(require('fs').readFileSync('$ROOT/data/${LOWER}.json','utf8')); console.log('data JSON parses OK')"
echo "created:"
echo "  $ROOT/data/${LOWER}.json"
echo "  $ROOT/tests/${LOWER}.spec.ts  (sample only — expand per test plan next)"
echo 'next: run FEATURE=sample BROWSER=chromium npx playwright test --project=chromium --grep "@'"$TAG"'"'

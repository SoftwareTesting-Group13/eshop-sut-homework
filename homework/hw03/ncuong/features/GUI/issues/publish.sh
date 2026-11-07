#!/usr/bin/env bash
set -euo pipefail
# Publish the drafted HW03 GUI issues with the GitHub CLI.
# Prerequisites:
#   1. gh auth login (or GH_TOKEN with repo scope)
#   2. The screenshots are pushed to the branch used in the raw URLs.
# Run from homework/hw03/ncuong/features/GUI:
#   bash issues/publish.sh
cd "$(dirname "$0")/.."
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install it and run: gh auth login" >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "Not authenticated. Run: gh auth login" >&2
  exit 1
fi
python3 - <<'PY'
import json, subprocess, sys
issues = json.load(open('issues/issues.json'))
for it in issues:
    body = open(it['body_file'], encoding='utf-8').read()
    cmd = ['gh', 'issue', 'create', '--title', it['title'], '--body', body]
    for label in it['labels']:
        cmd += ['--label', label]
    print('Creating', it['title'])
    subprocess.run(cmd, check=True)
PY

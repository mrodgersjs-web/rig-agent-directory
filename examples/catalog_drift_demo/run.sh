#!/usr/bin/env bash
# catalog_drift_demo/run.sh — run the four-step drift demo.
# No network, no secrets; CI also runs these commands.
set -euo pipefail

# Resolve to repo root: this file lives at examples/catalog_drift_demo/run.sh,
# so two levels up from its directory is the project root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

. .venv/bin/activate 2>/dev/null || true
if ! command -v rig-directory >/dev/null; then
  pip install -e '.[dev]'
fi

echo "== step 1: validate the committed catalog =="
rig-directory validate

echo "== step 2: README drift check (--check exits 1 on stale) =="
rig-directory readme --check

echo "== step 3: INDEX drift check =="
tmp="$(mktemp)"
rig-directory index --out "$tmp"
diff "$tmp" INDEX.md

echo "== step 4: print the canonical counts =="
rig-directory stats

echo "== all green =="

# rig-agent-directory — copilot instructions

## What it is
A crawler and catalog for the public repos of `mrodgersjs-web`. It
reads each repo, extracts agents, skills, deviation engines and
metadata, writes one typed JSON catalog (`catalog/catalog.json`),
and generates a search CLI and a markdown index from it. Nothing in
the catalog is typed by hand; the README counts/attribution blocks
and `INDEX.md` are all derived from the catalog.

## Layout
- `rig_directory/` — package: `crawl.py`, `catalog.py`, `render.py`,
  `cli.py`, `attribution.py`, `extract.py`, `py.typed`.
- `rig_directory/schema/catalog.schema.json` — JSON Schema for the
  catalog (referenced by `catalog.py`).
- `rig_directory/data/attribution.json` — per-repo upstream facts.
- `tests/fixtures/` — fixture repos + a golden catalog used by the
  offline tests.
- `tests/` — pytest suite.
- `.github/workflows/ci.yml` — tests on every push; refresh-job is
  weekly (`.github/workflows/refresh.yml`).

## Setup and tests
```
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest -q
```

The CLI lives at the `rig-directory` script entry point. A smoke run
that rebuilds the catalog from fixtures, validates it against the
schema, and checks that README/INDEX still match is what
`.github/workflows/ci.yml` runs.

## Conventions
Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, `ci:`,
`build:`, `chore:`). Every change to public code ships a test. No
secrets; `GITHUB_TOKEN` is optional and only raises the API rate
limit. No machine paths (`/Users/...`, `~/Developer/...`,
`$HOME/Developer/...`). No prices, no client names, no
credential/military/personnel claims. Banned words: unlock, empower,
synergy, leverage, disrupt, hustle, utilize, iterate, optimize. No
em dashes.

## Truth rule
Every number in README and docs must come from a command you just
ran. The `## What is in the catalog` tables come from
`rig-directory stats`. Catalog counts come from
`rig-directory validate`. Counts that drift from a re-ran command
fail the CI drift-check that rebuilds the catalog and diffs the
generated `INDEX.md` and README blocks.

## Do not touch
`tests/fixtures/` (golden catalog). `rig_directory/data/
attribution.json` is data, not prose; add a record through
`rig-directory attribute` (or hand-edit the JSON) and re-run the
generator.

## Done-test for this work
```
ruff check .
pytest -q
```
Both clean on a fresh venv. The catalog drift check (CI's last
step) must also pass.

# Example: a runnable end-to-end check of the public directory

This example exercises the public directory end-to-end against the
**committed fixture catalog** (no network, no secrets, no GitHub
token). It does the same job as `tests/test_counts.py`, but it is
shaped so you can run it as a shell command and read the output.

## Run

```sh
cd /Users/rig128gb/Developer/rig-agent-directory
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'

# 1. Validate the committed catalog against the schema
rig-directory validate

# 2. Detect README drift (fails if the auto-generated counts block is stale)
rig-directory readme --check

# 3. Detect INDEX.md drift (fails if a catalog entry went missing)
rig-directory index --out "$RUNNER_TEMP/INDEX.md"
diff "$RUNNER_TEMP/INDEX.md" INDEX.md

# 4. Print the counts the README cites
rig-directory stats
```

A green run prints the counts JSON; a red run prints which step
failed and what the diff was.

## What this proves

- `validate` confirms the catalog matches `rig_directory/schema/catalog.schema.json`
  and that its `counts` block matches `compute_counts(catalog)` —
  this is the source-of-truth check that catches hand-edits.
- `readme --check` confirms the README's `<!-- counts:start -->`
  block matches the committed catalog — a hex `diff` of the README
  that touches a number without a corresponding catalog change fails.
- `index --diff INDEX.md` confirms every entry in the catalog is
  rendered into `INDEX.md` — a row that disappears from the catalog
  but stays in the index (or vice versa) fails.
- `stats` shows the same numbers in JSON form so you can paste them
  into an issue or a Slack thread without re-running the catalog.

## When to run it

- Before pushing anything that changes `catalog/catalog.json`,
  `README.md`, `INDEX.md`, `rig_directory/extract.py`,
  `rig_directory/render.py`, or `rig_directory/catalog.py`.
- As part of CI on every PR; CI runs the same commands and fails the
  build if any step is red.

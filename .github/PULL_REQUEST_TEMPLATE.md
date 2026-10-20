## What

One paragraph: what this PR ships and why.

## How

The mechanical change in one sentence per file touched. Tests added in
the same commit as the behavior they cover.

## Verification

```
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -e '.[dev]'
$ ruff check .
$ pytest -q
```

Paste the actual output below. If the failure you are fixing is the
reason this PR exists, paste the failing output before the fix and
the passing output after the fix.

```
<paste here>
```

## Drift checks

```
$ rig-directory validate
$ rig-directory readme --check
$ rig-directory index --out /tmp/INDEX.md && diff /tmp/INDEX.md INDEX.md
```

All three must exit 0 — if any of those check fails, the committed
catalog or its generated artifacts are stale.

## Checklist

- [ ] Tests added in the same commit as the behavior they cover
- [ ] `ruff check .` clean
- [ ] `rig-directory validate` exits 0 against the committed catalog
- [ ] `rig-directory readme --check` exits 0
- [ ] `rig-directory index` reproduces the committed `INDEX.md`
- [ ] No `~/...` or `$HOME/...` paths added to tracked files
- [ ] No "1000x", "novel", or superlative claims added
- [ ] No prices, client names, or personal data

## Linked issue

Closes #<number>.

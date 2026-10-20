"""Upstream attribution for catalog entries.

Some repos in this catalog are not original work by the catalog owner. The
facts live in ``rig_directory/data/attribution.json`` and are stamped onto
every entry extracted from an attributed repo, so the rendered README and
INDEX.md can never present adapted work as original.

This module is the only place that reads the data file. Both the crawler
(``extract.extract_agent``) and the ``attribute`` CLI command call
``source_for``, so a catalog built by crawling and a catalog re-stamped in
place carry byte-identical attribution.
"""
from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

DATA = "data/attribution.json"
SCHEMA_VERSION = 1
# Catalog keys are plural; the singular form is only used in messages.
KINDS = ("skills", "agents", "engines")

REQUIRED_FIELDS = ("repo", "origin", "upstream_owner", "upstream_repo", "upstream_url", "license", "license_url", "note")


class AttributionError(ValueError):
    """The attribution data file is malformed."""


def _load() -> dict:
    raw = json.loads(resources.files("rig_directory").joinpath(DATA).read_text("utf-8"))
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise AttributionError(f"attribution.json: schema_version must be {SCHEMA_VERSION}")
    repos = raw.get("repos")
    if not isinstance(repos, list):
        raise AttributionError("attribution.json: 'repos' must be a list")
    for record in repos:
        missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
        if missing:
            raise AttributionError(
                f"attribution.json: record for {record.get('repo')!r} is missing {missing}"
            )
        if record["origin"] != "adapted":
            raise AttributionError(
                f"attribution.json: record for {record['repo']!r} has origin "
                f"{record['origin']!r}; only 'adapted' is supported"
            )
    return raw


_CACHE: dict | None = None


def records(root: Path | None = None) -> dict[str, dict]:
    """Map repo name -> attribution record."""
    global _CACHE
    if root is not None:
        raw = json.loads((Path(root) / DATA).read_text("utf-8"))
        return _validate(raw)
    if _CACHE is None:
        _CACHE = _validate(_load())
    return _CACHE


def _validate(raw: dict) -> dict[str, dict]:
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise AttributionError(f"attribution.json: schema_version must be {SCHEMA_VERSION}")
    out: dict[str, dict] = {}
    for record in raw.get("repos") or ():
        missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
        if missing:
            raise AttributionError(
                f"attribution.json: record for {record.get('repo')!r} is missing {missing}"
            )
        out[record["repo"]] = record
    return out


def source_for(repo: str) -> dict | None:
    """The `source` block for entries extracted from `repo`, or None if original."""
    record = records().get(repo)
    if record is None:
        return None
    return {
        "origin": record["origin"],
        "upstream_owner": record["upstream_owner"],
        "upstream_repo": record["upstream_repo"],
        "upstream_url": record["upstream_url"],
        "license": record["license"],
        "license_url": record["license_url"],
        "note": record["note"],
    }


def stamp(catalog: dict) -> int:
    """Stamp (or re-stamp) the source block on every entry of an attributed repo.

    Returns the number of entries stamped. Idempotent: running it twice gives
    the same catalog and the same count.
    """
    stamped = 0
    for kind in KINDS:
        for entry in catalog.get(kind, ()):
            source = source_for(entry.get("repo", ""))
            if source is None:
                continue
            entry["source"] = dict(source)
            stamped += 1
    return stamped


def attributed_repos(catalog: dict) -> list[str]:
    """Repos in this catalog that carry at least one attributed entry."""
    known = records()
    return sorted({e["repo"] for kind in KINDS for e in catalog.get(kind, ()) if e.get("repo") in known})

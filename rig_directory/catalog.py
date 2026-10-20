"""Build, load, validate and search the catalog."""
from __future__ import annotations

import json
import subprocess
from importlib import resources
from pathlib import Path

from . import attribution
from .extract import extract_repo_content

SCHEMA_VERSION = 1
KINDS = ("repo", "skill", "agent", "engine")
PLURAL = {"repo": "repos", "skill": "skills", "agent": "agents", "engine": "engines"}


def load_schema() -> dict:
    return json.loads(resources.files("rig_directory").joinpath("schema/catalog.schema.json").read_text("utf-8"))


def head_sha(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    run = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True)
    return run.stdout.strip() or None if run.returncode == 0 else None


def build_catalog(owner: str, repos_meta: list[dict], checkouts: Path) -> dict:
    """repos_meta: GitHub REST repo objects (name, description, fork, private, archived).
    checkouts: directory holding one sub-directory per repo name."""
    repos, skills, agents, engines = [], [], [], []
    for meta in sorted(repos_meta, key=lambda m: m["name"]):
        if meta.get("private"):
            continue  # public repos only, even if a caller passes private metadata
        name = meta["name"]
        root = checkouts / name
        crawled = root.is_dir() and not meta.get("fork", False)
        entry = {
            "name": name,
            "description": " ".join((meta.get("description") or "").split()),
            "url": f"https://github.com/{owner}/{name}",
            "fork": bool(meta.get("fork", False)),
            "archived": bool(meta.get("archived", False)),
            "crawled": crawled,
            "commit": head_sha(root) if crawled else None,
            "test_files": 0,
            "counts": {"skills": 0, "agents": 0, "engines": 0},
        }
        if crawled:
            found = extract_repo_content(name, root)
            entry["test_files"] = found["test_files"]
            entry["counts"] = {k: len(found[k]) for k in ("skills", "agents", "engines")}
            skills += found["skills"]
            agents += found["agents"]
            engines += found["engines"]
        repos.append(entry)
    base = f"https://github.com/{owner}"
    for s in skills:
        s["url"] = f"{base}/{s['repo']}/blob/HEAD/{s['path']}"
    for a in agents:
        a["url"] = f"{base}/{a['repo']}/blob/HEAD/{a['path']}"
    for e in engines:
        e["url"] = f"{base}/{e['repo']}/blob/HEAD/{e['path']}"
    skills.sort(key=lambda x: (x["name"].lower(), x["repo"], x["path"]))
    agents.sort(key=lambda x: (x["department"], x["name"].lower(), x["repo"], x["path"]))
    engines.sort(key=lambda x: (x["repo"], x["id"]))
    catalog = {
        "schema_version": SCHEMA_VERSION,
        "owner": owner,
        "counts": {},
        "repos": repos,
        "skills": skills,
        "agents": agents,
        "engines": engines,
    }
    catalog["counts"] = compute_counts(catalog)
    return catalog


def compute_counts(catalog: dict) -> dict:
    agents = catalog["agents"]
    attributed = sum(1 for a in agents if a.get("source"))
    return {
        "repos": len(catalog["repos"]),
        "repos_crawled": sum(1 for r in catalog["repos"] if r["crawled"]),
        "skills": len(catalog["skills"]),
        "skills_unique_names": len({s["name"] for s in catalog["skills"]}),
        "agents": len(agents),
        "agents_unique_names": len({a["name"] for a in agents}),
        "agents_attributed": attributed,
        "agents_original": len(agents) - attributed,
        "engines": len(catalog["engines"]),
    }


def validate(catalog: dict) -> list[str]:
    """Schema check plus consistency checks. Returns a list of problems."""
    from jsonschema import Draft202012Validator

    problems = [
        f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
        for e in Draft202012Validator(load_schema()).iter_errors(catalog)
    ]
    if problems:
        return problems
    if catalog["counts"] != compute_counts(catalog):
        problems.append("counts do not match the entries")
    # Every entry from a repo listed in data/attribution.json must carry its
    # source block, and no other repo may claim one. A catalog that lists
    # adapted work as original is rejected here, not just in the docs.
    for repo in attribution.attributed_repos(catalog):
        for kind in ("skills", "agents", "engines"):
            missing = [e for e in catalog[kind] if e["repo"] == repo and not e.get("source")]
            if missing:
                names = ", ".join(str(e.get("name") or e.get("codename")) for e in missing[:3])
                problems.append(
                    f"{kind} entries from attributed repo {repo} are missing a source block: {names}"
                    + (" ..." if len(missing) > 3 else "")
                )
    known = set(attribution.records())
    for kind in ("skills", "agents", "engines"):
        for entry in catalog[kind]:
            if entry.get("source") and entry["repo"] not in known:
                problems.append(
                    f"{kind} entry {entry.get('name') or entry.get('codename')} from {entry['repo']} "
                    "claims a source block but that repo is not in data/attribution.json"
                )
    names = {r["name"] for r in catalog["repos"]}
    for kind in ("skills", "agents", "engines"):
        for item in catalog[kind]:
            if item["repo"] not in names:
                problems.append(f"{kind} entry {item.get('name') or item.get('codename')} has unknown repo {item['repo']}")
    for r in catalog["repos"]:
        actual = {k: sum(1 for i in catalog[k] if i["repo"] == r["name"]) for k in ("skills", "agents", "engines")}
        if r["counts"] != actual:
            problems.append(f"repo {r['name']} counts {r['counts']} != {actual}")
    return problems


def entries(catalog: dict, kind: str | None = None):
    """Yield (kind, entry) pairs, optionally limited to one kind."""
    for k in KINDS:
        if kind and k != kind:
            continue
        for e in catalog[PLURAL[k]]:
            yield k, e


def search(catalog: dict, query: str = "", kind: str | None = None, repo: str | None = None,
           department: str | None = None, layer: str | None = None, pack: str | None = None) -> list[tuple[str, dict]]:
    terms = query.lower().split()
    out = []
    for k, e in entries(catalog, kind):
        if repo and e.get("repo", e.get("name")) != repo:
            continue
        if department and e.get("department") != department:
            continue
        if layer and e.get("layer", "").lower() != layer.lower():
            continue
        if pack and e.get("pack") != pack:
            continue
        hay = " ".join(str(e.get(f, "")) for f in ("name", "codename", "full_name", "description", "department", "layer", "pack")).lower()
        if all(t in hay for t in terms):
            out.append((k, e))
    return out

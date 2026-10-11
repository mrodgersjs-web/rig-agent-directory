"""rig-directory command line."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from . import catalog as cat
from . import crawl, render

DEFAULT_CATALOG = Path("catalog/catalog.json")


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_crawl(a) -> int:
    if a.live:
        meta = crawl.list_public_repos(a.owner)
        root = Path(a.checkouts) if a.checkouts else Path(tempfile.mkdtemp(prefix="rig-directory-"))
        failed = crawl.clone_repos(a.owner, meta, root)
        if failed:
            print(f"clone failed for: {', '.join(failed)}", file=sys.stderr)
            return 1
    else:
        if not (a.repos_meta and a.checkouts):
            print("offline crawl needs --repos-meta and --checkouts (or use --live)", file=sys.stderr)
            return 2
        meta = json.loads(Path(a.repos_meta).read_text(encoding="utf-8"))
        root = Path(a.checkouts)
    catalog = cat.build_catalog(a.owner, meta, root)
    problems = cat.validate(catalog)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    _write_json(Path(a.out), catalog)
    print(json.dumps(catalog["counts"]))
    return 0


def cmd_validate(a) -> int:
    problems = cat.validate(_load(a.catalog))
    for p in problems:
        print(p, file=sys.stderr)
    if not problems:
        print(f"{a.catalog}: valid")
    return 1 if problems else 0


def cmd_search(a) -> int:
    hits = cat.search(_load(a.catalog), " ".join(a.query), a.kind, a.repo, a.department, a.layer, a.pack)
    if a.json:
        print(json.dumps([{"kind": k, **e} for k, e in hits], indent=2, ensure_ascii=False))
    else:
        for k, e in hits:
            label = e.get("name") or e.get("codename")
            where = e.get("repo", "")
            print(f"{k:7} {label}  [{where}]  {e['description'][:100]}")
        print(f"{len(hits)} match(es)", file=sys.stderr)
    return 0 if hits else 1


def cmd_index(a) -> int:
    Path(a.out).write_text(render.render_index(_load(a.catalog)), encoding="utf-8")
    return 0


def cmd_readme(a) -> int:
    path = Path(a.readme)
    new = render.update_readme(path.read_text(encoding="utf-8"), _load(a.catalog))
    if a.check:
        if new != path.read_text(encoding="utf-8"):
            print(f"{path} counts block is stale; run `rig-directory readme`", file=sys.stderr)
            return 1
        return 0
    path.write_text(new, encoding="utf-8")
    return 0


def cmd_stats(a) -> int:
    print(json.dumps(_load(a.catalog)["counts"], indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="rig-directory")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("crawl", help="build the catalog from repo checkouts")
    c.add_argument("--owner", default="mrodgersjs-web")
    c.add_argument("--live", action="store_true", help="list public repos on GitHub and clone them")
    c.add_argument("--repos-meta", help="JSON list of GitHub repo objects (offline mode)")
    c.add_argument("--checkouts", help="dir with one sub-dir per repo (offline), or clone cache (live)")
    c.add_argument("--out", default=str(DEFAULT_CATALOG))
    c.set_defaults(fn=cmd_crawl)

    for name, fn, help_ in (("validate", cmd_validate, "validate a catalog against the schema"),
                            ("search", cmd_search, "search / filter the catalog"),
                            ("index", cmd_index, "write the markdown index"),
                            ("readme", cmd_readme, "refresh the README counts block"),
                            ("stats", cmd_stats, "print counts")):
        s = sub.add_parser(name, help=help_)
        s.add_argument("--catalog", default=str(DEFAULT_CATALOG))
        s.set_defaults(fn=fn)
        if name == "search":
            s.add_argument("query", nargs="*")
            s.add_argument("--kind", choices=cat.KINDS)
            s.add_argument("--repo")
            s.add_argument("--department")
            s.add_argument("--layer")
            s.add_argument("--pack")
            s.add_argument("--json", action="store_true")
        if name == "index":
            s.add_argument("--out", default="INDEX.md")
        if name == "readme":
            s.add_argument("--readme", default="README.md")
            s.add_argument("--check", action="store_true", help="exit 1 if the block is stale")
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

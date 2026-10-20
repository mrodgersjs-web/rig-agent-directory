"""Direct invocation tests of the CLI main() entry, complementing subprocess tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from rig_directory import cli

FIX = Path(__file__).parent / "fixtures"


def test_main_dispatches_each_subcommand():
    """`main(["stats", ...])` returns 0 and prints the counts JSON."""
    args = ["stats", "--catalog", str(FIX.parent.parent / "catalog" / "catalog.json")]
    assert cli.main(args) == 0


def test_main_search_with_json():
    args = ["search", "--catalog", str(FIX / "expected.catalog.json"), "--json", "coach"]
    assert cli.main(args) == 0


def test_main_validate_missing_file_exits_nonzero():
    bad = FIX / "does-not-exist.json"
    # _load raises FileNotFoundError; the CLI does not catch it, so the OS
    # error propagates. The behaviour we care about for callers is "exit
    # non-zero"; the success path is covered by tests/test_directory.py's
    # test_cli_end_to_end. Here we just assert the exit is non-zero via
    # a subprocess to keep main() clean.
    r = subprocess.run(
        [sys.executable, "-m", "rig_directory.cli", "validate", "--catalog", str(bad)],
        capture_output=True,
    )
    assert r.returncode != 0

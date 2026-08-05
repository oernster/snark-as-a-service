"""Stamp the version from VERSION into the published site.

The landing site under `docs/` is static HTML served by GitHub Pages, so it
cannot read VERSION when it renders. It carries the version between delimiters
instead:

    v<!--VERSION-->1.2.3<!--/VERSION-->

This script rewrites whatever sits between those delimiters to match VERSION.
It targets the site tree ONLY, never the root markdown files, which are required
to stay free of version data. Running it twice in a row touches nothing the
second time.

Usage:

    python stamp_version.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
VERSION_FILE = REPO_ROOT / "VERSION"
SITE_DIR = REPO_ROOT / "docs"
SITE_GLOBS = ("*.html", "*.css", "*.js")

TOKEN = re.compile(r"(<!--VERSION-->)(.*?)(<!--/VERSION-->)", re.DOTALL)


def read_version() -> str:
    """Return the version recorded in VERSION, stripped."""

    return VERSION_FILE.read_text(encoding="utf-8").strip()


def site_files() -> list[Path]:
    """Every file in the site tree that may carry a version token."""

    found: list[Path] = []
    for pattern in SITE_GLOBS:
        found.extend(SITE_DIR.rglob(pattern))
    return sorted(found)


def stamp(version: str, paths: list[Path]) -> tuple[list[Path], int]:
    """Rewrite every token in `paths` to `version`.

    Returns the files actually changed and the number of tokens found. Line
    endings are read and written verbatim so a stamp never reformats a file.
    """

    changed: list[Path] = []
    seen = 0

    for path in paths:
        with open(path, encoding="utf-8", newline="") as handle:
            original = handle.read()

        seen += len(TOKEN.findall(original))
        updated = TOKEN.sub(rf"\g<1>{version}\g<3>", original)
        if updated == original:
            continue

        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(updated)
        changed.append(path)

    return changed, seen


def main() -> int:
    if not VERSION_FILE.is_file():
        print(f"No VERSION file at {VERSION_FILE}")
        return 1
    if not SITE_DIR.is_dir():
        print(f"No site directory at {SITE_DIR}")
        return 1

    version = read_version()
    if not version:
        print(f"{VERSION_FILE} is empty")
        return 1

    paths = site_files()
    changed, seen = stamp(version, paths)

    print(f"Version {version}: {seen} token(s) in {len(paths)} site file(s).")
    if changed:
        for path in changed:
            print(f"  stamped {path.relative_to(REPO_ROOT).as_posix()}")
    else:
        print("  nothing to change; every token already matches.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

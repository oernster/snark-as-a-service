"""The application version, read from the repository-root VERSION file.

VERSION is the single source of truth. Nothing else in the tree states a version
number, so a bump is one edit and cannot half-apply. The fallback exists because
the file is a repository artefact rather than a packaged one: a deployment that
copies only the `app` package still starts, it just reports a dev placeholder.
"""

from pathlib import Path

FALLBACK_VERSION = "0.0.0-dev"
VERSION_FILE = Path(__file__).resolve().parent.parent / "VERSION"


def read_version(path: Path = VERSION_FILE) -> str:
    """Return the version recorded in `path` or the dev fallback."""

    try:
        recorded = path.read_text(encoding="utf-8").strip()
    except OSError:
        return FALLBACK_VERSION
    return recorded or FALLBACK_VERSION


__version__ = read_version()

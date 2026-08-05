"""The version is read from one file; a missing file is not fatal.

VERSION is the single source of truth, so the reader has to hold two promises:
it returns exactly what the file says; an absent or empty file degrades to the
dev placeholder rather than stopping the application from starting.
"""

from app.version import FALLBACK_VERSION, VERSION_FILE, __version__, read_version


def test_the_version_is_read_from_the_file(tmp_path):
    path = tmp_path / "VERSION"
    path.write_text("9.9.9\n", encoding="utf-8")

    assert read_version(path) == "9.9.9"


def test_a_missing_file_gives_the_dev_fallback(tmp_path):
    assert read_version(tmp_path / "absent") == FALLBACK_VERSION


def test_an_empty_file_gives_the_dev_fallback(tmp_path):
    path = tmp_path / "VERSION"
    path.write_text("   \n", encoding="utf-8")

    assert read_version(path) == FALLBACK_VERSION


def test_the_repository_version_file_is_the_one_that_is_used():
    # The module-level value is what FastAPI reports, so it must come from the
    # repository file rather than the fallback.
    assert VERSION_FILE.is_file()
    assert __version__ == VERSION_FILE.read_text(encoding="utf-8").strip()

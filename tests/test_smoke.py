"""Smoke test — validates CI end-to-end.

Replaced by real tests once Phase 0 M0.2 (Testing infrastructure) lands.
"""

from jibo2 import __version__


def test_version_defined() -> None:
    assert __version__ == "0.0.0"


def test_smoke() -> None:
    assert True

"""Shared test fixtures visible to the entire test tree."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Absolute path to `tests/fixtures/`."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_path(fixtures_dir: Path):
    """Resolve a named fixture relative to `tests/fixtures/`.

    Usage:
        def test_something(fixture_path):
            wav = fixture_path("audio/wake_word_quiet_room.wav")
            ...
    """

    def _resolve(name: str) -> Path:
        candidate = fixtures_dir / name
        if not candidate.exists():
            pytest.skip(f"fixture missing: tests/fixtures/{name}")
        return candidate

    return _resolve

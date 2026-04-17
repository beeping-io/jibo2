"""E2E-specific fixtures."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests.e2e.mock_jibo2 import MockJibo2


@pytest.fixture
def mock_jibo2() -> MockJibo2:
    """Fresh MockJibo2 per test."""
    return MockJibo2()


@pytest.fixture
def advance_time(mock_jibo2: MockJibo2) -> Callable[[float], None]:
    """Shortcut to advance the mock's clock without touching real time."""
    return mock_jibo2.advance_clock

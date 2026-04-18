"""Unit tests for `jibo2.config`."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from jibo2 import (
    EnvSecretSource,
    SecretNotFoundError,
    SecretSource,
    clear_cache,
    get_secret,
    set_sources,
)
from jibo2.config import set_ttl


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    """Restore defaults between tests."""
    set_sources([EnvSecretSource()])
    set_ttl(300.0)
    clear_cache()


def test_get_secret_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    assert get_secret("ANTHROPIC_API_KEY") == "sk-ant-test"


def test_missing_secret_raises_secret_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DOES_NOT_EXIST", raising=False)
    with pytest.raises(SecretNotFoundError, match="DOES_NOT_EXIST"):
        get_secret("DOES_NOT_EXIST")


def test_default_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEFAULT_FALLBACK", raising=False)
    assert get_secret("DEFAULT_FALLBACK", default="fallback-value") == "fallback-value"


class _CountingSource:
    """Test helper — counts `get` invocations per name."""

    def __init__(self, values: dict[str, str]) -> None:
        self.values = values
        self.calls: dict[str, int] = {}

    def get(self, name: str) -> str | None:
        self.calls[name] = self.calls.get(name, 0) + 1
        return self.values.get(name)


def test_cache_hits_second_call() -> None:
    source = _CountingSource({"KEY": "value"})
    set_sources([source])

    assert get_secret("KEY") == "value"
    assert get_secret("KEY") == "value"

    assert source.calls["KEY"] == 1


def test_cache_expires_after_ttl() -> None:
    source = _CountingSource({"KEY": "value"})
    set_sources([source])
    set_ttl(0.01)

    assert get_secret("KEY") == "value"
    time.sleep(0.02)
    assert get_secret("KEY") == "value"

    assert source.calls["KEY"] == 2


def test_clear_cache_forces_refresh() -> None:
    source = _CountingSource({"KEY": "value"})
    set_sources([source])

    get_secret("KEY")
    clear_cache()
    get_secret("KEY")

    assert source.calls["KEY"] == 2


def test_custom_source_chain_order() -> None:
    primary = _CountingSource({"ONLY_IN_PRIMARY": "primary"})
    secondary = _CountingSource({"ONLY_IN_PRIMARY": "secondary", "ONLY_IN_SECONDARY": "b"})
    set_sources([primary, secondary])

    assert get_secret("ONLY_IN_PRIMARY") == "primary"
    # secondary is queried only for keys primary does not know about.
    assert get_secret("ONLY_IN_SECONDARY") == "b"
    assert secondary.calls.get("ONLY_IN_PRIMARY") is None


def test_set_sources_clears_cache() -> None:
    initial = _CountingSource({"KEY": "initial"})
    set_sources([initial])
    get_secret("KEY")

    replacement = _CountingSource({"KEY": "replaced"})
    set_sources([replacement])
    assert get_secret("KEY") == "replaced"


def test_missing_secret_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    """Hitting a missing key twice should touch the chain only once."""
    source = _CountingSource({})
    set_sources([source])

    with pytest.raises(SecretNotFoundError):
        get_secret("NOPE", default=None)
    with pytest.raises(SecretNotFoundError):
        get_secret("NOPE", default=None)

    assert source.calls["NOPE"] == 1


def test_dotenv_loaded_when_present(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        """
        # comment line
        FOO=from_file
        BAR="quoted_value"
        BAZ='also_quoted'
        """.strip(),
        encoding="utf-8",
    )
    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.delenv("BAR", raising=False)
    monkeypatch.delenv("BAZ", raising=False)

    set_sources([EnvSecretSource(dotenv_path=env_file)])
    assert get_secret("FOO") == "from_file"
    assert get_secret("BAR") == "quoted_value"
    assert get_secret("BAZ") == "also_quoted"


def test_dotenv_does_not_override_existing_env(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("OVERRIDE_TEST=from_file", encoding="utf-8")
    monkeypatch.setenv("OVERRIDE_TEST", "from_env")

    set_sources([EnvSecretSource(dotenv_path=env_file)])
    assert get_secret("OVERRIDE_TEST") == "from_env"


def test_dotenv_skips_malformed_lines(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "NOT_AN_ENV_LINE\n=missing_key\nGOOD=value\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("GOOD", raising=False)

    set_sources([EnvSecretSource(dotenv_path=env_file)])
    assert get_secret("GOOD") == "value"


def test_dotenv_missing_is_ok(tmp_path: Path) -> None:
    """Absent .env must not crash — the source just returns None."""
    missing = tmp_path / ".env"
    source = EnvSecretSource(dotenv_path=missing)
    assert source.get("ANYTHING") is None


def test_env_source_satisfies_protocol() -> None:
    source = EnvSecretSource()
    assert isinstance(source, SecretSource)

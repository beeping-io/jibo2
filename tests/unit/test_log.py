"""Unit tests for `jibo2.log`."""

from __future__ import annotations

import json
import logging

import pytest

from jibo2 import configure, get_logger


@pytest.fixture(autouse=True)
def _reset_structlog(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset the module's configured flag and structlog caches between tests."""
    import structlog

    import jibo2.log

    monkeypatch.setattr(jibo2.log, "_configured", False, raising=False)
    structlog.reset_defaults()


def test_get_logger_returns_object() -> None:
    log = get_logger("jibo2.test")
    assert log is not None
    assert hasattr(log, "info")


def test_json_mode_produces_valid_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("JIBO2_ENV", "prod")
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "INFO")
    configure(force=True)

    log = get_logger("jibo2.test")
    log.info("boot_complete", component="agent", voice="skywalker")

    captured = capsys.readouterr().out.strip().splitlines()
    assert captured, "expected at least one log line on stdout"
    payload = json.loads(captured[-1])
    assert payload["event"] == "boot_complete"
    assert payload["component"] == "agent"
    assert payload["voice"] == "skywalker"
    assert payload["level"] == "info"
    assert "timestamp" in payload


def test_human_mode_default_dev(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("JIBO2_ENV", raising=False)
    configure(force=True)

    log = get_logger("jibo2.test")
    log.info("hello_world", x=42)

    out = capsys.readouterr().out
    assert "hello_world" in out
    # Dev renderer is not JSON.
    with pytest.raises(json.JSONDecodeError):
        json.loads(out.strip().splitlines()[-1])


def test_log_level_filters_below_threshold(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "WARNING")
    configure(force=True)

    log = get_logger("jibo2.test")
    log.debug("dropped")
    log.info("also_dropped")
    log.warning("kept")

    out = capsys.readouterr().out
    assert "dropped" not in out
    assert "also_dropped" not in out
    assert "kept" in out


def test_context_binding(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("JIBO2_ENV", "prod")
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "INFO")
    configure(force=True)

    log = get_logger("jibo2.test").bind(request_id="abc-123", user="alfred")
    log.info("served")

    payload = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert payload["request_id"] == "abc-123"
    assert payload["user"] == "alfred"


def test_invalid_log_level_falls_back_to_info(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "NOT_A_REAL_LEVEL")

    import jibo2.log as log_module

    assert log_module._resolve_level() == logging.INFO


def test_configure_is_idempotent(monkeypatch: pytest.MonkeyPatch) -> None:
    # First call configures.
    configure()

    import jibo2.log as log_module

    assert log_module._configured is True
    # Second call without force should be a no-op — no exception, flag stays True.
    configure()
    assert log_module._configured is True

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
    monkeypatch.setattr(jibo2.log, "_level_override", None, raising=False)
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


def test_file_handler_not_added_when_log_dir_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("JIBO2_LOG_DIR", raising=False)
    configure(force=True)

    root = logging.getLogger()
    file_handlers = [
        h for h in root.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)
    ]
    assert file_handlers == []


def test_file_handler_added_when_log_dir_set(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    monkeypatch.setenv("JIBO2_LOG_DIR", str(tmp_path))
    configure(force=True)

    root = logging.getLogger()
    file_handlers = [
        h for h in root.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)
    ]
    assert len(file_handlers) == 1

    log = get_logger("jibo2.test")
    log.info("to_disk", hello="world")

    # Flush the file handler so the record lands on disk synchronously.
    for handler in file_handlers:
        handler.flush()

    log_file = tmp_path / "jibo2.log"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "to_disk" in content


def test_retention_dev_is_7_days(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    monkeypatch.setenv("JIBO2_LOG_DIR", str(tmp_path))
    monkeypatch.delenv("JIBO2_ENV", raising=False)
    configure(force=True)

    root = logging.getLogger()
    file_handlers = [
        h for h in root.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)
    ]
    assert file_handlers[0].backupCount == 7


def test_retention_prod_is_30_days(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    monkeypatch.setenv("JIBO2_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("JIBO2_ENV", "prod")
    configure(force=True)

    root = logging.getLogger()
    file_handlers = [
        h for h in root.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)
    ]
    assert file_handlers[0].backupCount == 30


def test_set_level_overrides_env(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from jibo2 import set_level

    monkeypatch.setenv("JIBO2_ENV", "prod")
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "INFO")
    configure(force=True)

    set_level("WARNING")

    log = get_logger("jibo2.test")
    log.info("should_be_dropped")
    log.warning("should_emit")

    out = capsys.readouterr().out
    assert "should_be_dropped" not in out
    assert "should_emit" in out


def test_reset_level_restores_env(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from jibo2 import reset_level, set_level

    monkeypatch.setenv("JIBO2_ENV", "prod")
    monkeypatch.setenv("JIBO2_LOG_LEVEL", "INFO")
    configure(force=True)

    set_level("ERROR")
    get_logger().info("dropped_during_override")

    reset_level()
    get_logger().info("emitted_after_reset")

    out = capsys.readouterr().out
    assert "dropped_during_override" not in out
    assert "emitted_after_reset" in out


def test_set_level_accepts_int(monkeypatch: pytest.MonkeyPatch) -> None:
    from jibo2 import set_level

    set_level(logging.DEBUG)

    import jibo2.log as log_module

    assert log_module._resolve_level() == logging.DEBUG


def test_set_level_rejects_unknown_name() -> None:
    from jibo2 import set_level

    with pytest.raises(ValueError, match="unknown log level"):
        set_level("NOT_A_LEVEL")

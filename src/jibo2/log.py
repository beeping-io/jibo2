"""Structured logging for Jibo2.

Single entry point: `from jibo2 import get_logger`.

Environment variables:

- ``JIBO2_ENV`` — ``dev`` (default) or ``prod``. Controls the renderer:
  * ``dev``  → human-friendly ConsoleRenderer
  * ``prod`` → line-delimited JSON (one object per log line)
- ``JIBO2_LOG_LEVEL`` — ``DEBUG`` / ``INFO`` (default) / ``WARNING`` /
  ``ERROR`` / ``CRITICAL``. Records below the threshold are dropped.
- ``JIBO2_LOG_DIR`` — optional. If set, logs are also written to
  ``{dir}/jibo2.log`` with daily rotation and retention of 7 days in
  ``dev`` / 30 days in ``prod``. stdout always receives everything;
  the file handler is additive.

Runtime overrides:

- :func:`set_level` and :func:`reset_level` let callers override the
  level at runtime. This is the hook Firebase Remote Config plugs into
  (see the follow-up task in F0:M5). Priority: explicit override >
  env var > INFO default. If Remote Config is unreachable the env
  value still drives the level — offline-first is a project principle.

Architecture: structlog pipeline → stdlib ``logging`` → one or more
handlers (``StreamHandler`` + ``TimedRotatingFileHandler``). This bridge
lets the file handler do rotation natively and also captures foreign
stdlib-logging messages (e.g. third-party libraries) with the same
format.

Calling ``get_logger()`` the first time configures structlog with the
current env values. Pass ``force=True`` to :func:`configure` to re-read
the env (useful in tests that monkeypatch the environment).
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
from pathlib import Path

import structlog
from structlog.types import Processor

_configured: bool = False
_level_override: int | None = None

_SHARED_PROCESSORS: list[Processor] = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

_DEV_RETENTION_DAYS = 7
_PROD_RETENTION_DAYS = 30


def _env() -> str:
    return os.environ.get("JIBO2_ENV", "dev").lower()


def _renderer() -> Processor:
    if _env() == "prod":
        return structlog.processors.JSONRenderer()
    return structlog.dev.ConsoleRenderer(colors=False)


def _resolve_level() -> int:
    # Explicit runtime override wins over env.
    if _level_override is not None:
        return _level_override
    raw = os.environ.get("JIBO2_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, raw, None)
    if isinstance(level, int):
        return level
    return logging.INFO


def _coerce_level(level: str | int) -> int:
    if isinstance(level, int):
        return level
    resolved = getattr(logging, level.upper(), None)
    if isinstance(resolved, int):
        return resolved
    msg = f"unknown log level: {level!r}"
    raise ValueError(msg)


def set_level(level: str | int) -> None:
    """Override the active log level at runtime.

    Accepts a level name (``"DEBUG"``, ``"INFO"``, ...) or the matching
    stdlib ``logging`` integer. Takes precedence over ``JIBO2_LOG_LEVEL``
    and persists until :func:`reset_level` is called.
    """
    global _level_override
    _level_override = _coerce_level(level)
    configure(force=True)


def reset_level() -> None:
    """Clear any runtime override and return to the env-driven level."""
    global _level_override
    _level_override = None
    configure(force=True)


def _retention_days() -> int:
    return _PROD_RETENTION_DAYS if _env() == "prod" else _DEV_RETENTION_DAYS


def _make_formatter() -> logging.Formatter:
    return structlog.stdlib.ProcessorFormatter(
        processor=_renderer(),
        foreign_pre_chain=_SHARED_PROCESSORS,
    )


def _build_handlers(level: int) -> list[logging.Handler]:
    formatter = _make_formatter()

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(level)
    handlers: list[logging.Handler] = [stdout_handler]

    log_dir = os.environ.get("JIBO2_LOG_DIR")
    if log_dir:
        dir_path = Path(log_dir)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.TimedRotatingFileHandler(
            dir_path / "jibo2.log",
            when="midnight",
            interval=1,
            backupCount=_retention_days(),
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        handlers.append(file_handler)

    return handlers


def configure(*, force: bool = False) -> None:
    """Configure the global structlog + stdlib logging pipeline.

    Idempotent by default — re-invocations are a no-op once configured.
    Tests that mutate env vars should pass ``force=True`` to re-apply.
    """
    global _configured
    if _configured and not force:
        return

    level = _resolve_level()

    root = logging.getLogger()
    root.setLevel(level)
    for existing in list(root.handlers):
        root.removeHandler(existing)
    for handler in _build_handlers(level):
        root.addHandler(handler)

    structlog.configure(
        processors=[
            *_SHARED_PROCESSORS,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=not force,
    )
    _configured = True


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a bound logger configured once per process."""
    configure()
    return structlog.get_logger(name)

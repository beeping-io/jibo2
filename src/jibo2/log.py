"""Structured logging for Jibo2.

Single entry point: `from jibo2 import get_logger` (re-exported from
`jibo2.log.get_logger`).

Environment variables:

- ``JIBO2_ENV`` — ``dev`` (default) or ``prod``. Controls the renderer:
  * ``dev``  → human-friendly ConsoleRenderer
  * ``prod`` → line-delimited JSON (one object per log line)
- ``JIBO2_LOG_LEVEL`` — ``DEBUG`` / ``INFO`` (default) / ``WARNING`` /
  ``ERROR`` / ``CRITICAL``. Records below the threshold are dropped.

Calling ``get_logger()`` the first time configures structlog with the
current env values. Pass ``force=True`` to :func:`configure` to re-read
the env (useful in tests that monkeypatch the environment).
"""

from __future__ import annotations

import logging
import os
from typing import Any

import structlog

_configured: bool = False


def _processors() -> list[Any]:
    env = os.environ.get("JIBO2_ENV", "dev").lower()
    shared: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if env == "prod":
        return [*shared, structlog.processors.JSONRenderer()]
    return [*shared, structlog.dev.ConsoleRenderer(colors=False)]


def _resolve_level() -> int:
    raw = os.environ.get("JIBO2_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, raw, None)
    if isinstance(level, int):
        return level
    return logging.INFO


def configure(*, force: bool = False) -> None:
    """Configure the global structlog pipeline.

    Idempotent by default — re-invocations are a no-op once configured.
    Tests that mutate env vars can pass ``force=True`` to re-apply.
    """
    global _configured
    if _configured and not force:
        return
    structlog.configure(
        processors=_processors(),
        wrapper_class=structlog.make_filtering_bound_logger(_resolve_level()),
        context_class=dict,
        cache_logger_on_first_use=not force,
    )
    _configured = True


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a bound logger configured once per process."""
    configure()
    return structlog.get_logger(name)

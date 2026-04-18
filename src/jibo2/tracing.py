"""Performance-tracing abstraction for Jibo2.

Provides a tracer-agnostic way to mark critical code paths — boot,
wake-word detection, STT/LLM/TTS roundtrips, motor commands — without
coupling every module to a specific backend.

Today the default is :class:`NoOpTracer` (zero overhead, nothing
uploaded). A follow-up task (J2-91) will register a Firebase
Performance Monitoring implementation that satisfies the same
:class:`Tracer` protocol. :class:`MemoryTracer` is an in-process
implementation used by tests.

Public API:

- :func:`get_tracer` / :func:`set_tracer` — access/replace the global.
- :func:`span` — context manager for inline scoping.
- :func:`trace` — decorator for sync or async callables.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Literal, ParamSpec, Protocol, TypeVar, runtime_checkable

Status = Literal["ok", "error"]
AttributeValue = str | int | float | bool | None


@runtime_checkable
class Span(Protocol):
    """A single tracing span."""

    name: str

    def set_attribute(self, key: str, value: AttributeValue) -> None: ...
    def set_status(self, status: Status) -> None: ...
    def end(self) -> None: ...


@runtime_checkable
class Tracer(Protocol):
    """Creates spans. Implementations decide what to do with them."""

    def start_span(
        self,
        name: str,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Span: ...


class NoOpSpan:
    def __init__(self, name: str) -> None:
        self.name = name

    def set_attribute(self, key: str, value: AttributeValue) -> None: ...
    def set_status(self, status: Status) -> None: ...
    def end(self) -> None: ...


class NoOpTracer:
    def start_span(
        self,
        name: str,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Span:
        _ = attributes
        return NoOpSpan(name)


@dataclass
class MemorySpan:
    """Span implementation that keeps state in memory for tests."""

    name: str
    attributes: dict[str, AttributeValue] = field(default_factory=dict)
    status: Status = "ok"
    start_time: float = field(default_factory=time.monotonic)
    end_time: float | None = None

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time) * 1000.0

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        self.attributes[key] = value

    def set_status(self, status: Status) -> None:
        self.status = status

    def end(self) -> None:
        if self.end_time is None:
            self.end_time = time.monotonic()


@dataclass
class MemoryTracer:
    """Tracer that keeps every span in `spans` list for assertions."""

    spans: list[MemorySpan] = field(default_factory=list)

    def start_span(
        self,
        name: str,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Span:
        new_span = MemorySpan(name=name, attributes=dict(attributes or {}))
        self.spans.append(new_span)
        return new_span

    def names(self) -> list[str]:
        return [s.name for s in self.spans]


_current_tracer: Tracer = NoOpTracer()


def get_tracer() -> Tracer:
    return _current_tracer


def set_tracer(tracer: Tracer) -> None:
    global _current_tracer
    _current_tracer = tracer


@contextmanager
def span(name: str, **attributes: AttributeValue) -> Iterator[Span]:
    """Open a span for the duration of the ``with`` block."""
    active = get_tracer().start_span(name, attributes)
    try:
        yield active
    except Exception:
        active.set_status("error")
        active.end()
        raise
    active.set_status("ok")
    active.end()


P = ParamSpec("P")
T = TypeVar("T")


def trace(name: str | None = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator that traces the decorated callable.

    Works for sync and async functions. The span name defaults to
    ``{module}.{qualname}`` if ``name`` is omitted. Exceptions mark the
    span as ``error`` and are re-raised.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        resolved_name = name or f"{func.__module__}.{func.__qualname__}"

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                active = get_tracer().start_span(resolved_name)
                try:
                    result = await func(*args, **kwargs)
                except Exception:
                    active.set_status("error")
                    active.end()
                    raise
                active.set_status("ok")
                active.end()
                return result  # type: ignore[return-value]

            return async_wrapper  # type: ignore[return-value]

        @wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            active = get_tracer().start_span(resolved_name)
            try:
                result = func(*args, **kwargs)
            except Exception:
                active.set_status("error")
                active.end()
                raise
            active.set_status("ok")
            active.end()
            return result

        return sync_wrapper

    return decorator

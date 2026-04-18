"""Unit tests for `jibo2.tracing`."""

from __future__ import annotations

import pytest

from jibo2 import MemoryTracer, NoOpTracer, get_tracer, set_tracer, span, trace


@pytest.fixture(autouse=True)
def _reset_tracer() -> None:
    set_tracer(NoOpTracer())


def test_get_tracer_default_is_noop() -> None:
    assert isinstance(get_tracer(), NoOpTracer)


def test_set_tracer_replaces_global() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)
    assert get_tracer() is tracer


def test_noop_default_does_nothing() -> None:
    @trace("no_recording")
    def run() -> int:
        return 1

    assert run() == 1
    # No attribute on NoOpTracer to inspect — the fact it didn't blow up is the test.


def test_trace_decorator_sync() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    @trace("boot")
    def boot() -> str:
        return "done"

    result = boot()

    assert result == "done"
    assert tracer.names() == ["boot"]
    assert tracer.spans[0].status == "ok"
    assert tracer.spans[0].duration_ms is not None
    assert tracer.spans[0].duration_ms >= 0


async def test_trace_decorator_async() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    @trace("llm_request")
    async def ask() -> str:
        return "reply"

    assert await ask() == "reply"
    assert tracer.names() == ["llm_request"]
    assert tracer.spans[0].status == "ok"


def test_trace_captures_sync_exceptions() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    @trace("will_fail")
    def boom() -> None:
        raise RuntimeError("nope")

    with pytest.raises(RuntimeError, match="nope"):
        boom()

    assert tracer.spans[0].status == "error"
    assert tracer.spans[0].end_time is not None


async def test_trace_captures_async_exceptions() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    @trace("will_fail_async")
    async def boom() -> None:
        msg = "async nope"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="async nope"):
        await boom()

    assert tracer.spans[0].status == "error"


def test_trace_default_name_is_qualname() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    @trace()
    def named_func() -> None: ...

    named_func()

    assert tracer.spans[0].name.endswith("named_func")


def test_span_context_manager() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    with span("inline_work", voice="skywalker") as s:
        s.set_attribute("latency_ms", 123)

    assert tracer.spans[0].name == "inline_work"
    assert tracer.spans[0].attributes == {"voice": "skywalker", "latency_ms": 123}
    assert tracer.spans[0].status == "ok"


def test_span_captures_exceptions() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    with pytest.raises(ValueError, match="bad"), span("risky"):
        msg = "bad"
        raise ValueError(msg)

    assert tracer.spans[0].status == "error"
    assert tracer.spans[0].end_time is not None


def test_span_nested() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    with span("outer"), span("inner"):
        pass

    assert tracer.names() == ["outer", "inner"]
    assert all(s.status == "ok" for s in tracer.spans)


def test_span_end_is_idempotent() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    recorded = tracer.start_span("once")
    recorded.end()
    first_end = tracer.spans[0].end_time
    recorded.end()  # second call should not overwrite
    assert tracer.spans[0].end_time == first_end


def test_duration_ms_is_none_before_end() -> None:
    tracer = MemoryTracer()
    set_tracer(tracer)

    tracer.start_span("still_open")
    assert tracer.spans[0].duration_ms is None

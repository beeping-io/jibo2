"""Secret + config loader for Jibo2.

Single entry point: ``from jibo2 import get_secret``.

Lookup order (first hit wins):

1. Sources registered via :func:`set_sources`. Default chain contains a
   single :class:`EnvSecretSource`.
2. :class:`EnvSecretSource` reads ``os.environ``. On first call it lazy-
   loads ``.env`` from the current working directory (if present) so
   copying ``.env.example → .env`` is enough to bootstrap — no extra
   tool required.

Resolutions are cached for 5 minutes (configurable with
:func:`set_ttl`). The cache is keyed by secret name and covers misses
as well so repeated lookups on missing keys stay cheap.

A follow-up task (J2-92) registers a ``FirebaseSecretManagerSource``
ahead of ``EnvSecretSource`` in prod once F0:M5 provisions the Firebase
projects. The API surface does not change.
"""

from __future__ import annotations

import os
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable


class SecretNotFoundError(KeyError):
    """Raised when a secret has no value and no default was provided."""


@runtime_checkable
class SecretSource(Protocol):
    """A source of secrets. Return ``None`` to fall through to the next source."""

    def get(self, name: str) -> str | None: ...


class EnvSecretSource:
    """Reads secrets from ``os.environ``.

    Lazy-loads ``.env`` (path configurable; default is ``cwd / .env``)
    the first time ``get`` is called. An env var already set in the
    process wins over the ``.env`` value so Docker / shell exports
    remain authoritative.
    """

    def __init__(self, dotenv_path: Path | None = None) -> None:
        self._dotenv_loaded = False
        self._dotenv_path = dotenv_path if dotenv_path is not None else Path.cwd() / ".env"

    def _lazy_load_dotenv(self) -> None:
        if self._dotenv_loaded:
            return
        self._dotenv_loaded = True
        if not self._dotenv_path.exists():
            return
        try:
            content = self._dotenv_path.read_text(encoding="utf-8")
        except OSError:
            return
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if not key:
                continue
            os.environ.setdefault(key, value)

    def get(self, name: str) -> str | None:
        self._lazy_load_dotenv()
        return os.environ.get(name)


@dataclass
class _CachedValue:
    value: str | None
    expires_at: float


@dataclass
class _SecretRegistry:
    sources: list[SecretSource] = field(default_factory=lambda: [EnvSecretSource()])
    ttl_seconds: float = 300.0
    _cache: dict[str, _CachedValue] = field(default_factory=dict)

    def clear_cache(self) -> None:
        self._cache.clear()

    def set_sources(self, sources: Iterable[SecretSource]) -> None:
        self.sources = list(sources)
        self.clear_cache()

    def set_ttl(self, seconds: float) -> None:
        self.ttl_seconds = seconds
        self.clear_cache()

    def lookup(self, name: str) -> str | None:
        now = time.monotonic()
        cached = self._cache.get(name)
        if cached is not None and cached.expires_at > now:
            return cached.value

        for source in self.sources:
            value = source.get(name)
            if value is not None:
                self._cache[name] = _CachedValue(value=value, expires_at=now + self.ttl_seconds)
                return value

        self._cache[name] = _CachedValue(value=None, expires_at=now + self.ttl_seconds)
        return None


_registry = _SecretRegistry()


def get_secret(name: str, *, default: str | None = None) -> str:
    """Resolve a secret by name.

    Returns the value from the first source that knows the key, or
    ``default`` if none do. Raises :class:`SecretNotFoundError` when the
    secret is missing and no default is supplied.
    """
    value = _registry.lookup(name)
    if value is not None:
        return value
    if default is not None:
        return default
    raise SecretNotFoundError(name)


def set_sources(sources: Iterable[SecretSource]) -> None:
    """Replace the global source chain. Clears the cache."""
    _registry.set_sources(sources)


def set_ttl(seconds: float) -> None:
    """Override the cache TTL (seconds). Clears the cache."""
    _registry.set_ttl(seconds)


def clear_cache() -> None:
    """Drop every cached entry — next lookup hits the sources again."""
    _registry.clear_cache()

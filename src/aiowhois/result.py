from __future__ import annotations

import typing
from collections import UserDict

from .tld import TLD


@typing.runtime_checkable
class Parseable(typing.Protocol):
    def parse(self, out: bytes) -> None: ...
    def as_dict(self) -> dict[str, str]: ...


_tld_registry: dict[str, typing.Type[Parseable]] = {}


def register(*tlds: str):
    """register is a decorator factory that can be provided to
    result classes to have them automatically registered for lookup
    later based on the domain being handled."""

    def decorator(cls):
        for tld in tlds:
            _tld_registry[tld.lower()] = cls
        return cls

    return decorator


class Base(UserDict): ...


@register(TLD.COM)
class WhoIsCom(Base):
    """WhoIsCom is used for parsing a"""

    def parse(self, out: bytes) -> None: ...

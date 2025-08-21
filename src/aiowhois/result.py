from __future__ import annotations


class WhoisResult:
    """WhoisResult encapsulates a whois query result"""

    def __init__(self) -> None: ...

    @classmethod
    def from_bytes(cls, b: bytes) -> WhoisResult:
        return cls()

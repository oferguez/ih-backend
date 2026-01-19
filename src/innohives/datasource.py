from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass(frozen=True)
class MessageRow:
    """Represents one message row from the source table."""

    message_id: int
    dt_published: str
    translated_content: str
    channel_name: str
    channel_id: int


class MessageSource(Protocol):
    """Protocol for message sources used by analysis logic."""

    def iter_messages(self) -> Iterable[MessageRow]:
        """Yield messages as rows from the backing store."""


@dataclass(frozen=True)
class InMemoryMessageSource:
    """Simple in-memory source for tests and local mocking."""

    rows: tuple[MessageRow, ...]

    def iter_messages(self) -> Iterable[MessageRow]:
        return self.rows

from __future__ import annotations

from typing import Protocol


class Vectorizer(Protocol):
    """Minimal interface needed from the vectorizer."""

    def fit_transform(self, documents: list[str]):  # type: ignore[no-untyped-def]
        """Build the term-document matrix."""

    def get_feature_names_out(self) -> list[str]:
        """Return vocabulary terms for the last fit."""

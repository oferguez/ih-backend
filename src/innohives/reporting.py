from __future__ import annotations

from dataclasses import dataclass

from .subjects import MonthlySubjectsResult


@dataclass(frozen=True)
class SubjectDelta:
    subject: str
    month_a_count: int
    month_b_count: int
    delta: int

    def as_dict(self, month_a_label: str, month_b_label: str) -> dict[str, int | str]:
        return {
            "subject": self.subject,
            month_a_label: self.month_a_count,
            month_b_label: self.month_b_count,
            "delta": self.delta,
        }


@dataclass(frozen=True)
class SubjectDeltaReporter:
    """Builds subject delta reports between two months."""

    def compare(
        self,
        results: list[MonthlySubjectsResult],
        month_a: str,
        month_b: str,
        month_a_label: str,
        month_b_label: str,
        top_n: int = 30,
        bottom_n: int = 30,
    ) -> list[dict[str, int | str]]:
        month_map = {result.month: result.subjects for result in results}
        subjects_a = month_map.get(month_a, {})
        subjects_b = month_map.get(month_b, {})

        all_subjects = set(subjects_a) | set(subjects_b)
        deltas: list[SubjectDelta] = []
        for subject in all_subjects:
            count_a = subjects_a.get(subject, 0)
            count_b = subjects_b.get(subject, 0)
            deltas.append(
                SubjectDelta(
                    subject=subject,
                    month_a_count=count_a,
                    month_b_count=count_b,
                    delta=count_b - count_a,
                )
            )

        deltas.sort(key=lambda item: (-item.delta, item.subject))
        if top_n == 0 or bottom_n == 0:
            combined = deltas
        else:
            top = deltas[:top_n] if top_n > 0 else []
            bottom = deltas[-bottom_n:] if bottom_n > 0 else []
            if bottom:
                bottom = list(reversed(bottom))
            combined = top + [item for item in bottom if item not in top]
        return [item.as_dict(month_a_label, month_b_label) for item in combined]

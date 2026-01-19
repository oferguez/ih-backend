from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from innohives.analyse_trends import TrendAnalysisRunner
from innohives.subjects import MonthlySubjectsResult


class FakeAnalyzer:
    def __init__(self, results: list[MonthlySubjectsResult]) -> None:
        self._results = results
        self.called = False

    def run(self) -> list[MonthlySubjectsResult]:
        self.called = True
        return self._results


class FakeReporter:
    def __init__(self, payload: list[dict[str, int | str]]) -> None:
        self._payload = payload
        self.calls: list[dict[str, Any]] = []

    def compare(
        self,
        *,
        results: list[MonthlySubjectsResult],
        month_a: str,
        month_b: str,
        month_a_label: str,
        month_b_label: str,
        top_n: int,
        bottom_n: int,
    ) -> list[dict[str, int | str]]:
        self.calls.append(
            {
                "results": results,
                "month_a": month_a,
                "month_b": month_b,
                "month_a_label": month_a_label,
                "month_b_label": month_b_label,
                "top_n": top_n,
                "bottom_n": bottom_n,
            }
        )
        return self._payload


class FakeTrendStorage:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def replace_trend_deltas(
        self,
        subject_trends: list[dict[str, int | str]],
        *,
        month_a: str,
        month_b: str,
        month_a_label: str,
        month_b_label: str,
    ) -> None:
        self.calls.append(
            {
                "subject_trends": subject_trends,
                "month_a": month_a,
                "month_b": month_b,
                "month_a_label": month_a_label,
                "month_b_label": month_b_label,
            }
        )


def test_trend_analysis_runner_writes_payload_and_calls_storage(tmp_path: Path) -> None:
    results = [
        MonthlySubjectsResult(month="2025-09", subjects={"alpha": 2}),
        MonthlySubjectsResult(month="2025-12", subjects={"alpha": 5}),
    ]
    payload = [
        {"subject": "alpha", "sept": 2, "dec": 5, "delta": 3},
    ]
    analyzer = FakeAnalyzer(results)
    reporter = FakeReporter(payload)
    storage = FakeTrendStorage()
    output_path = tmp_path / "trends.json"

    runner = TrendAnalysisRunner(
        analyzer=analyzer,
        reporter=reporter,
        trend_storage=storage,
        logger=logging.getLogger("test"),
        output_path=str(output_path),
    )

    runner.run(
        month_a="2025-09",
        month_b="2025-12",
        month_a_label="sept",
        month_b_label="dec",
        top_n=100,
        bottom_n=100,
    )

    assert analyzer.called is True
    assert len(reporter.calls) == 1
    assert reporter.calls[0]["month_a"] == "2025-09"
    assert reporter.calls[0]["month_b"] == "2025-12"
    assert len(storage.calls) == 1
    assert storage.calls[0]["subject_trends"] == payload
    assert storage.calls[0]["month_a_label"] == "sept"
    assert storage.calls[0]["month_b_label"] == "dec"

    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded == payload

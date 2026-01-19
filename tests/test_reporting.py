from __future__ import annotations

from innohives.reporting import SubjectDeltaReporter
from innohives.subjects import MonthlySubjectsResult


def test_compare_subjects_by_month_sorts_by_delta_desc() -> None:
    results = [
        MonthlySubjectsResult(
            month="2025-09",
            subjects={"alpha": 5, "beta": 2},
        ),
        MonthlySubjectsResult(
            month="2025-12",
            subjects={"alpha": 9, "gamma": 3},
        ),
    ]

    reporter = SubjectDeltaReporter()
    output = reporter.compare(
        results=results,
        month_a="2025-09",
        month_b="2025-12",
        month_a_label="sept",
        month_b_label="dec",
    )

    assert output[0]["subject"] == "alpha"
    assert output[0]["sept"] == 5
    assert output[0]["dec"] == 9
    assert output[0]["delta"] == 4
    assert output[1]["subject"] == "gamma"
    assert output[1]["sept"] == 0
    assert output[1]["dec"] == 3
    assert output[1]["delta"] == 3
    assert output[2]["subject"] == "beta"
    assert output[2]["sept"] == 2
    assert output[2]["dec"] == 0
    assert output[2]["delta"] == -2


def test_compare_subjects_by_month_limits_top_and_bottom() -> None:
    results = [
        MonthlySubjectsResult(
            month="2025-09",
            subjects={"alpha": 5, "beta": 2, "gamma": 1},
        ),
        MonthlySubjectsResult(
            month="2025-12",
            subjects={"alpha": 9, "beta": 1, "delta": 4},
        ),
    ]

    reporter = SubjectDeltaReporter()
    output = reporter.compare(
        results=results,
        month_a="2025-09",
        month_b="2025-12",
        month_a_label="sept",
        month_b_label="dec",
        top_n=1,
        bottom_n=1,
    )

    assert len(output) == 2
    assert output[0]["subject"] == "alpha"
    assert output[0]["delta"] == 4
    assert output[1]["subject"] == "gamma"
    assert output[1]["delta"] == -1

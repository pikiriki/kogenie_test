from models import (
    PerformanceComparison,
    PerformanceContext,
)


def absolute_change(
    current: float | None,
    baseline: float | None,
) -> float | None:

    if current is None:
        return None

    if baseline is None:
        return None

    return current - baseline


def relative_change_percent(
    current: float | None,
    baseline: float | None,
) -> float | None:

    if current is None:
        return None

    if baseline is None:
        return None

    if baseline == 0:
        return None

    return (
        (current - baseline)
        / baseline
        * 100
    )


def compare_performance(
    context: PerformanceContext,
) -> PerformanceComparison:

    if (
        not context.baseline_metrics
        or context.comparison_type
        == "no_valid_baseline"
    ):

        return PerformanceComparison(
            baseline_available=False,

            ctr_absolute_change=None,
            ctr_relative_change_pct=None,

            cpc_absolute_change=None,
            cpc_relative_change_pct=None,

            conversion_rate_absolute_change=None,
            conversion_rate_relative_change_pct=None,

            cpa_absolute_change=None,
            cpa_relative_change_pct=None,

            roas_absolute_change=None,
            roas_relative_change_pct=None,

            available_comparisons=[],

            comparison_boundary=(
                context.comparison_boundaries
                + [
                    (
                        "Performance change cannot "
                        "be calculated because no "
                        "valid baseline is available."
                    )
                ]
            ),
        )

    current = (
        context.current_metrics
    )

    baseline = (
        context.baseline_metrics
    )

    ctr_absolute = absolute_change(
        current.ctr,
        baseline.ctr,
    )

    ctr_relative = (
        relative_change_percent(
            current.ctr,
            baseline.ctr,
        )
    )

    cpc_absolute = absolute_change(
        current.cpc,
        baseline.cpc,
    )


    cpc_relative = (
        relative_change_percent(
            current.cpc,
            baseline.cpc,
        )
    )

    conversion_rate_absolute = (
        absolute_change(
            current.conversion_rate,
            baseline.conversion_rate,
        )
    )


    conversion_rate_relative = (
        relative_change_percent(
            current.conversion_rate,
            baseline.conversion_rate,
        )
    )

    cpa_absolute = absolute_change(
        current.cpa,
        baseline.cpa,
    )


    cpa_relative = (
        relative_change_percent(
            current.cpa,
            baseline.cpa,
        )
    )

    roas_absolute = absolute_change(
        current.roas,
        baseline.roas,
    )


    roas_relative = (
        relative_change_percent(
            current.roas,
            baseline.roas,
        )
    )

    available_comparisons = []

    metric_pairs = {
        "ctr": (
            current.ctr,
            baseline.ctr,
        ),
        "cpc": (
            current.cpc,
            baseline.cpc,
        ),
        "conversion_rate": (
            current.conversion_rate,
            baseline.conversion_rate,
        ),
        "cpa": (
            current.cpa,
            baseline.cpa,
        ),
        "roas": (
            current.roas,
            baseline.roas,
        ),
    }

    for name, values in (
        metric_pairs.items()
    ):

        current_value = values[0]
        baseline_value = values[1]

        if (
            current_value is not None
            and baseline_value is not None
        ):

            available_comparisons.append(
                name
            )

    comparison_boundary = list(
        context.comparison_boundaries
    )

    comparison_boundary.append(
        (
            "Absolute change is calculated as "
            "current minus baseline."
        )
    )

    comparison_boundary.append(
        (
            "Relative change is calculated as "
            "(current - baseline) / baseline."
        )
    )

    comparison_boundary.append(
        (
            "Relative change is unavailable when "
            "the baseline value is zero."
        )
    )

    comparison_boundary.append(
        (
            "Metric change is descriptive. "
            "It does not establish that the "
            "campaign strategy, copy, visual, "
            "or any other individual element "
            "caused the observed difference."
        )
    )

    return PerformanceComparison(
        baseline_available=True,

        ctr_absolute_change=(
            ctr_absolute
        ),
        ctr_relative_change_pct=(
            ctr_relative
        ),

        cpc_absolute_change=(
            cpc_absolute
        ),
        cpc_relative_change_pct=(
            cpc_relative
        ),

        conversion_rate_absolute_change=(
            conversion_rate_absolute
        ),
        conversion_rate_relative_change_pct=(
            conversion_rate_relative
        ),

        cpa_absolute_change=(
            cpa_absolute
        ),
        cpa_relative_change_pct=(
            cpa_relative
        ),

        roas_absolute_change=(
            roas_absolute
        ),
        roas_relative_change_pct=(
            roas_relative
        ),

        available_comparisons=(
            available_comparisons
        ),

        comparison_boundary=(
            comparison_boundary
        ),
    )


def format_signed_number(
    value: float | None,
    suffix: str = "",
) -> str:

    if value is None:
        return "N/A"

    return (
        f"{value:+.2f}"
        f"{suffix}"
    )


def format_relative_change(
    value: float | None,
) -> str:

    if value is None:
        return "N/A"

    return f"{value:+.2f}%"


def format_percentage_point_change(
    value: float | None,
) -> str:

    if value is None:
        return "N/A"

    return (
        f"{value * 100:+.2f} "
        "percentage points"
    )

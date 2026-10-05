from datetime import date

from models import (
    OutcomeEvidenceSnapshot,
    PerformanceContext,
)


def normalize_text(
    value: str,
) -> str:

    return " ".join(
        value
        .strip()
        .lower()
        .split()
    )


def measurement_days(
    snapshot: OutcomeEvidenceSnapshot,
) -> int:

    start = date.fromisoformat(
        snapshot.raw_outcome.measured_from
    )

    end = date.fromisoformat(
        snapshot.raw_outcome.measured_to
    )

    return (
        end - start
    ).days + 1


def previous_period_exclusion_reasons(
    current: OutcomeEvidenceSnapshot,
    candidate: OutcomeEvidenceSnapshot,
) -> list[str]:

    reasons = []

    current_id = (
        current.raw_outcome.id
    )

    candidate_id = (
        candidate.raw_outcome.id
    )


    if (
        current_id is not None
        and candidate_id is not None
        and current_id == candidate_id
    ):

        reasons.append(
            "This is the current outcome itself."
        )

    if (
        current.raw_outcome.campaign_id
        != candidate.raw_outcome.campaign_id
    ):

        reasons.append(
            "Campaign IDs differ."
        )

    if normalize_text(
        current.raw_outcome.channel
    ) != normalize_text(
        candidate.raw_outcome.channel
    ):

        reasons.append(
            (
                "Channels differ: "
                f"{candidate.raw_outcome.channel} "
                "vs "
                f"{current.raw_outcome.channel}."
            )
        )

    if normalize_text(
        current.conversion_definition
    ) != normalize_text(
        candidate.conversion_definition
    ):

        reasons.append(
            (
                "Conversion definitions differ: "
                f"{candidate.conversion_definition} "
                "vs "
                f"{current.conversion_definition}."
            )
        )

    if normalize_text(
        current.attribution_context
    ) != normalize_text(
        candidate.attribution_context
    ):

        reasons.append(
            "Attribution contexts differ."
        )

    if (
        current.source_quality
        != candidate.source_quality
    ):

        reasons.append(
            (
                "Source-quality labels differ: "
                f"{candidate.source_quality} "
                "vs "
                f"{current.source_quality}."
            )
        )

    current_days = measurement_days(
        current
    )

    candidate_days = measurement_days(
        candidate
    )


    if current_days != candidate_days:

        reasons.append(
            (
                "Measurement-window lengths differ: "
                f"{candidate_days} days vs "
                f"{current_days} days."
            )
        )

    current_start = date.fromisoformat(
        current.raw_outcome.measured_from
    )

    candidate_end = date.fromisoformat(
        candidate.raw_outcome.measured_to
    )


    if candidate_end >= current_start:

        reasons.append(
            (
                "Candidate outcome does not end "
                "before the current measurement "
                "window begins."
            )
        )

    return reasons


def build_performance_context(
    current_snapshot: OutcomeEvidenceSnapshot,
    historical_snapshots: list[
        OutcomeEvidenceSnapshot
    ],
    campaign_objective: str,
) -> PerformanceContext:

    campaign_objective = (
        campaign_objective.strip()
    )


    if not campaign_objective:

        raise ValueError(
            "Campaign objective cannot be empty."
        )

    comparable = []

    non_comparable = []

    for candidate in historical_snapshots:

        reasons = (
            previous_period_exclusion_reasons(
                current=current_snapshot,
                candidate=candidate,
            )
        )

        if reasons:

            outcome_id = (
                candidate.raw_outcome.id
            )

            label = (
                f"Outcome {outcome_id}"
                if outcome_id is not None
                else "Unsaved candidate outcome"
            )

            non_comparable.append(
                (
                    label
                    + " excluded: "
                    + " ".join(reasons)
                )
            )

            continue

        comparable.append(
            candidate
        )

    if not comparable:

        return PerformanceContext(
            campaign_objective=(
                campaign_objective
            ),

            comparison_type=(
                "no_valid_baseline"
            ),

            current_snapshot=(
                current_snapshot
            ),

            comparable_outcomes=[],

            non_comparable_outcomes=(
                non_comparable
            ),

            baseline_metrics=None,

            current_metrics=(
                current_snapshot
                .derived_metrics
            ),

            comparison_boundaries=[
                (
                    "No historical outcome passed "
                    "the current comparability rules."
                ),
                (
                    "Do not label current performance "
                    "as improved or declined without "
                    "a valid baseline."
                ),
                (
                    "Do not substitute an industry "
                    "benchmark automatically."
                ),
                (
                    "Current metrics remain descriptive "
                    "observations, not causal conclusions."
                ),
            ],
        )

    baseline = max(
        comparable,
        key=lambda snapshot: (
            date.fromisoformat(
                snapshot
                .raw_outcome
                .measured_to
            )
        ),
    )

    comparison_boundaries = [
        (
            "The baseline is the most recent "
            "historical outcome that passed the "
            "current previous-period comparability rules."
        ),
        (
            "Comparison requires the same campaign, "
            "channel, conversion definition, attribution "
            "context, source-quality label, and "
            "measurement-window length."
        ),
        (
            "The comparison is descriptive. "
            "It does not prove that copy, visual, angle, "
            "budget, or another campaign element caused "
            "any metric difference."
        ),
        (
            "Audience composition, placement delivery, "
            "auction conditions, seasonality, and other "
            "unrecorded conditions may still differ."
        ),
        (
            "Do not generalize a period-over-period "
            "difference into a universal performance claim."
        ),
    ]

    return PerformanceContext(
        campaign_objective=(
            campaign_objective
        ),

        comparison_type=(
            "previous_period"
        ),

        current_snapshot=(
            current_snapshot
        ),

        comparable_outcomes=(
            comparable
        ),

        non_comparable_outcomes=(
            non_comparable
        ),

        baseline_metrics=(
            baseline.derived_metrics
        ),

        current_metrics=(
            current_snapshot
            .derived_metrics
        ),

        comparison_boundaries=(
            comparison_boundaries
        ),
    )

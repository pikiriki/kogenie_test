from models import (
    CreativeEvidenceLedger,
    CreativeEvidenceObservation,
    CreativeOutcomeLink,
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


SUPPORTED_METRICS = {
    "ctr",
    "cpc",
    "conversion_rate",
    "cpa",
    "roas",
}


DIRECTIONS = {
    "higher",
    "lower",
}


def get_metric_changes(
    link: CreativeOutcomeLink,
    metric_name: str,
) -> tuple[
    float | None,
    float | None,
]:

    if metric_name not in SUPPORTED_METRICS:

        raise ValueError(
            f"Unsupported metric: {metric_name}"
        )

    comparison = (
        link.performance_comparison
    )

    fields = {
        "ctr": (
            comparison.ctr_absolute_change,
            comparison.ctr_relative_change_pct,
        ),

        "cpc": (
            comparison.cpc_absolute_change,
            comparison.cpc_relative_change_pct,
        ),

        "conversion_rate": (
            comparison
            .conversion_rate_absolute_change,

            comparison
            .conversion_rate_relative_change_pct,
        ),

        "cpa": (
            comparison.cpa_absolute_change,
            comparison.cpa_relative_change_pct,
        ),

        "roas": (
            comparison.roas_absolute_change,
            comparison.roas_relative_change_pct,
        ),
    }

    return fields[
        metric_name
    ]


def classify_direction(
    absolute_change: float,
    desired_direction: str,
) -> str:

    if desired_direction not in DIRECTIONS:

        raise ValueError(
            (
                "Desired direction must be "
                "'higher' or 'lower'."
            )
        )

    if absolute_change == 0:

        return "neutral"

    if desired_direction == "higher":

        if absolute_change > 0:
            return "supports"

        return "contradicts"

    if absolute_change < 0:
        return "supports"

    return "contradicts"


def build_angle_evidence_ledger(
    links: list[CreativeOutcomeLink],
    approved_angle: str,
    metric_name: str,
    desired_direction: str,
    channel: str,
    conversion_definition: str,
    attribution_context: str,
    source_quality: str,
) -> CreativeEvidenceLedger:

    if metric_name not in SUPPORTED_METRICS:

        raise ValueError(
            f"Unsupported metric: {metric_name}"
        )

    if desired_direction not in DIRECTIONS:

        raise ValueError(
            (
                "Desired direction must be "
                "'higher' or 'lower'."
            )
        )

    approved_angle = (
        approved_angle.strip()
    )

    if not approved_angle:

        raise ValueError(
            "Approved angle cannot be empty."
        )

    creative_key = (
        "angle: "
        + approved_angle
    )

    observations = []

    supporting = []

    contradicting = []

    neutral = []

    incomparable = []

    for link in links:

        if normalize_text(
            link.approved_angle
        ) != normalize_text(
            approved_angle
        ):

            continue

        reasons = []

        if normalize_text(
            link.outcome_channel
        ) != normalize_text(
            channel
        ):

            reasons.append(
                (
                    "Channel differs: "
                    f"{link.outcome_channel} "
                    f"vs {channel}."
                )
            )

        snapshot = (
            link.outcome_snapshot
        )

        if normalize_text(
            snapshot.conversion_definition
        ) != normalize_text(
            conversion_definition
        ):

            reasons.append(
                "Conversion definition differs."
            )

        if normalize_text(
            snapshot.attribution_context
        ) != normalize_text(
            attribution_context
        ):

            reasons.append(
                "Attribution context differs."
            )

        if (
            snapshot.source_quality
            != source_quality
        ):

            reasons.append(
                (
                    "Source quality differs: "
                    f"{snapshot.source_quality} "
                    f"vs {source_quality}."
                )
            )

        if not (
            link
            .performance_comparison
            .baseline_available
        ):

            reasons.append(
                "No valid performance baseline."
            )

        (
            absolute_change,
            relative_change,
        ) = get_metric_changes(
            link,
            metric_name,
        )

        if absolute_change is None:

            reasons.append(
                (
                    f"{metric_name} absolute "
                    "change is unavailable."
                )
            )

        if reasons:

            identifier = (
                f"Campaign {link.campaign_id}, "
                f"Outcome {link.outcome_id}"
            )

            incomparable.append(
                (
                    identifier
                    + " excluded: "
                    + " ".join(reasons)
                )
            )

            continue

        direction = classify_direction(
            absolute_change=absolute_change,
            desired_direction=(
                desired_direction
            ),
        )

        observation = (
            CreativeEvidenceObservation(
                campaign_id=(
                    link.campaign_id
                ),

                outcome_id=(
                    link.outcome_id
                ),

                channel=(
                    link.outcome_channel
                ),

                metric_name=(
                    metric_name
                ),

                absolute_change=(
                    absolute_change
                ),

                relative_change_pct=(
                    relative_change
                ),

                direction=direction,

                source_quality=(
                    snapshot.source_quality
                ),
            )
        )

        observations.append(
            observation
        )

        if direction == "supports":

            supporting.append(
                observation
            )

        elif direction == "contradicts":

            contradicting.append(
                observation
            )

        else:

            neutral.append(
                observation
            )

    comparable_count = len(
        observations
    )

    support_count = len(
        supporting
    )

    contradict_count = len(
        contradicting
    )

    neutral_count = len(
        neutral
    )

    if comparable_count == 0:

        repeated_pattern = (
            "No comparable historical observations "
            "are available for this creative key "
            "and metric question."
        )

    elif comparable_count == 1:

        repeated_pattern = (
            "Only one comparable historical "
            "observation is available. A repeated "
            "pattern has not been established."
        )

    else:

        repeated_pattern = (
            f"Across {comparable_count} comparable "
            f"observations, {support_count} support "
            f"the '{desired_direction} {metric_name}' "
            f"direction, {contradict_count} contradict "
            f"it, and {neutral_count} are neutral."
        )

    if comparable_count < 2:

        evidence_strength = (
            "insufficient"
        )

    elif (
        support_count > 0
        and contradict_count > 0
    ):

        evidence_strength = (
            "mixed"
        )

    elif (
        comparable_count < 4
        and support_count > 0
        and contradict_count == 0
    ):

        evidence_strength = (
            "emerging"
        )

    elif (
        comparable_count >= 4
        and support_count
        / comparable_count
        >= 0.75
        and contradict_count == 0
    ):

        evidence_strength = (
            "repeated_association"
        )

    else:

        evidence_strength = (
            "mixed"
        )

    learning_boundary = [
        (
            "This ledger summarizes repeated "
            "historical association, not causal effect."
        ),
        (
            "Supporting observations mean the selected "
            "metric moved in the hypothesized direction "
            "relative to each observation's own valid "
            "baseline."
        ),
        (
            "Contradicting observations are preserved "
            "and must not be hidden when evaluating "
            "the creative pattern."
        ),
        (
            "Only observations matching the selected "
            "channel, conversion definition, attribution "
            "context, and source-quality class are treated "
            "as comparable."
        ),
        (
            "The evidence-strength label is an engineering "
            "heuristic for organizing history. It is not "
            "a statistical significance test."
        ),
        (
            "Repeated association does not prove that "
            "the creative angle caused the metric change."
        ),
        (
            "CreativeOutcomeLink itself may represent "
            "campaign-level association rather than "
            "verified execution-level deployment."
        ),
        (
            "Do not convert this ledger directly into "
            "an advertising performance claim."
        ),
    ]

    return CreativeEvidenceLedger(
        creative_key=creative_key,

        metric_name=metric_name,

        desired_direction=(
            desired_direction
        ),

        channel=channel,

        conversion_definition=(
            conversion_definition
        ),

        attribution_context=(
            attribution_context
        ),

        source_quality=(
            source_quality
        ),

        observations=observations,

        supporting_observations=(
            supporting
        ),

        contradicting_observations=(
            contradicting
        ),

        neutral_observations=neutral,

        incomparable_observations=(
            incomparable
        ),

        repeated_pattern=(
            repeated_pattern
        ),

        evidence_strength=(
            evidence_strength
        ),

        learning_boundary=(
            learning_boundary
        ),
    )

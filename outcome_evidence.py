from models import (
    CampaignOutcome,
    OutcomeEvidenceSnapshot,
)

from campaign_metrics import (
    derive_campaign_metrics,
)

from outcome_data import (
    validate_campaign_outcome,
)


def build_outcome_evidence_snapshot(
    outcome: CampaignOutcome,
    conversion_definition: str,
    attribution_context: str,
    known_gaps: list[str],
) -> OutcomeEvidenceSnapshot:

    validate_campaign_outcome(
        outcome
    )

    conversion_definition = (
        conversion_definition.strip()
    )


    if not conversion_definition:

        raise ValueError(
            "Conversion definition cannot be empty."
        )

    attribution_context = (
        attribution_context.strip()
    )


    if not attribution_context:

        raise ValueError(
            "Attribution context cannot be empty."
        )

    cleaned_gaps = []

    for gap in known_gaps:

        cleaned = gap.strip()

        if not cleaned:
            continue

        if cleaned not in cleaned_gaps:

            cleaned_gaps.append(
                cleaned
            )

    metrics = derive_campaign_metrics(
        outcome
    )

    interpretation_boundary = []

    interpretation_boundary.append(
        (
            "Treat impressions, clicks, conversions, "
            "spend, and revenue as observations "
            "reported by the stated source for the "
            "specified measurement window."
        )
    )

    interpretation_boundary.append(
        (
            "CTR, CPC, conversion rate, CPA, and ROAS "
            "are deterministic calculations derived "
            "from the supplied raw outcome values."
        )
    )

    interpretation_boundary.append(
        (
            "Treat conversions and revenue according "
            "to this attribution context only: "
            + attribution_context
        )
    )

    interpretation_boundary.append(
        (
            "Do not infer that the campaign, copy, "
            "visual, angle, or any individual creative "
            "element caused the observed outcome "
            "without additional causal evidence."
        )
    )

    interpretation_boundary.append(
        (
            "Do not assume this observed result will "
            "repeat in another audience, channel, "
            "budget, time period, or campaign."
        )
    )

    if outcome.data_quality == "manual":

        interpretation_boundary.append(
            (
                "The data was manually entered. "
                "Do not describe it as independently "
                "verified platform data."
            )
        )

    if outcome.data_quality == "estimated":

        interpretation_boundary.append(
            (
                "At least part of the outcome is "
                "estimated. Avoid presenting derived "
                "metrics as exact measurements."
            )
        )

    if outcome.data_quality == "incomplete":

        interpretation_boundary.append(
            (
                "The outcome record is known to be "
                "incomplete. Do not treat the metrics "
                "as a complete representation of "
                "campaign performance."
            )
        )

    for gap in cleaned_gaps:

        interpretation_boundary.append(
            (
                "Known limitation: "
                + gap
            )
        )

    return OutcomeEvidenceSnapshot(
        raw_outcome=outcome,

        derived_metrics=metrics,

        conversion_definition=(
            conversion_definition
        ),

        attribution_context=(
            attribution_context
        ),

        source_quality=(
            outcome.data_quality
        ),

        known_gaps=cleaned_gaps,

        interpretation_boundary=(
            interpretation_boundary
        ),
    )

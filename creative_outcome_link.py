from models import (
    CampaignMemory,
    CreativeOutcomeLink,
    OutcomeEvidenceSnapshot,
    PerformanceAnalysis,
    PerformanceComparison,
    VisualAsset,
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


def dedupe_strings(
    items: list[str],
) -> list[str]:

    result = []

    seen = set()

    for item in items:

        cleaned = item.strip()

        if not cleaned:
            continue

        if cleaned in seen:
            continue

        seen.add(cleaned)
        result.append(cleaned)

    return result


def build_creative_outcome_link(
    campaign_memory: CampaignMemory,
    visual_assets: list[VisualAsset],
    outcome_snapshot: OutcomeEvidenceSnapshot,
    performance_comparison: PerformanceComparison,
    performance_analysis: PerformanceAnalysis,
) -> CreativeOutcomeLink:

    outcome = (
        outcome_snapshot.raw_outcome
    )

    if (
        campaign_memory.campaign_id
        != outcome.campaign_id
    ):

        raise ValueError(
            (
                "CampaignMemory and outcome "
                "belong to different campaigns."
            )
        )

    campaign_assets = [
        asset

        for asset in visual_assets

        if (
            asset.campaign_id
            == outcome.campaign_id
        )
    ]

    channel_assets = [
        asset

        for asset in campaign_assets

        if normalize_text(
            asset.channel
        ) == normalize_text(
            outcome.channel
        )
    ]

    visual_asset_ids = []

    for asset in channel_assets:

        if asset.id is None:
            continue

        if (
            asset.id
            not in visual_asset_ids
        ):

            visual_asset_ids.append(
                asset.id
            )

    if visual_asset_ids:

        relationship_status = (
            "campaign_strategy_and_"
            "channel_visual_context"
        )

    else:

        relationship_status = (
            "campaign_strategy_context"
        )

    causal_boundary = [
        (
            "This CreativeOutcomeLink records "
            "historical campaign association and "
            "does not establish causal effect."
        ),
        (
            "The approved campaign angle and Big Idea "
            "were part of the same campaign context "
            "as the measured outcome, but the outcome "
            "does not establish that either caused "
            "the measured performance."
        ),
    ]

    if visual_asset_ids:

        causal_boundary.append(
            (
                "The listed VisualAsset IDs are "
                "human-approved assets for the same "
                "campaign and channel. This does not "
                "prove that those exact visual files "
                "were deployed or served during the "
                "outcome measurement window."
            )
        )

    else:

        causal_boundary.append(
            (
                "No human-approved VisualAsset for "
                "the outcome channel is linked in "
                "the current visual asset library."
            )
        )

    causal_boundary.append(
        (
            "The current system does not include "
            "a platform creative ID, ad ID, deployment "
            "timestamp, or impression-level join that "
            "connects an approved visual artifact "
            "directly to delivered advertising events."
        )
    )

    causal_boundary.append(
        (
            "PerformanceAnalysis hypotheses remain "
            "hypotheses and must not be represented "
            "as proven explanations."
        )
    )

    causal_boundary.extend(
        outcome_snapshot
        .interpretation_boundary
    )

    causal_boundary = dedupe_strings(
        causal_boundary
    )

    return CreativeOutcomeLink(
        campaign_id=(
            outcome.campaign_id
        ),

        outcome_id=(
            outcome.id
        ),

        outcome_channel=(
            outcome.channel
        ),

        approved_angle=(
            campaign_memory.approved_angle
        ),

        approved_big_idea=(
            campaign_memory.approved_big_idea
        ),

        approved_visual_asset_ids=(
            visual_asset_ids
        ),

        outcome_snapshot=(
            outcome_snapshot
        ),

        performance_comparison=(
            performance_comparison
        ),

        performance_analysis=(
            performance_analysis
        ),

        relationship_status=(
            relationship_status
        ),

        causal_boundary=(
            causal_boundary
        ),
    )

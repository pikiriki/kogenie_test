from database import (
    get_campaign_outcomes,
    initialize_database,
)

from models import (
    CampaignOutcome,
)

from outcome_evidence import (
    build_outcome_evidence_snapshot,
)

from performance_context import (
    build_performance_context,
)


initialize_database()


# Campaign 1 is the campaign used in Lessons 101–103.
campaign_id = 1


outcomes = get_campaign_outcomes(
    campaign_id
)


if not outcomes:

    print(
        "\nNo current CampaignOutcome exists."
    )

    print(
        "Complete Lesson 101 first."
    )

    raise SystemExit


current_outcome = outcomes[0]


conversion_definition = (
    "Waitlist signup for this tutorial example."
)


attribution_context = (
    "Fictional Meta Ads Manager attribution "
    "for code testing only. No Shopify or "
    "backend conversion reconciliation was performed."
)


current_snapshot = (
    build_outcome_evidence_snapshot(
        outcome=current_outcome,

        conversion_definition=(
            conversion_definition
        ),

        attribution_context=(
            attribution_context
        ),

        known_gaps=[
            "The dataset is fictional tutorial data.",
            "No control group or holdout exists.",
            "No causal experiment was performed.",
        ],
    )
)


# Fictional tutorial fixtures — kept in memory only,
# never saved to SQLite.
previous_outcome = CampaignOutcome(
    campaign_id=campaign_id,

    channel="Meta",

    impressions=45000,
    clicks=900,
    conversions=27,

    spend=15000.0,
    revenue=37500.0,

    measured_from="2026-09-24",
    measured_to="2026-09-30",

    source=(
        "Fictional Meta prior-period "
        "data for code testing"
    ),

    data_quality="manual",
)


previous_snapshot = (
    build_outcome_evidence_snapshot(
        outcome=previous_outcome,

        conversion_definition=(
            conversion_definition
        ),

        attribution_context=(
            attribution_context
        ),

        known_gaps=[
            "The dataset is fictional tutorial data.",
            "No control group or holdout exists.",
            "No causal experiment was performed.",
        ],
    )
)


google_outcome = CampaignOutcome(
    campaign_id=campaign_id,

    channel="Google Search",

    impressions=20000,
    clicks=1400,
    conversions=45,

    spend=16000.0,
    revenue=60000.0,

    measured_from="2026-09-24",
    measured_to="2026-09-30",

    source=(
        "Fictional Google Ads "
        "data for code testing"
    ),

    data_quality="manual",
)


google_snapshot = (
    build_outcome_evidence_snapshot(
        outcome=google_outcome,

        conversion_definition=(
            conversion_definition
        ),

        attribution_context=(
            "Fictional Google Ads attribution "
            "for code testing only."
        ),

        known_gaps=[
            "The dataset is fictional tutorial data.",
        ],
    )
)


context = build_performance_context(
    current_snapshot=current_snapshot,

    historical_snapshots=[
        previous_snapshot,
        google_snapshot,
    ],

    campaign_objective=(
        "Generate waitlist signups"
    ),
)


print("=" * 70)
print("PERFORMANCE CONTEXT")
print("=" * 70)


print("\nCAMPAIGN OBJECTIVE")
print(
    context.campaign_objective
)


print("\nCOMPARISON TYPE")
print(
    context.comparison_type
)


print("\nCOMPARABLE OUTCOMES")


if context.comparable_outcomes:

    for snapshot in (
        context.comparable_outcomes
    ):

        outcome = snapshot.raw_outcome

        print(
            f"- {outcome.channel}: "
            f"{outcome.measured_from} "
            f"→ {outcome.measured_to}"
        )

else:

    print("- None")


print("\nNON-COMPARABLE OUTCOMES")


if context.non_comparable_outcomes:

    for reason in (
        context.non_comparable_outcomes
    ):

        print(f"- {reason}")

else:

    print("- None")


print("\nBASELINE METRICS")


baseline = context.baseline_metrics


if baseline is None:

    print("- No valid baseline")

else:

    print(
        "CTR:",
        (
            "N/A"
            if baseline.ctr is None
            else f"{baseline.ctr * 100:.2f}%"
        ),
    )

    print(
        "CPA:",
        (
            "N/A"
            if baseline.cpa is None
            else f"{baseline.cpa:.2f}"
        ),
    )

    print(
        "ROAS:",
        (
            "N/A"
            if baseline.roas is None
            else f"{baseline.roas:.2f}x"
        ),
    )


print("\nCURRENT METRICS")


current = context.current_metrics


print(
    "CTR:",
    (
        "N/A"
        if current.ctr is None
        else f"{current.ctr * 100:.2f}%"
    ),
)


print(
    "CPA:",
    (
        "N/A"
        if current.cpa is None
        else f"{current.cpa:.2f}"
    ),
)


print(
    "ROAS:",
    (
        "N/A"
        if current.roas is None
        else f"{current.roas:.2f}x"
    ),
)


print("\nCOMPARISON BOUNDARIES")


for boundary in (
    context.comparison_boundaries
):

    print(f"- {boundary}")


from performance_comparison import (
    compare_performance,
    format_percentage_point_change,
    format_relative_change,
    format_signed_number,
)


comparison = compare_performance(
    context
)


print("\n" + "=" * 70)
print("PERFORMANCE COMPARISON")
print("=" * 70)


print("\nBASELINE AVAILABLE")

print(
    comparison.baseline_available
)


if not comparison.baseline_available:

    print(
        "\nNo valid performance-change "
        "calculation can be made."
    )

    raise SystemExit


print("\nCTR")


print(
    "Absolute:",
    format_percentage_point_change(
        comparison
        .ctr_absolute_change
    ),
)


print(
    "Relative:",
    format_relative_change(
        comparison
        .ctr_relative_change_pct
    ),
)


print("\nCPC")


print(
    "Absolute:",
    format_signed_number(
        comparison
        .cpc_absolute_change
    ),
)


print(
    "Relative:",
    format_relative_change(
        comparison
        .cpc_relative_change_pct
    ),
)


print("\nCONVERSION RATE")


print(
    "Absolute:",
    format_percentage_point_change(
        comparison
        .conversion_rate_absolute_change
    ),
)


print(
    "Relative:",
    format_relative_change(
        comparison
        .conversion_rate_relative_change_pct
    ),
)


print("\nCPA")


print(
    "Absolute:",
    format_signed_number(
        comparison
        .cpa_absolute_change
    ),
)


print(
    "Relative:",
    format_relative_change(
        comparison
        .cpa_relative_change_pct
    ),
)


print("\nROAS")


print(
    "Absolute:",
    format_signed_number(
        comparison
        .roas_absolute_change,
        suffix="x",
    ),
)


print(
    "Relative:",
    format_relative_change(
        comparison
        .roas_relative_change_pct
    ),
)


print(
    "\nAVAILABLE COMPARISONS"
)


for metric in (
    comparison.available_comparisons
):

    print(f"- {metric}")


print(
    "\nCOMPARISON BOUNDARY"
)


for boundary in (
    comparison.comparison_boundary
):

    print(f"- {boundary}")


from performance_analyst import (
    analyze_performance,
)


print(
    "\nANALYZING PERFORMANCE...\n"
)


analysis = analyze_performance(
    snapshot=current_snapshot,
    context=context,
    comparison=comparison,
)


print("=" * 70)
print("PERFORMANCE ANALYSIS")
print("=" * 70)


print("\nOBSERVED CHANGES")


if analysis.observed_changes:

    for item in (
        analysis.observed_changes
    ):
        print(f"- {item}")

else:

    print("- None")


print(
    "\nSUPPORTED INTERPRETATIONS"
)


if (
    analysis
    .supported_interpretations
):

    for item in (
        analysis
        .supported_interpretations
    ):
        print(f"- {item}")

else:

    print("- None")


print(
    "\nUNSUPPORTED EXPLANATIONS"
)


if (
    analysis
    .unsupported_explanations
):

    for item in (
        analysis
        .unsupported_explanations
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nHYPOTHESES")


if analysis.hypotheses:

    for index, item in enumerate(
        analysis.hypotheses,
        start=1,
    ):

        print(
            f"{index}. {item}"
        )

else:

    print("- None")


print(
    "\nADDITIONAL EVIDENCE NEEDED"
)


if (
    analysis
    .additional_evidence_needed
):

    for item in (
        analysis
        .additional_evidence_needed
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nANALYSIS CONFIDENCE")

print(
    analysis.confidence
)


from creative_outcome_link import (
    build_creative_outcome_link,
)

from database import (
    get_campaign_memories,
    get_visual_assets,
)


memories = get_campaign_memories()


campaign_memory = next(
    (
        memory

        for memory in memories

        if (
            memory.campaign_id
            == campaign_id
        )
    ),
    None,
)


if campaign_memory is None:

    print(
        "\nNo approved CampaignMemory exists "
        f"for Campaign {campaign_id}."
    )

    print(
        "\nCreativeOutcomeLink was not created."
    )

    print(
        "\nReason:"
        "\nPerformance data should not be linked "
        "to an unapproved or fabricated creative "
        "history record."
    )

    raise SystemExit


visual_assets = get_visual_assets(
    campaign_id
)


print(
    "\nApproved visual assets found:",
    len(visual_assets),
)


creative_outcome_link = (
    build_creative_outcome_link(
        campaign_memory=(
            campaign_memory
        ),

        visual_assets=(
            visual_assets
        ),

        outcome_snapshot=(
            current_snapshot
        ),

        performance_comparison=(
            comparison
        ),

        performance_analysis=(
            analysis
        ),
    )
)


print("\n" + "=" * 70)
print("CREATIVE OUTCOME LINK")
print("=" * 70)


print("\nCAMPAIGN")
print(
    creative_outcome_link.campaign_id
)


print("\nOUTCOME ID")
print(
    creative_outcome_link.outcome_id
)


print("\nOUTCOME CHANNEL")
print(
    creative_outcome_link.outcome_channel
)


print("\nAPPROVED ANGLE")
print(
    creative_outcome_link.approved_angle
)


print("\nAPPROVED BIG IDEA")
print(
    creative_outcome_link
    .approved_big_idea
)


print(
    "\nAPPROVED VISUAL ASSET IDS"
)


if (
    creative_outcome_link
    .approved_visual_asset_ids
):

    for asset_id in (
        creative_outcome_link
        .approved_visual_asset_ids
    ):

        print(
            f"- Visual Asset {asset_id}"
        )

else:

    print("- None")


print(
    "\nRELATIONSHIP STATUS"
)

print(
    creative_outcome_link
    .relationship_status
)


print("\nOUTCOME METRICS")


metrics = (
    creative_outcome_link
    .outcome_snapshot
    .derived_metrics
)


print(
    "CTR:",
    (
        "N/A"
        if metrics.ctr is None
        else f"{metrics.ctr * 100:.2f}%"
    ),
)


print(
    "CPA:",
    (
        "N/A"
        if metrics.cpa is None
        else f"{metrics.cpa:.2f}"
    ),
)


print(
    "ROAS:",
    (
        "N/A"
        if metrics.roas is None
        else f"{metrics.roas:.2f}x"
    ),
)


print(
    "\nSUPPORTED INTERPRETATIONS"
)


for item in (
    creative_outcome_link
    .performance_analysis
    .supported_interpretations
):

    print(f"- {item}")


print("\nHYPOTHESES")


if (
    creative_outcome_link
    .performance_analysis
    .hypotheses
):

    for item in (
        creative_outcome_link
        .performance_analysis
        .hypotheses
    ):

        print(f"- {item}")

else:

    print("- None")


print("\nCAUSAL BOUNDARY")


for rule in (
    creative_outcome_link
    .causal_boundary
):

    print(f"- {rule}")

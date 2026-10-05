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

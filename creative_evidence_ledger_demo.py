from models import (
    CampaignMetrics,
    CampaignOutcome,
    CreativeOutcomeLink,
    OutcomeEvidenceSnapshot,
    PerformanceAnalysis,
    PerformanceComparison,
)

from creative_evidence_ledger import (
    build_angle_evidence_ledger,
)


# In-memory fictional test fixtures only.
# Nothing in this demo is saved to SQLite.
def make_test_link(
    campaign_id: int,
    outcome_id: int,
    roas_change: float,
    roas_relative_change: float,
) -> CreativeOutcomeLink:

    raw = CampaignOutcome(
        id=outcome_id,

        campaign_id=campaign_id,

        channel="Meta",

        impressions=10000,
        clicks=300,
        conversions=15,

        spend=5000.0,
        revenue=15000.0,

        measured_from="2026-09-01",
        measured_to="2026-09-07",

        source=(
            "Temporary fictional ledger test"
        ),

        data_quality="manual",

        created_at=None,
    )

    metrics = CampaignMetrics(
        outcome_id=outcome_id,

        campaign_id=campaign_id,

        channel="Meta",

        ctr=0.03,
        cpc=16.67,

        conversion_rate=0.05,
        cpa=333.33,

        roas=3.0,
    )

    snapshot = OutcomeEvidenceSnapshot(
        raw_outcome=raw,

        derived_metrics=metrics,

        conversion_definition=(
            "Waitlist signup"
        ),

        attribution_context=(
            "Fictional Meta attribution "
            "for ledger testing"
        ),

        source_quality="manual",

        known_gaps=[
            "Fictional tutorial fixture.",
        ],

        interpretation_boundary=[
            (
                "Do not use this fixture "
                "as real performance evidence."
            )
        ],
    )

    comparison = PerformanceComparison(
        baseline_available=True,

        ctr_absolute_change=None,
        ctr_relative_change_pct=None,

        cpc_absolute_change=None,
        cpc_relative_change_pct=None,

        conversion_rate_absolute_change=None,
        conversion_rate_relative_change_pct=None,

        cpa_absolute_change=None,
        cpa_relative_change_pct=None,

        roas_absolute_change=(
            roas_change
        ),

        roas_relative_change_pct=(
            roas_relative_change
        ),

        available_comparisons=[
            "roas"
        ],

        comparison_boundary=[
            (
                "Fictional tutorial comparison."
            )
        ],
    )

    analysis = PerformanceAnalysis(
        observed_changes=[],
        supported_interpretations=[],
        unsupported_explanations=[],
        hypotheses=[],
        additional_evidence_needed=[],
        confidence="low",
    )

    return CreativeOutcomeLink(
        campaign_id=campaign_id,

        outcome_id=outcome_id,

        outcome_channel="Meta",

        approved_angle=(
            "What To Try Next"
        ),

        approved_big_idea=(
            "Existing campaign context can "
            "become several candidate directions."
        ),

        approved_visual_asset_ids=[],

        outcome_snapshot=snapshot,

        performance_comparison=(
            comparison
        ),

        performance_analysis=(
            analysis
        ),

        relationship_status=(
            "campaign_strategy_context"
        ),

        causal_boundary=[
            (
                "Temporary fictional fixture. "
                "No causal inference."
            )
        ],
    )


links = [
    make_test_link(
        campaign_id=101,
        outcome_id=1001,
        roas_change=0.50,
        roas_relative_change=20.0,
    ),

    make_test_link(
        campaign_id=102,
        outcome_id=1002,
        roas_change=0.20,
        roas_relative_change=8.0,
    ),

    make_test_link(
        campaign_id=103,
        outcome_id=1003,
        roas_change=-0.30,
        roas_relative_change=-12.0,
    ),

    make_test_link(
        campaign_id=104,
        outcome_id=1004,
        roas_change=0.40,
        roas_relative_change=15.0,
    ),
]


ledger = build_angle_evidence_ledger(
    links=links,

    approved_angle=(
        "What To Try Next"
    ),

    metric_name="roas",

    desired_direction="higher",

    channel="Meta",

    conversion_definition=(
        "Waitlist signup"
    ),

    attribution_context=(
        "Fictional Meta attribution "
        "for ledger testing"
    ),

    source_quality="manual",
)


print("=" * 70)
print("CREATIVE EVIDENCE LEDGER")
print("=" * 70)


print("\nCREATIVE KEY")
print(
    ledger.creative_key
)


print("\nMETRIC")
print(
    ledger.metric_name
)


print("\nDESIRED DIRECTION")
print(
    ledger.desired_direction
)


print("\nCOMPARABLE OBSERVATIONS")


for observation in ledger.observations:

    print("\n" + "-" * 60)

    print(
        f"Campaign {observation.campaign_id}"
    )

    print(
        f"Outcome {observation.outcome_id}"
    )

    print(
        "Absolute change:",
        observation.absolute_change,
    )

    print(
        "Relative change:",
        observation.relative_change_pct,
    )

    print(
        "Direction:",
        observation.direction,
    )


print("\nSUMMARY COUNTS")


print(
    "Supporting:",
    len(
        ledger.supporting_observations
    ),
)


print(
    "Contradicting:",
    len(
        ledger.contradicting_observations
    ),
)


print(
    "Neutral:",
    len(
        ledger.neutral_observations
    ),
)


print(
    "Incomparable:",
    len(
        ledger.incomparable_observations
    ),
)


print("\nREPEATED PATTERN")

print(
    ledger.repeated_pattern
)


print("\nEVIDENCE STRENGTH")

print(
    ledger.evidence_strength
)


print(
    "\nCONTRADICTING OBSERVATIONS"
)


if ledger.contradicting_observations:

    for observation in (
        ledger
        .contradicting_observations
    ):

        print(
            f"- Campaign "
            f"{observation.campaign_id}: "
            f"{observation.relative_change_pct:+.2f}%"
        )

else:

    print("- None")


print(
    "\nINCOMPARABLE OBSERVATIONS"
)


if ledger.incomparable_observations:

    for item in (
        ledger
        .incomparable_observations
    ):

        print(f"- {item}")

else:

    print("- None")


print("\nLEARNING BOUNDARY")


for boundary in (
    ledger.learning_boundary
):

    print(f"- {boundary}")

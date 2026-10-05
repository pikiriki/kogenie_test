from database import (
    get_campaign_outcomes,
    initialize_database,
)

from outcome_evidence import (
    build_outcome_evidence_snapshot,
)


initialize_database()


# Campaign 1 is the campaign used in Lessons 101–102.
campaign_id = 1


outcomes = get_campaign_outcomes(
    campaign_id
)


if not outcomes:

    print(
        "\nNo campaign outcomes exist."
    )

    print(
        "Complete Lesson 101 first."
    )

    raise SystemExit


outcome = outcomes[0]


conversion_definition = (
    "Waitlist signup for this tutorial example."
)


attribution_context = (
    "Fictional Meta Ads Manager attribution "
    "for code testing only. No Shopify or "
    "backend conversion reconciliation was performed."
)


known_gaps = [
    "The dataset is fictional tutorial data.",
    "No control group or holdout exists.",
    "No causal experiment was performed.",
    "No cross-platform attribution reconciliation was performed.",
    "The exact platform attribution window is not documented.",
]


snapshot = (
    build_outcome_evidence_snapshot(
        outcome=outcome,
        conversion_definition=(
            conversion_definition
        ),
        attribution_context=(
            attribution_context
        ),
        known_gaps=known_gaps,
    )
)


print("=" * 70)
print("OUTCOME EVIDENCE SNAPSHOT")
print("=" * 70)


print("\nRAW OUTCOME")

print(
    snapshot.raw_outcome.model_dump_json(
        indent=2
    )
)


print("\nDERIVED METRICS")


metrics = snapshot.derived_metrics


print(
    "CTR:",
    (
        "N/A"
        if metrics.ctr is None
        else f"{metrics.ctr * 100:.2f}%"
    ),
)


print(
    "CPC:",
    (
        "N/A"
        if metrics.cpc is None
        else f"{metrics.cpc:.2f}"
    ),
)


print(
    "Conversion rate:",
    (
        "N/A"
        if metrics.conversion_rate is None
        else (
            f"{metrics.conversion_rate * 100:.2f}%"
        )
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


print("\nCONVERSION DEFINITION")

print(
    snapshot.conversion_definition
)


print("\nATTRIBUTION CONTEXT")

print(
    snapshot.attribution_context
)


print("\nSOURCE QUALITY")

print(
    snapshot.source_quality
)


print("\nKNOWN GAPS")


if snapshot.known_gaps:

    for gap in snapshot.known_gaps:
        print(f"- {gap}")

else:

    print("- None explicitly recorded")


print("\nINTERPRETATION BOUNDARY")


for rule in (
    snapshot.interpretation_boundary
):

    print(f"- {rule}")

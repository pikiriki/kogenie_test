from campaign_metrics import (
    derive_campaign_metrics,
    format_number,
    format_percentage,
)

from database import (
    get_campaign_outcomes,
    initialize_database,
)


initialize_database()


# Campaign 1 is the campaign used in Lesson 101.
campaign_id = 1


outcomes = get_campaign_outcomes(
    campaign_id
)


if not outcomes:

    print(
        "\nNo CampaignOutcome records "
        "exist for this campaign."
    )

    print(
        "Complete Lesson 101 outcome "
        "recording first."
    )

    raise SystemExit


print("\n" + "=" * 70)
print("CAMPAIGN METRICS")
print("=" * 70)


for outcome in outcomes:

    metrics = derive_campaign_metrics(
        outcome
    )

    print("\n" + "-" * 70)

    print(
        f"Outcome ID: {outcome.id}"
    )

    print(
        f"Channel: {outcome.channel}"
    )

    print(
        f"Window: "
        f"{outcome.measured_from} "
        f"→ "
        f"{outcome.measured_to}"
    )

    print("\nRAW")

    print(
        "Impressions:",
        outcome.impressions,
    )

    print(
        "Clicks:",
        outcome.clicks,
    )

    print(
        "Conversions:",
        outcome.conversions,
    )

    print(
        "Spend:",
        outcome.spend,
    )

    print(
        "Revenue:",
        outcome.revenue,
    )

    print("\nDERIVED")

    print(
        "CTR:",
        format_percentage(
            metrics.ctr
        ),
    )

    print(
        "CPC:",
        format_number(
            metrics.cpc
        ),
    )

    print(
        "Conversion rate:",
        format_percentage(
            metrics.conversion_rate
        ),
    )

    print(
        "CPA:",
        format_number(
            metrics.cpa
        ),
    )

    roas_display = (
        "N/A"
        if metrics.roas is None
        else (
            f"{metrics.roas:.2f}x"
        )
    )


    print(
        "ROAS:",
        roas_display,
    )

    print("\nPROVENANCE")

    print(
        "Source:",
        outcome.source,
    )

    print(
        "Data quality:",
        outcome.data_quality,
    )

from database import (
    get_campaign_outcomes,
    initialize_database,
    save_campaign_outcome,
)

from models import (
    CampaignOutcome,
)


initialize_database()


print(
    "\nDEMO ONLY — USING FICTIONAL OUTCOME DATA\n"
)


# Campaign 1 already exists in copy_studio.db.
campaign_id = 1


# In this demo, conversion = waitlist signup.
outcome = CampaignOutcome(
    campaign_id=campaign_id,

    channel="Meta",

    impressions=50000,
    clicks=1200,
    conversions=36,

    spend=18000.0,
    revenue=54000.0,

    measured_from="2026-10-01",
    measured_to="2026-10-07",

    source=(
        "Fictional Meta Ads Manager "
        "export for code testing"
    ),

    data_quality="manual",
)


outcome_id = save_campaign_outcome(
    outcome
)


print(
    f"Saved CampaignOutcome: "
    f"{outcome_id}"
)


outcomes = get_campaign_outcomes(
    campaign_id
)


print("\n" + "=" * 70)
print("CAMPAIGN OUTCOMES")
print("=" * 70)


for item in outcomes:

    print("\n" + "-" * 70)

    print(
        f"Outcome ID: {item.id}"
    )

    print(
        f"Campaign: {item.campaign_id}"
    )

    print(
        f"Channel: {item.channel}"
    )

    print(
        f"Window: "
        f"{item.measured_from} "
        f"→ "
        f"{item.measured_to}"
    )

    print(
        f"Impressions: "
        f"{item.impressions}"
    )

    print(
        f"Clicks: "
        f"{item.clicks}"
    )

    print(
        f"Conversions: "
        f"{item.conversions}"
    )

    print(
        f"Spend: "
        f"{item.spend}"
    )

    print(
        f"Revenue: "
        f"{item.revenue}"
    )

    print(
        f"Source: "
        f"{item.source}"
    )

    print(
        f"Data quality: "
        f"{item.data_quality}"
    )

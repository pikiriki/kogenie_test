from models import (
    CampaignMetrics,
    CampaignOutcome,
)

from outcome_data import (
    validate_campaign_outcome,
)


def safe_divide(
    numerator: float,
    denominator: float,
) -> float | None:

    if denominator == 0:
        return None

    return numerator / denominator


def derive_campaign_metrics(
    outcome: CampaignOutcome,
) -> CampaignMetrics:

    validate_campaign_outcome(
        outcome
    )

    ctr = safe_divide(
        outcome.clicks,
        outcome.impressions,
    )

    cpc = safe_divide(
        outcome.spend,
        outcome.clicks,
    )

    conversion_rate = safe_divide(
        outcome.conversions,
        outcome.clicks,
    )

    cpa = safe_divide(
        outcome.spend,
        outcome.conversions,
    )

    roas = safe_divide(
        outcome.revenue,
        outcome.spend,
    )

    return CampaignMetrics(
        outcome_id=outcome.id,

        campaign_id=outcome.campaign_id,

        channel=outcome.channel,

        ctr=ctr,
        cpc=cpc,

        conversion_rate=(
            conversion_rate
        ),

        cpa=cpa,

        roas=roas,
    )


def format_percentage(
    value: float | None,
) -> str:

    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"


def format_number(
    value: float | None,
    decimals: int = 2,
) -> str:

    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}"

from datetime import date

from models import CampaignOutcome


def validate_campaign_outcome(
    outcome: CampaignOutcome,
) -> None:

    if outcome.impressions < 0:
        raise ValueError(
            "Impressions cannot be negative."
        )


    if outcome.clicks < 0:
        raise ValueError(
            "Clicks cannot be negative."
        )


    if outcome.conversions < 0:
        raise ValueError(
            "Conversions cannot be negative."
        )


    if outcome.spend < 0:
        raise ValueError(
            "Spend cannot be negative."
        )


    if outcome.revenue < 0:
        raise ValueError(
            "Revenue cannot be negative."
        )


    if outcome.clicks > outcome.impressions:

        raise ValueError(
            (
                "Clicks cannot exceed impressions "
                "in this simplified outcome model."
            )
        )


    if outcome.conversions > outcome.clicks:

        raise ValueError(
            (
                "Conversions cannot exceed clicks "
                "in this simplified outcome model."
            )
        )


    measured_from = date.fromisoformat(
        outcome.measured_from
    )


    measured_to = date.fromisoformat(
        outcome.measured_to
    )


    if measured_to < measured_from:

        raise ValueError(
            (
                "measured_to cannot be "
                "before measured_from."
            )
        )


    if not outcome.source.strip():

        raise ValueError(
            "Outcome source cannot be empty."
        )

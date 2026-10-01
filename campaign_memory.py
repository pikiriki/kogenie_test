import json

from models import (
    ApprovalRecord,
    CampaignMemory,
    CopyStrategyCard,
)


def build_campaign_memory(
    strategy_card: CopyStrategyCard,
    approval_record: ApprovalRecord,
    outcome_context: str = "No campaign outcome data recorded.",
) -> CampaignMemory:

    if approval_record.status != "approved":
        raise ValueError(
            "Campaign memory can only be created "
            "from an approved copy snapshot."
        )

    snapshot = json.loads(
        approval_record.approved_message_snapshot
    )

    approved_message = snapshot.get(
        "full_copy"
    )

    if not approved_message:
        raise ValueError(
            "Approved snapshot does not contain full_copy."
        )

    cleaned_outcome_context = (
        outcome_context.strip()
    )

    if not cleaned_outcome_context:

        cleaned_outcome_context = (
            "No campaign outcome data recorded."
        )

    return CampaignMemory(
        campaign_id=approval_record.campaign_id,
        approved_angle=(
            strategy_card.selected_angle
        ),
        approved_big_idea=(
            strategy_card.big_idea
        ),
        approved_message=approved_message,
        evidence_boundaries=(
            strategy_card.proof_boundary
        ),
        outcome_context=(
            cleaned_outcome_context
        ),
    )

from pathlib import Path

from models import (
    CopyStrategyCard,
    GeneratedVisual,
    VisualApprovalRecord,
    VisualAsset,
    VisualCreativeBrief,
)

from visual_approval import (
    sha256_file,
)


def build_visual_asset(
    generated_visual: GeneratedVisual,
    approval_record: VisualApprovalRecord,
    strategy_card: CopyStrategyCard,
    visual_brief: VisualCreativeBrief,
) -> VisualAsset:

    if approval_record.status != "approved":

        raise ValueError(
            (
                "Only a human-approved visual "
                "can enter the visual asset library."
            )
        )

    if approval_record.id is None:

        raise ValueError(
            "Approved visual has no approval record ID."
        )

    if not (
        approval_record
        .approved_visual_snapshot_path
    ):

        raise ValueError(
            (
                "Approved visual has no immutable "
                "snapshot path."
            )
        )

    if not (
        approval_record
        .approved_visual_sha256
    ):

        raise ValueError(
            (
                "Approved visual has no approved "
                "SHA-256 fingerprint."
            )
        )

    if (
        generated_visual.campaign_id
        != approval_record.campaign_id
    ):

        raise ValueError(
            (
                "Generated visual and approval "
                "belong to different campaigns."
            )
        )

    if (
        generated_visual.image_path
        != approval_record.visual_path
    ):

        raise ValueError(
            (
                "Generated visual path does not "
                "match the approved visual."
            )
        )

    snapshot_path = Path(
        approval_record
        .approved_visual_snapshot_path
    )

    if not snapshot_path.exists():

        raise FileNotFoundError(
            (
                "Approved visual snapshot "
                "does not exist."
            )
        )

    actual_sha256 = sha256_file(
        str(snapshot_path)
    )

    if (
        actual_sha256
        != approval_record
        .approved_visual_sha256
    ):

        raise RuntimeError(
            (
                "Approved visual snapshot no "
                "longer matches its recorded hash."
            )
        )

    if not approval_record.decided_at:

        raise ValueError(
            (
                "Approved visual does not have "
                "a decision timestamp."
            )
        )

    return VisualAsset(
        campaign_id=(
            generated_visual.campaign_id
        ),

        visual_path=(
            generated_visual.image_path
        ),

        approved_snapshot_path=(
            approval_record
            .approved_visual_snapshot_path
        ),

        sha256=(
            approval_record
            .approved_visual_sha256
        ),

        channel=(
            generated_visual.channel
        ),

        strategy_angle=(
            strategy_card.selected_angle
        ),

        visual_job=(
            visual_brief.visual_job
        ),

        created_at=(
            approval_record.decided_at
        ),

        approval_record_id=(
            approval_record.id
        ),

        usage_status="available",
    )

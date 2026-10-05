import hashlib
import shutil

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path

from database import (
    create_visual_approval_record,
    finalize_visual_approval_record,
    get_visual_approval_record,
)

from models import (
    GeneratedVisual,
    VisualApprovalRecord,
    VisualReviewReport,
)


from config import (
    get_config,
)


CONFIG = get_config()


def sha256_file(
    file_path: str,
) -> str:

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"Visual does not exist: {file_path}"
        )

    hasher = hashlib.sha256()

    with path.open("rb") as file:

        for chunk in iter(
            lambda: file.read(
                1024 * 1024
            ),
            b"",
        ):

            hasher.update(
                chunk
            )

    return hasher.hexdigest()


def assert_visual_is_approval_eligible(
    visual_review: VisualReviewReport,
) -> None:

    if visual_review.revision_needed:

        raise ValueError(
            (
                "Visual cannot enter human approval "
                "while automated review still "
                "requires revision."
            )
        )

    if visual_review.evidence_violations:

        raise ValueError(
            (
                "Visual cannot enter human approval "
                "with unresolved evidence violations."
            )
        )

    if (
        visual_review
        .negative_constraint_violations
    ):

        raise ValueError(
            (
                "Visual cannot enter human approval "
                "with unresolved negative-constraint "
                "violations."
            )
        )


def create_visual_approval_request(
    generated_visual: GeneratedVisual,
    visual_review: VisualReviewReport,
) -> int:

    assert_visual_is_approval_eligible(
        visual_review
    )

    visual_sha256 = sha256_file(
        generated_visual.image_path
    )

    approval_id = (
        create_visual_approval_record(
            campaign_id=(
                generated_visual.campaign_id
            ),

            visual_path=(
                generated_visual.image_path
            ),

            visual_sha256=visual_sha256,

            generation_spec_snapshot=(
                generated_visual
                .generation_spec_snapshot
            ),

            visual_review_snapshot=(
                visual_review.model_dump_json(
                    indent=2
                )
            ),
        )
    )

    return approval_id


def create_approved_visual_snapshot(
    approval_record: VisualApprovalRecord,
    output_directory: str | None = None,
) -> tuple[str, str]:

    source = Path(
        approval_record.visual_path
    )

    if not source.exists():

        raise FileNotFoundError(
            (
                "Visual awaiting approval "
                "no longer exists."
            )
        )

    current_sha256 = sha256_file(
        str(source)
    )

    if (
        current_sha256
        != approval_record.visual_sha256
    ):

        raise RuntimeError(
            (
                "Visual bytes changed after the "
                "approval request was created. "
                "Create a new approval request."
            )
        )

    if output_directory is None:

        output_dir = (
            CONFIG.approved_visuals_path
        )

    else:

        output_dir = Path(
            output_directory
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix = source.suffix.lower()

    snapshot_path = (
        output_dir
        / (
            f"campaign_{approval_record.campaign_id}_"
            f"visual_approval_{approval_record.id}"
            f"{suffix}"
        )
    )

    if snapshot_path.exists():

        raise RuntimeError(
            (
                "Approved visual snapshot already "
                "exists. Refusing to overwrite it."
            )
        )

    shutil.copy2(
        source,
        snapshot_path,
    )

    snapshot_sha256 = sha256_file(
        str(snapshot_path)
    )

    if (
        snapshot_sha256
        != approval_record.visual_sha256
    ):

        raise RuntimeError(
            (
                "Approved snapshot hash does not "
                "match the reviewed visual."
            )
        )

    return (
        str(snapshot_path),
        snapshot_sha256,
    )


def decide_visual_approval(
    approval_id: int,
    decision: str,
    reviewer: str,
    note: str,
) -> VisualApprovalRecord:

    decision = (
        decision
        .strip()
        .lower()
    )

    if decision not in {
        "approved",
        "rejected",
    }:

        raise ValueError(
            (
                "Decision must be "
                "'approved' or 'rejected'."
            )
        )

    reviewer = reviewer.strip()

    if not reviewer:

        raise ValueError(
            "Reviewer name cannot be empty."
        )

    approval_record = (
        get_visual_approval_record(
            approval_id
        )
    )

    if approval_record is None:

        raise ValueError(
            "Visual approval record does not exist."
        )

    if (
        approval_record.status
        != "awaiting human approval"
    ):

        raise ValueError(
            (
                "Visual approval has already "
                f"been decided: "
                f"{approval_record.status}"
            )
        )

    snapshot_path = None
    snapshot_sha256 = None

    if decision == "approved":

        (
            snapshot_path,
            snapshot_sha256,
        ) = create_approved_visual_snapshot(
            approval_record
        )

    decided_at = datetime.now(
        timezone.utc
    ).isoformat()

    finalize_visual_approval_record(
        approval_id=approval_id,
        decision=decision,
        reviewer=reviewer,
        note=note.strip(),
        decided_at=decided_at,
        approved_visual_snapshot_path=(
            snapshot_path
        ),
        approved_visual_sha256=(
            snapshot_sha256
        ),
    )

    final_record = (
        get_visual_approval_record(
            approval_id
        )
    )

    if final_record is None:

        raise RuntimeError(
            "Could not reload visual approval."
        )

    return final_record


def update_visual_metadata_status(
    generated_visual: GeneratedVisual,
    status: str,
) -> GeneratedVisual:

    updated_visual = (
        generated_visual.model_copy(
            update={
                "approval_status": status,
            }
        )
    )

    Path(
        updated_visual.metadata_path
    ).write_text(
        updated_visual.model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )

    return updated_visual

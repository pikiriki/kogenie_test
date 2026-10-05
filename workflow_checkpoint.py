import hashlib
import json

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path
from typing import Any

from pydantic import BaseModel

from config import (
    get_config,
)

from database import (
    get_workflow_checkpoints,
    get_workflow_run,
    invalidate_workflow_checkpoint,
    save_workflow_checkpoint_record,
)

from models import (
    WorkflowCheckpoint,
    WorkflowRun,
)

from workflow_run import (
    start_workflow_run,
)


CONFIG = get_config()


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def safe_name(
    value: str,
) -> str:

    cleaned = []

    for character in (
        value.strip().lower()
    ):

        if (
            character.isalnum()
            or character in {
                "-",
                "_",
            }
        ):

            cleaned.append(
                character
            )

        else:

            cleaned.append(
                "_"
            )

    return "".join(
        cleaned
    )


def sha256_file(
    path: Path,
) -> str:

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


def serialize_checkpoint_payload(
    payload: Any,
) -> str:

    if isinstance(
        payload,
        BaseModel,
    ):

        serializable = (
            payload.model_dump(
                mode="json"
            )
        )

    else:

        serializable = payload

    return json.dumps(
        serializable,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        default=str,
    )


def create_workflow_checkpoint(
    run_id: str,
    stage: str,
    artifact_type: str,
    payload: Any,
) -> WorkflowCheckpoint:

    stage = stage.strip()
    artifact_type = (
        artifact_type.strip()
    )

    if not stage:

        raise ValueError(
            "Checkpoint stage cannot be empty."
        )


    if not artifact_type:

        raise ValueError(
            "Checkpoint artifact type "
            "cannot be empty."
        )

    run = get_workflow_run(
        run_id
    )


    if run is None:

        raise ValueError(
            "Workflow run does not exist."
        )


    if run.status != "running":

        raise ValueError(
            (
                "New checkpoints can only be "
                "created for a running workflow."
            )
        )

    envelope = {
        "run_id": run_id,
        "stage": stage,
        "artifact_type": (
            artifact_type
        ),
        "payload": payload,
    }

    serialized = (
        serialize_checkpoint_payload(
            envelope
        )
    )

    checkpoint_dir = (
        CONFIG.workflow_checkpoints_path
    )


    checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_name = (
        f"{safe_name(run_id)}__"
        f"{safe_name(stage)}__"
        f"{safe_name(artifact_type)}"
        ".json"
    )

    artifact_path = (
        checkpoint_dir
        / file_name
    )

    expected_bytes = (
        serialized.encode(
            "utf-8"
        )
    )

    expected_hash = (
        hashlib.sha256(
            expected_bytes
        ).hexdigest()
    )

    if artifact_path.exists():

        existing_hash = (
            sha256_file(
                artifact_path
            )
        )

        if (
            existing_hash
            != expected_hash
        ):

            raise RuntimeError(
                (
                    "Checkpoint artifact already "
                    "exists with different content. "
                    "Refusing to overwrite it."
                )
            )

    else:

        artifact_path.write_text(
            serialized,
            encoding="utf-8",
        )

    checkpoint = WorkflowCheckpoint(
        run_id=run_id,

        stage=stage,

        artifact_type=(
            artifact_type
        ),

        artifact_reference=str(
            artifact_path
        ),

        artifact_hash=(
            expected_hash
        ),

        created_at=utc_now(),

        valid=True,
    )

    checkpoint_id = (
        save_workflow_checkpoint_record(
            checkpoint
        )
    )

    return checkpoint.model_copy(
        update={
            "id": checkpoint_id,
        }
    )


def validate_workflow_checkpoint(
    checkpoint: WorkflowCheckpoint,
) -> bool:

    if not checkpoint.valid:

        return False

    if checkpoint.id is None:

        return False

    path = Path(
        checkpoint.artifact_reference
    )

    if not path.exists():

        invalidate_workflow_checkpoint(
            checkpoint.id
        )

        return False

    actual_hash = (
        sha256_file(
            path
        )
    )

    if (
        actual_hash
        != checkpoint.artifact_hash
    ):

        invalidate_workflow_checkpoint(
            checkpoint.id
        )

        return False

    return True


def load_checkpoint_payload(
    checkpoint: WorkflowCheckpoint,
) -> Any:

    if not validate_workflow_checkpoint(
        checkpoint
    ):

        raise RuntimeError(
            "Workflow checkpoint is not valid."
        )

    path = Path(
        checkpoint.artifact_reference
    )


    envelope = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if (
        envelope.get("run_id")
        != checkpoint.run_id
        or envelope.get("stage")
        != checkpoint.stage
        or envelope.get("artifact_type")
        != checkpoint.artifact_type
    ):

        invalidate_workflow_checkpoint(
            checkpoint.id
        )

        raise RuntimeError(
            (
                "Checkpoint artifact metadata "
                "does not match its database record."
            )
        )

    return envelope[
        "payload"
    ]


def find_last_safe_checkpoint(
    run_id: str,
    ordered_stages: list[str],
    artifact_type: str = "stage_output",
) -> WorkflowCheckpoint | None:

    checkpoints = (
        get_workflow_checkpoints(
            run_id
        )
    )

    by_stage = {
        checkpoint.stage: checkpoint

        for checkpoint in checkpoints

        if (
            checkpoint.artifact_type
            == artifact_type
        )
    }

    last_safe = None

    for stage in ordered_stages:

        checkpoint = (
            by_stage.get(
                stage
            )
        )

        if checkpoint is None:

            break

        if not (
            validate_workflow_checkpoint(
                checkpoint
            )
        ):

            break

        last_safe = checkpoint

    return last_safe


def determine_resume_stage(
    run_id: str,
    ordered_stages: list[str],
) -> tuple[
    WorkflowCheckpoint | None,
    str | None,
]:

    if not ordered_stages:

        raise ValueError(
            "Workflow stage order cannot be empty."
        )

    checkpoint = (
        find_last_safe_checkpoint(
            run_id,
            ordered_stages,
        )
    )

    if checkpoint is None:

        return (
            None,
            ordered_stages[0],
        )

    index = ordered_stages.index(
        checkpoint.stage
    )

    if (
        index
        == len(ordered_stages) - 1
    ):

        return (
            checkpoint,
            None,
        )

    return (
        checkpoint,
        ordered_stages[
            index + 1
        ],
    )


def start_recovery_run(
    source_run_id: str,
    ordered_stages: list[str],
) -> tuple[
    WorkflowRun,
    WorkflowCheckpoint | None,
    str | None,
]:

    source_run = get_workflow_run(
        source_run_id
    )


    if source_run is None:

        raise ValueError(
            "Recovery source run does not exist."
        )

    if source_run.status != "failed":

        raise ValueError(
            (
                "Recovery may only start from "
                "a failed workflow run."
            )
        )

    (
        last_checkpoint,
        resume_stage,
    ) = determine_resume_stage(
        source_run_id,
        ordered_stages,
    )

    if resume_stage is None:

        raise ValueError(
            (
                "All defined workflow stages "
                "already have valid checkpoints."
            )
        )

    recovery_run = (
        start_workflow_run(
            workflow_name=(
                source_run.workflow_name
            ),

            initial_stage=(
                resume_stage
            ),
        )
    )

    recovery_context = {
        "source_run_id": (
            source_run_id
        ),

        "resume_stage": (
            resume_stage
        ),

        "last_safe_stage": (
            last_checkpoint.stage
            if last_checkpoint
            is not None
            else None
        ),

        "reused_checkpoint_reference": (
            last_checkpoint
            .artifact_reference

            if last_checkpoint
            is not None

            else None
        ),

        "reused_checkpoint_hash": (
            last_checkpoint
            .artifact_hash

            if last_checkpoint
            is not None

            else None
        ),
    }

    create_workflow_checkpoint(
        run_id=(
            recovery_run.run_id
        ),

        stage="recovery_start",

        artifact_type=(
            "recovery_context"
        ),

        payload=(
            recovery_context
        ),
    )

    return (
        recovery_run,
        last_checkpoint,
        resume_stage,
    )

import hashlib
import json

from typing import Any
from uuid import uuid4

from pydantic import BaseModel

from config import (
    get_config,
)

from database import (
    claim_idempotent_workflow_record,
)

from models import (
    IdempotencyRecord,
    WorkflowRun,
)

from workflow_run import (
    create_run_id,
    utc_now,
)

from workflow_event import (
    record_workflow_event,
)


CONFIG = get_config()


def create_idempotency_key() -> str:

    return (
        "idem_"
        + uuid4().hex
    )


def normalize_payload(
    payload: Any,
) -> Any:

    if isinstance(
        payload,
        BaseModel,
    ):

        return payload.model_dump(
            mode="json"
        )

    if isinstance(
        payload,
        dict,
    ):

        return {
            str(key): normalize_payload(
                value
            )

            for key, value
            in payload.items()
        }

    if isinstance(
        payload,
        (
            list,
            tuple,
        ),
    ):

        return [
            normalize_payload(
                item
            )

            for item in payload
        ]

    return payload


def fingerprint_request(
    operation: str,
    request_payload: Any,
) -> str:

    operation = operation.strip()


    if not operation:

        raise ValueError(
            "Operation cannot be empty."
        )

    fingerprint_payload = {
        "operation": operation,

        "request": normalize_payload(
            request_payload
        ),
    }

    serialized = json.dumps(
        fingerprint_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        default=str,
    )

    return hashlib.sha256(
        serialized.encode(
            "utf-8"
        )
    ).hexdigest()


def start_idempotent_workflow(
    idempotency_key: str,
    operation: str,
    request_payload: Any,
    workflow_name: str,
    initial_stage: str = "starting",
) -> tuple[
    IdempotencyRecord,
    WorkflowRun,
    bool,
]:

    idempotency_key = (
        idempotency_key.strip()
    )


    if not idempotency_key:

        raise ValueError(
            "Idempotency key cannot be empty."
        )

    fingerprint = (
        fingerprint_request(
            operation=operation,
            request_payload=(
                request_payload
            ),
        )
    )

    started_at = utc_now()

    run_id = create_run_id()

    run = WorkflowRun(
        run_id=run_id,

        workflow_name=(
            workflow_name.strip()
        ),

        started_at=(
            started_at
        ),

        completed_at=None,

        status="running",

        config_snapshot=(
            CONFIG.model_dump_json(
                indent=2
            )
        ),

        current_stage=(
            initial_stage.strip()
        ),

        failure=None,
    )

    if not run.workflow_name:

        raise ValueError(
            "Workflow name cannot be empty."
        )


    if not run.current_stage:

        raise ValueError(
            "Initial stage cannot be empty."
        )

    record = IdempotencyRecord(
        idempotency_key=(
            idempotency_key
        ),

        operation=(
            operation.strip()
        ),

        request_fingerprint=(
            fingerprint
        ),

        run_id=run_id,

        status="in_progress",

        created_at=(
            started_at
        ),

        completed_at=None,
    )

    (
        claimed_record,
        claimed_run,
        created_new,
    ) = (
        claim_idempotent_workflow_record(
            record=record,
            run=run,
        )
    )

    if created_new:

        record_workflow_event(
            run_id=(
                claimed_run.run_id
            ),

            event_type="run_started",

            stage=(
                claimed_run.current_stage
            ),

            message=(
                f"Workflow "
                f"'{claimed_run.workflow_name}' "
                "started through an "
                "idempotent request."
            ),

            metadata={
                "operation": (
                    claimed_record.operation
                ),

                "request_fingerprint": (
                    claimed_record
                    .request_fingerprint
                ),
            },
        )

    else:

        record_workflow_event(
            run_id=(
                claimed_run.run_id
            ),

            event_type=(
                "idempotency_reused"
            ),

            stage=(
                claimed_run.current_stage
            ),

            message=(
                "Existing workflow run reused "
                "for repeated idempotent request."
            ),

            metadata={
                "operation": (
                    claimed_record.operation
                ),

                "idempotency_status": (
                    claimed_record.status
                ),
            },
        )

    return (
        claimed_record,
        claimed_run,
        created_new,
    )

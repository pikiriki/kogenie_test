from datetime import (
    datetime,
    timezone,
)

import json

from uuid import uuid4

from database import (
    append_workflow_event_record,
)

from models import (
    WorkflowEvent,
)


MAX_METADATA_CHARACTERS = 10000


SENSITIVE_KEY_FRAGMENTS = {
    "api_key",
    "password",
    "authorization",
    "secret",
}


def create_event_id() -> str:

    return (
        "evt_"
        + uuid4().hex
    )


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def validate_event_metadata(
    metadata: dict,
) -> None:

    for key in metadata:

        normalized_key = (
            str(key)
            .strip()
            .lower()
        )

        for fragment in (
            SENSITIVE_KEY_FRAGMENTS
        ):

            if fragment in normalized_key:

                raise ValueError(
                    (
                        "Sensitive-looking metadata "
                        f"key is not allowed in "
                        f"workflow events: {key}"
                    )
                )

    serialized = json.dumps(
        metadata,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )

    if (
        len(serialized)
        > MAX_METADATA_CHARACTERS
    ):

        raise ValueError(
            (
                "Workflow event metadata is "
                "too large. Store artifact "
                "content elsewhere and log "
                "only identifiers/provenance."
            )
        )


def record_workflow_event(
    run_id: str,
    event_type: str,
    message: str,
    stage: str | None = None,
    metadata: dict | None = None,
) -> WorkflowEvent:

    if metadata is None:

        metadata = {}

    run_id = run_id.strip()

    message = message.strip()

    if not run_id:

        raise ValueError(
            "Workflow event run_id "
            "cannot be empty."
        )


    if not message:

        raise ValueError(
            "Workflow event message "
            "cannot be empty."
        )

    validate_event_metadata(
        metadata
    )

    event = WorkflowEvent(
        event_id=create_event_id(),

        run_id=run_id,

        event_type=event_type,

        stage=stage,

        occurred_at=utc_now(),

        message=message,

        metadata=metadata,
    )

    append_workflow_event_record(
        event
    )

    return event

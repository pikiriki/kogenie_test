from datetime import (
    datetime,
    timezone,
)

from uuid import uuid4

from config import (
    get_config,
)

from database import (
    complete_workflow_run_record,
    create_workflow_run_record,
    fail_workflow_run_record,
    get_workflow_run,
    update_workflow_run_stage,
)

from models import (
    WorkflowRun,
)

from workflow_event import (
    record_workflow_event,
)


CONFIG = get_config()


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def create_run_id() -> str:

    return (
        "run_"
        + uuid4().hex
    )


def start_workflow_run(
    workflow_name: str,
    initial_stage: str = "starting",
) -> WorkflowRun:

    workflow_name = (
        workflow_name.strip()
    )

    initial_stage = (
        initial_stage.strip()
    )

    if not workflow_name:

        raise ValueError(
            "Workflow name cannot be empty."
        )


    if not initial_stage:

        raise ValueError(
            "Initial stage cannot be empty."
        )

    config_snapshot = (
        CONFIG.model_dump_json(
            indent=2
        )
    )

    run = WorkflowRun(
        run_id=create_run_id(),

        workflow_name=(
            workflow_name
        ),

        started_at=utc_now(),

        completed_at=None,

        status="running",

        config_snapshot=(
            config_snapshot
        ),

        current_stage=(
            initial_stage
        ),

        failure=None,
    )

    create_workflow_run_record(
        run
    )

    record_workflow_event(
        run_id=run.run_id,

        event_type="run_started",

        stage=run.current_stage,

        message=(
            f"Workflow "
            f"'{run.workflow_name}' "
            "started."
        ),

        metadata={
            "workflow_name": (
                run.workflow_name
            ),
        },
    )

    return run


def set_workflow_stage(
    run_id: str,
    stage: str,
) -> WorkflowRun:

    previous = get_workflow_run(
        run_id
    )


    if previous is None:

        raise ValueError(
            "Workflow run does not exist."
        )

    update_workflow_run_stage(
        run_id,
        stage,
    )

    run = get_workflow_run(
        run_id
    )

    if run is None:

        raise RuntimeError(
            "Could not reload workflow run."
        )

    record_workflow_event(
        run_id=run_id,

        event_type="stage_changed",

        stage=stage,

        message=(
            "Workflow stage changed "
            f"from '{previous.current_stage}' "
            f"to '{stage}'."
        ),

        metadata={
            "from_stage": (
                previous.current_stage
            ),

            "to_stage": stage,
        },
    )

    return run


def complete_workflow_run(
    run_id: str,
) -> WorkflowRun:

    complete_workflow_run_record(
        run_id=run_id,
        completed_at=utc_now(),
    )

    run = get_workflow_run(
        run_id
    )


    if run is None:

        raise RuntimeError(
            "Could not reload completed run."
        )

    record_workflow_event(
        run_id=run_id,

        event_type="run_completed",

        stage="completed",

        message=(
            "Workflow completed successfully."
        ),

        metadata={},
    )

    return run


def fail_workflow_run(
    run_id: str,
    failure_summary: str,
) -> WorkflowRun:

    fail_workflow_run_record(
        run_id=run_id,
        completed_at=utc_now(),
        failure=failure_summary,
    )

    run = get_workflow_run(
        run_id
    )


    if run is None:

        raise RuntimeError(
            "Could not reload failed run."
        )

    record_workflow_event(
        run_id=run_id,

        event_type="run_failed",

        stage=run.current_stage,

        message=(
            "Workflow entered failed state."
        ),

        metadata={
            "failure_summary": (
                run.failure
            ),
        },
    )

    return run

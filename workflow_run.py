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

    return run


def set_workflow_stage(
    run_id: str,
    stage: str,
) -> WorkflowRun:

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


    return run

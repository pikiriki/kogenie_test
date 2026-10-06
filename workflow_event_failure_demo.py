from database import (
    get_workflow_events,
    initialize_database,
)

from workflow_lease import (
    acquire_workflow_lease,
)

from workflow_run import (
    fail_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


run = start_workflow_run(
    workflow_name=(
        "event_failure_demo"
    ),

    initial_stage="research",
)

acquire_workflow_lease(
    run.run_id
)


set_workflow_stage(
    run.run_id,
    "strategy",
)


run = fail_workflow_run(
    run_id=run.run_id,

    failure_summary=(
        "Strategy stage failed. "
        "Exception type: RuntimeError."
    ),
)


events = get_workflow_events(
    run.run_id
)


for event in events:

    print(
        event.occurred_at,
        event.event_type,
        event.stage,
        event.message,
    )

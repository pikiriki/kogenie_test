from database import (
    get_workflow_events,
    initialize_database,
)

from workflow_checkpoint import (
    create_workflow_checkpoint,
)

from workflow_lease import (
    acquire_workflow_lease,
    heartbeat_workflow_lease,
)

from workflow_run import (
    complete_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


run = start_workflow_run(
    workflow_name=(
        "event_timeline_demo"
    ),

    initial_stage="research",
)


acquire_workflow_lease(
    run.run_id
)


heartbeat_workflow_lease(
    run.run_id
)


create_workflow_checkpoint(
    run_id=run.run_id,

    stage="research",

    artifact_type="stage_output",

    payload={
        "status": (
            "research completed"
        ),
    },
)


set_workflow_stage(
    run.run_id,
    "strategy",
)


heartbeat_workflow_lease(
    run.run_id
)


create_workflow_checkpoint(
    run_id=run.run_id,

    stage="strategy",

    artifact_type="stage_output",

    payload={
        "angle": (
            "What To Try Next"
        ),
    },
)


run = complete_workflow_run(
    run.run_id
)


events = get_workflow_events(
    run.run_id
)


print("=" * 70)
print("WORKFLOW EVENT TIMELINE")
print("=" * 70)


print(
    "\nRUN:",
    run.run_id,
)


for event in events:

    print("\n" + "-" * 70)

    print(
        event.occurred_at
    )

    print(
        event.event_type
    )

    print(
        "Stage:",
        event.stage,
    )

    print(
        event.message
    )

    if event.metadata:

        print(
            "Metadata:",
            event.metadata,
        )

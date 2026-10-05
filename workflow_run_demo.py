from database import (
    get_workflow_run,
    initialize_database,
)

from workflow_run import (
    complete_workflow_run,
    fail_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


run = start_workflow_run(
    workflow_name=(
        "campaign_generation_demo"
    ),
    initial_stage="runtime_check",
)


print("=" * 70)
print("WORKFLOW RUN")
print("=" * 70)


print("\nRUN ID")
print(
    run.run_id
)


print("\nSTATUS")
print(
    run.status
)


print("\nCURRENT STAGE")
print(
    run.current_stage
)


run = set_workflow_stage(
    run.run_id,
    "research",
)


print(
    "\nStage:",
    run.current_stage,
)


run = set_workflow_stage(
    run.run_id,
    "strategy",
)


print(
    "Stage:",
    run.current_stage,
)


run = set_workflow_stage(
    run.run_id,
    "copy_generation",
)


print(
    "Stage:",
    run.current_stage,
)


run = complete_workflow_run(
    run.run_id
)


print("\nFINAL STATUS")
print(
    run.status
)


print("\nFINAL STAGE")
print(
    run.current_stage
)


print("\nSTARTED")
print(
    run.started_at
)


print("\nCOMPLETED")
print(
    run.completed_at
)


print("\nCONFIG SNAPSHOT")

print(
    run.config_snapshot
)

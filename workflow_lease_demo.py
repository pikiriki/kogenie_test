from time import sleep

from database import (
    get_workflow_run,
    initialize_database,
)

from workflow_checkpoint import (
    create_workflow_checkpoint,
    start_recovery_run,
)

from workflow_lease import (
    acquire_workflow_lease,
    current_worker_id,
    fail_stale_workflow_run,
    find_stale_workflow_runs,
    heartbeat_workflow_lease,
)

from workflow_run import (
    complete_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


STAGES = [
    "research",
    "strategy",
]


run_a = start_workflow_run(
    workflow_name=(
        "lease_recovery_demo"
    ),

    initial_stage="research",
)


print(
    "\nRUN A:",
    run_a.run_id,
)

print(
    "WORKER:",
    current_worker_id(),
)


# One-second lease for the demo only. The configured
# application default stays KOGENIE_WORKFLOW_LEASE_SECONDS.
lease_a = acquire_workflow_lease(
    run_id=run_a.run_id,
    lease_seconds=1,
)


print(
    "\nLEASE EXPIRES:",
    lease_a.lease_expires_at,
)


research_payload = {
    "status": "research completed",
}


create_workflow_checkpoint(
    run_id=run_a.run_id,

    stage="research",

    artifact_type="stage_output",

    payload=research_payload,
)


set_workflow_stage(
    run_a.run_id,
    "strategy",
)


print(
    "\nSimulating worker disappearance..."
)


sleep(2)


stale_runs = (
    find_stale_workflow_runs()
)


print("\nSTALE RUNS")


for run, lease in stale_runs:

    print(
        f"- {run.run_id} "
        f"stage={run.current_stage}"
    )

    if lease is None:

        print(
            "  lease: missing"
        )

    else:

        print(
            "  expired:",
            lease.lease_expires_at,
        )


run_a = fail_stale_workflow_run(
    run_a.run_id
)


print("\nRUN A STATUS")

print(
    run_a.status
)


print("\nRUN A FAILED AT")

print(
    run_a.current_stage
)


print("\nRUN A FAILURE")

print(
    run_a.failure
)


(
    run_b,
    last_safe_checkpoint,
    resume_stage,
) = start_recovery_run(
    source_run_id=(
        run_a.run_id
    ),

    ordered_stages=STAGES,
)


print("\nRECOVERY RUN")

print(
    run_b.run_id
)


print("\nLAST SAFE STAGE")

print(
    (
        last_safe_checkpoint.stage
        if last_safe_checkpoint
        else "None"
    )
)


print("\nRESUME STAGE")

print(
    resume_stage
)


lease_b = acquire_workflow_lease(
    run_b.run_id
)


heartbeat_workflow_lease(
    run_b.run_id
)


strategy_payload = {
    "status": "strategy completed",
}


create_workflow_checkpoint(
    run_id=run_b.run_id,

    stage="strategy",

    artifact_type="stage_output",

    payload=strategy_payload,
)


run_b = complete_workflow_run(
    run_b.run_id
)


print("\nRUN B FINAL STATUS")

print(
    run_b.status
)


healthy_run = start_workflow_run(
    workflow_name=(
        "healthy_heartbeat_demo"
    ),

    initial_stage="work",
)


acquire_workflow_lease(
    healthy_run.run_id,
    lease_seconds=2,
)


sleep(1)


heartbeat_workflow_lease(
    healthy_run.run_id,
    lease_seconds=2,
)


sleep(1)


stale_ids = [
    run.run_id

    for run, lease
    in find_stale_workflow_runs()
]


print(
    "\nHEALTHY RUN MARKED STALE"
)

print(
    healthy_run.run_id
    in stale_ids
)


complete_workflow_run(
    healthy_run.run_id
)

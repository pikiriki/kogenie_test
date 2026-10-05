from database import (
    initialize_database,
)

from workflow_checkpoint import (
    create_workflow_checkpoint,
    load_checkpoint_payload,
    start_recovery_run,
)

from workflow_run import (
    complete_workflow_run,
    fail_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


STAGES = [
    "research",
    "strategy",
    "copy_generation",
    "channel_generation",
]


run_a = start_workflow_run(
    workflow_name=(
        "campaign_generation_demo"
    ),
    initial_stage="research",
)


print(
    "\nRUN A:",
    run_a.run_id,
)


research_payload = {
    "research_document_id": (
        "demo-research-1"
    ),

    "status": "completed",
}


research_checkpoint = (
    create_workflow_checkpoint(
        run_id=run_a.run_id,
        stage="research",
        artifact_type="stage_output",
        payload=research_payload,
    )
)


set_workflow_stage(
    run_a.run_id,
    "strategy",
)


strategy_payload = {
    "selected_angle": (
        "What To Try Next"
    ),

    "big_idea": (
        "Existing campaign context "
        "can become several candidate "
        "creative directions."
    ),
}


strategy_checkpoint = (
    create_workflow_checkpoint(
        run_id=run_a.run_id,
        stage="strategy",
        artifact_type="stage_output",
        payload=strategy_payload,
    )
)


strategy_checkpoint_again = (
    create_workflow_checkpoint(
        run_id=run_a.run_id,
        stage="strategy",
        artifact_type="stage_output",
        payload=strategy_payload,
    )
)


print(
    "\nSTRATEGY CHECKPOINT ID"
)

print(
    strategy_checkpoint.id
)


print(
    "\nSECOND IDENTICAL CALL ID"
)

print(
    strategy_checkpoint_again.id
)


set_workflow_stage(
    run_a.run_id,
    "copy_generation",
)


try:

    raise RuntimeError(
        "Simulated copy-generation failure."
    )

except Exception as error:

    run_a = fail_workflow_run(
        run_id=run_a.run_id,

        failure_summary=(
            "Copy generation failed. "
            f"Exception type: "
            f"{type(error).__name__}."
        ),
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


print("\n" + "=" * 70)
print("RECOVERY")
print("=" * 70)


print("\nSOURCE RUN")
print(
    run_a.run_id
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


reused_strategy = (
    load_checkpoint_payload(
        last_safe_checkpoint
    )
)


print(
    "\nREUSED STRATEGY PAYLOAD"
)

print(
    reused_strategy
)


copy_payload = {
    "headline": (
        "What should you try next?"
    ),

    "status": "completed",
}


copy_checkpoint = (
    create_workflow_checkpoint(
        run_id=run_b.run_id,
        stage="copy_generation",
        artifact_type="stage_output",
        payload=copy_payload,
    )
)


set_workflow_stage(
    run_b.run_id,
    "channel_generation",
)


channel_payload = {
    "channels": [
        "Meta",
        "Search",
        "Email",
        "Landing Page",
        "X",
    ],

    "status": "completed",
}


create_workflow_checkpoint(
    run_id=run_b.run_id,
    stage="channel_generation",
    artifact_type="stage_output",
    payload=channel_payload,
)


run_b = complete_workflow_run(
    run_b.run_id
)


print("\nRECOVERY FINAL STATUS")

print(
    run_b.status
)

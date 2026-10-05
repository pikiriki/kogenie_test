from database import (
    initialize_database,
)

from workflow_run import (
    fail_workflow_run,
    set_workflow_stage,
    start_workflow_run,
)


initialize_database()


run = start_workflow_run(
    workflow_name=(
        "visual_generation_demo"
    ),
    initial_stage="preparation",
)


try:

    run = set_workflow_stage(
        run.run_id,
        "visual_generation",
    )

    raise RuntimeError(
        "Simulated image-generation failure."
    )

except Exception as error:

    failed_run = fail_workflow_run(
        run_id=run.run_id,

        failure_summary=(
            "Visual generation stage failed. "
            f"Exception type: "
            f"{type(error).__name__}."
        ),
    )

    print("=" * 70)
    print("FAILED WORKFLOW RUN")
    print("=" * 70)


    print("\nRUN ID")
    print(
        failed_run.run_id
    )


    print("\nSTATUS")
    print(
        failed_run.status
    )


    print("\nFAILED AT STAGE")
    print(
        failed_run.current_stage
    )


    print("\nFAILURE")
    print(
        failed_run.failure
    )


    print("\nCOMPLETED AT")
    print(
        failed_run.completed_at
    )

    raise

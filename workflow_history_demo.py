from database import (
    get_recent_workflow_runs,
    get_workflow_checkpoints,
    initialize_database,
)


initialize_database()


runs = get_recent_workflow_runs(
    limit=10
)


print("=" * 70)
print("RECENT WORKFLOW RUNS")
print("=" * 70)


if not runs:

    print(
        "\nNo workflow runs recorded."
    )

    raise SystemExit


for run in runs:

    print("\n" + "-" * 70)

    print(
        "Run:",
        run.run_id,
    )

    print(
        "Workflow:",
        run.workflow_name,
    )

    print(
        "Status:",
        run.status,
    )

    print(
        "Stage:",
        run.current_stage,
    )

    print(
        "Started:",
        run.started_at,
    )

    print(
        "Ended:",
        (
            run.completed_at
            or "-"
        ),
    )

    if run.failure:

        print(
            "Failure:",
            run.failure,
        )

    checkpoints = (
        get_workflow_checkpoints(
            run.run_id
        )
    )

    print(
        "Checkpoints:",
        len(checkpoints),
    )

    for checkpoint in checkpoints:

        print(
            "  -",
            checkpoint.stage,
            checkpoint.artifact_type,
            (
                "valid"
                if checkpoint.valid
                else "invalid"
            ),
        )

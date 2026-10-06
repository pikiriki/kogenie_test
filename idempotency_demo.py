from database import (
    get_idempotency_record,
    initialize_database,
)

from idempotency import (
    create_idempotency_key,
    start_idempotent_workflow,
)

from workflow_run import (
    complete_workflow_run,
)


initialize_database()


idempotency_key = (
    create_idempotency_key()
)


# Campaign 999 is only a value inside the tutorial request
# fingerprint. No Campaign 999 row is created.
request_payload = {
    "campaign_id": 999,

    "campaign_objective": (
        "Tutorial duplicate-run test"
    ),

    "brief_version": 1,
}


(
    record_1,
    run_1,
    created_1,
) = start_idempotent_workflow(
    idempotency_key=(
        idempotency_key
    ),

    operation=(
        "tutorial_campaign_generation"
    ),

    request_payload=(
        request_payload
    ),

    workflow_name=(
        "idempotency_demo"
    ),

    initial_stage="starting",
)


print("=" * 70)
print("FIRST REQUEST")
print("=" * 70)


print(
    "Created new:",
    created_1,
)


print(
    "Run:",
    run_1.run_id,
)


(
    record_2,
    run_2,
    created_2,
) = start_idempotent_workflow(
    idempotency_key=(
        idempotency_key
    ),

    operation=(
        "tutorial_campaign_generation"
    ),

    request_payload=(
        request_payload
    ),

    workflow_name=(
        "idempotency_demo"
    ),

    initial_stage="starting",
)


print("\n" + "=" * 70)
print("RETRY")
print("=" * 70)


print(
    "Created new:",
    created_2,
)


print(
    "Run:",
    run_2.run_id,
)


print(
    "Same run:",
    (
        run_1.run_id
        == run_2.run_id
    ),
)


completed_run = (
    complete_workflow_run(
        run_1.run_id
    )
)


completed_record = (
    get_idempotency_record(
        idempotency_key
    )
)


print("\nRUN STATUS")
print(
    completed_run.status
)


print("\nIDEMPOTENCY STATUS")
print(
    completed_record.status
)


(
    record_3,
    run_3,
    created_3,
) = start_idempotent_workflow(
    idempotency_key=(
        idempotency_key
    ),

    operation=(
        "tutorial_campaign_generation"
    ),

    request_payload=(
        request_payload
    ),

    workflow_name=(
        "idempotency_demo"
    ),

    initial_stage="starting",
)


print("\n" + "=" * 70)
print("RETRY AFTER COMPLETION")
print("=" * 70)


print(
    "Created new:",
    created_3,
)


print(
    "Same run:",
    (
        run_3.run_id
        == run_1.run_id
    ),
)


print(
    "Run status:",
    run_3.status,
)


changed_request = {
    "campaign_id": 999,

    "campaign_objective": (
        "DIFFERENT REQUEST"
    ),

    "brief_version": 1,
}


try:

    start_idempotent_workflow(
        idempotency_key=(
            idempotency_key
        ),

        operation=(
            "tutorial_campaign_generation"
        ),

        request_payload=(
            changed_request
        ),

        workflow_name=(
            "idempotency_demo"
        ),

        initial_stage="starting",
    )

except ValueError as error:

    print(
        "\nEXPECTED CONFLICT"
    )

    print(error)

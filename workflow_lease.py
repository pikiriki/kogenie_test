from datetime import (
    datetime,
    timedelta,
    timezone,
)

from uuid import uuid4

from config import (
    get_config,
)

from database import (
    claim_workflow_lease_record,
    fail_workflow_if_stale,
    get_running_workflow_runs,
    get_workflow_lease,
    get_workflow_run,
    update_workflow_lease_record,
)

from models import (
    WorkflowLease,
    WorkflowRun,
)

from workflow_event import (
    record_workflow_event,
)


CONFIG = get_config()


PROCESS_WORKER_ID = (
    "worker_"
    + uuid4().hex
)


def current_worker_id() -> str:

    return PROCESS_WORKER_ID


def build_lease_times(
    lease_seconds: int,
) -> tuple[
    str,
    str,
]:

    if lease_seconds <= 0:

        raise ValueError(
            "Lease seconds must be positive."
        )

    now = datetime.now(
        timezone.utc
    )

    expires = (
        now
        + timedelta(
            seconds=lease_seconds
        )
    )

    return (
        now.isoformat(),
        expires.isoformat(),
    )


def acquire_workflow_lease(
    run_id: str,
    worker_id: str | None = None,
    lease_seconds: int | None = None,
) -> WorkflowLease:

    if worker_id is None:

        worker_id = (
            PROCESS_WORKER_ID
        )


    if lease_seconds is None:

        lease_seconds = (
            CONFIG.workflow_lease_seconds
        )

    (
        heartbeat_at,
        lease_expires_at,
    ) = build_lease_times(
        lease_seconds
    )

    lease = WorkflowLease(
        run_id=run_id,

        worker_id=worker_id,

        heartbeat_at=(
            heartbeat_at
        ),

        lease_expires_at=(
            lease_expires_at
        ),
    )

    claimed_lease = (
        claim_workflow_lease_record(
            lease
        )
    )

    record_workflow_event(
        run_id=run_id,

        event_type="lease_acquired",

        stage=None,

        message=(
            "Workflow lease acquired "
            "or confirmed."
        ),

        metadata={
            "worker_id": (
                worker_id
            ),

            "lease_expires_at": (
                claimed_lease
                .lease_expires_at
            ),
        },
    )

    return claimed_lease


def heartbeat_workflow_lease(
    run_id: str,
    worker_id: str | None = None,
    lease_seconds: int | None = None,
) -> WorkflowLease:

    if worker_id is None:

        worker_id = (
            PROCESS_WORKER_ID
        )


    if lease_seconds is None:

        lease_seconds = (
            CONFIG.workflow_lease_seconds
        )

    (
        heartbeat_at,
        lease_expires_at,
    ) = build_lease_times(
        lease_seconds
    )

    update_workflow_lease_record(
        run_id=run_id,
        worker_id=worker_id,
        heartbeat_at=(
            heartbeat_at
        ),
        lease_expires_at=(
            lease_expires_at
        ),
    )

    lease = get_workflow_lease(
        run_id
    )


    if lease is None:

        raise RuntimeError(
            "Workflow lease disappeared."
        )

    record_workflow_event(
        run_id=run_id,

        event_type="heartbeat",

        stage=None,

        message=(
            "Workflow heartbeat renewed."
        ),

        metadata={
            "worker_id": (
                worker_id
            ),

            "lease_expires_at": (
                lease.lease_expires_at
            ),
        },
    )

    return lease


def workflow_lease_is_stale(
    lease: WorkflowLease,
    now: datetime | None = None,
) -> bool:

    if now is None:

        now = datetime.now(
            timezone.utc
        )

    expires = (
        datetime.fromisoformat(
            lease.lease_expires_at
        )
    )

    return expires <= now


def find_stale_workflow_runs(
) -> list[
    tuple[
        WorkflowRun,
        WorkflowLease | None,
    ]
]:

    stale = []

    now = datetime.now(
        timezone.utc
    )

    for run in (
        get_running_workflow_runs()
    ):

        lease = get_workflow_lease(
            run.run_id
        )

        if lease is None:

            stale.append(
                (
                    run,
                    None,
                )
            )

            continue

        if workflow_lease_is_stale(
            lease,
            now=now,
        ):

            stale.append(
                (
                    run,
                    lease,
                )
            )

    return stale


def fail_stale_workflow_run(
    run_id: str,
) -> WorkflowRun:

    checked_at = datetime.now(
        timezone.utc
    ).isoformat()

    changed = fail_workflow_if_stale(
        run_id=run_id,

        checked_at=(
            checked_at
        ),

        failure=(
            "Workflow liveness could not "
            "be established. The lease was "
            "missing or expired."
        ),
    )

    if not changed:

        raise RuntimeError(
            (
                "Workflow is no longer stale "
                "or is no longer running."
            )
        )

    run = get_workflow_run(
        run_id
    )


    if run is None:

        raise RuntimeError(
            "Could not reload stale workflow."
        )

    record_workflow_event(
        run_id=run_id,

        event_type="stale_detected",

        stage=run.current_stage,

        message=(
            "Workflow was marked failed "
            "after liveness could no "
            "longer be established."
        ),

        metadata={},
    )

    return run

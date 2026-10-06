import json
import sqlite3

from datetime import datetime, timezone

from config import (
    get_config,
)

from models import (
    ApprovalRecord,
    CampaignMemory,
    CampaignOutcome,
    CompleteSalesMessage,
    IdempotencyRecord,
    VisualApprovalRecord,
    VisualAsset,
    WorkflowCheckpoint,
    WorkflowEvent,
    WorkflowLease,
    WorkflowRun,
)

from outcome_data import (
    validate_campaign_outcome,
)


CONFIG = get_config()


DATABASE_NAME = str(
    CONFIG.database_path
)


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def initialize_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_description TEXT NOT NULL,
            audience TEXT NOT NULL,
            campaign_objective TEXT NOT NULL,
            tone TEXT NOT NULL,
            preferred_words TEXT,
            avoided_words TEXT,
            headline TEXT NOT NULL,
            body TEXT NOT NULL,
            cta TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS brand_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            tone TEXT NOT NULL,
            preferred_words TEXT NOT NULL DEFAULT '',
            avoided_words TEXT NOT NULL DEFAULT ''
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS approved_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_profile_id INTEGER NOT NULL,
            claim_text TEXT NOT NULL,
            evidence_note TEXT NOT NULL DEFAULT '',
            source_reference TEXT NOT NULL DEFAULT '',
            verification_status TEXT NOT NULL DEFAULT 'unverified',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (brand_profile_id) REFERENCES brand_profiles(id),
            UNIQUE (brand_profile_id, claim_text)
        )
        """
    )

    cursor.execute(
        """
        PRAGMA table_info(approved_claims)
        """
    )

    approved_claim_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "evidence_note" not in approved_claim_columns:
        cursor.execute(
            """
            ALTER TABLE approved_claims
            ADD COLUMN evidence_note TEXT NOT NULL DEFAULT ''
            """
        )

    if "source_reference" not in approved_claim_columns:
        cursor.execute(
            """
            ALTER TABLE approved_claims
            ADD COLUMN source_reference TEXT NOT NULL DEFAULT ''
            """
        )

    if "verification_status" not in approved_claim_columns:
        cursor.execute(
            """
            ALTER TABLE approved_claims
            ADD COLUMN verification_status TEXT NOT NULL DEFAULT 'unverified'
            """
        )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS draft_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            headline TEXT NOT NULL,
            body TEXT NOT NULL,
            cta TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'unknown',
            note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
        """
    )

    cursor.execute(
        """
        PRAGMA table_info(draft_versions)
        """
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "source" not in existing_columns:
        cursor.execute(
            """
            ALTER TABLE draft_versions
            ADD COLUMN source TEXT NOT NULL DEFAULT 'unknown'
            """
        )

    if "note" not in existing_columns:
        cursor.execute(
            """
            ALTER TABLE draft_versions
            ADD COLUMN note TEXT NOT NULL DEFAULT ''
            """
        )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS approval_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            campaign_id INTEGER NOT NULL,

            status TEXT NOT NULL,

            reviewer TEXT NOT NULL DEFAULT '',

            note TEXT NOT NULL DEFAULT '',

            approved_message_snapshot TEXT NOT NULL,

            approved_at TEXT,

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS campaign_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            campaign_id INTEGER NOT NULL UNIQUE,

            approved_angle TEXT NOT NULL,

            approved_big_idea TEXT NOT NULL,

            approved_message TEXT NOT NULL,

            evidence_boundaries TEXT NOT NULL,

            outcome_context TEXT NOT NULL,

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS visual_approval_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            campaign_id INTEGER NOT NULL,

            visual_path TEXT NOT NULL,
            visual_sha256 TEXT NOT NULL,

            generation_spec_snapshot TEXT NOT NULL,
            visual_review_snapshot TEXT NOT NULL,

            status TEXT NOT NULL,

            reviewer TEXT,
            note TEXT NOT NULL DEFAULT '',

            approved_visual_snapshot_path TEXT,
            approved_visual_sha256 TEXT,

            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            decided_at TEXT,

            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS visual_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            campaign_id INTEGER NOT NULL,

            visual_path TEXT NOT NULL,
            approved_snapshot_path TEXT NOT NULL,

            sha256 TEXT NOT NULL,

            channel TEXT NOT NULL,

            strategy_angle TEXT NOT NULL,
            visual_job TEXT NOT NULL,

            created_at TEXT NOT NULL,

            approval_record_id INTEGER NOT NULL UNIQUE,

            usage_status TEXT NOT NULL
                CHECK (
                    usage_status IN (
                        'available',
                        'in_use',
                        'retired'
                    )
                ),

            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(id),

            FOREIGN KEY (approval_record_id)
                REFERENCES visual_approval_records(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS campaign_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            campaign_id INTEGER NOT NULL,

            channel TEXT NOT NULL,

            impressions INTEGER NOT NULL,
            clicks INTEGER NOT NULL,
            conversions INTEGER NOT NULL,

            spend REAL NOT NULL,
            revenue REAL NOT NULL,

            measured_from TEXT NOT NULL,
            measured_to TEXT NOT NULL,

            source TEXT NOT NULL,

            data_quality TEXT NOT NULL
                CHECK (
                    data_quality IN (
                        'verified',
                        'manual',
                        'estimated',
                        'incomplete'
                    )
                ),

            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_runs (
            run_id TEXT PRIMARY KEY,

            workflow_name TEXT NOT NULL,

            started_at TEXT NOT NULL,

            completed_at TEXT,

            status TEXT NOT NULL
                CHECK (
                    status IN (
                        'running',
                        'completed',
                        'failed'
                    )
                ),

            config_snapshot TEXT NOT NULL,

            current_stage TEXT NOT NULL,

            failure TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_leases (
            run_id TEXT PRIMARY KEY,

            worker_id TEXT NOT NULL,

            heartbeat_at TEXT NOT NULL,

            lease_expires_at TEXT NOT NULL,

            FOREIGN KEY (run_id)
                REFERENCES workflow_runs(run_id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_events (
            event_id TEXT PRIMARY KEY,

            run_id TEXT NOT NULL,

            event_type TEXT NOT NULL,

            stage TEXT,

            occurred_at TEXT NOT NULL,

            message TEXT NOT NULL,

            metadata_json TEXT NOT NULL,

            FOREIGN KEY (run_id)
                REFERENCES workflow_runs(run_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_workflow_events_run_time

        ON workflow_events (
            run_id,
            occurred_at
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id TEXT NOT NULL,

            stage TEXT NOT NULL,

            artifact_type TEXT NOT NULL,

            artifact_reference TEXT NOT NULL,

            artifact_hash TEXT NOT NULL,

            created_at TEXT NOT NULL,

            valid INTEGER NOT NULL
                CHECK (
                    valid IN (0, 1)
                ),

            UNIQUE (
                run_id,
                stage,
                artifact_type
            ),

            FOREIGN KEY (run_id)
                REFERENCES workflow_runs(run_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS idempotency_records (
            idempotency_key TEXT PRIMARY KEY,

            operation TEXT NOT NULL,

            request_fingerprint TEXT NOT NULL,

            run_id TEXT NOT NULL UNIQUE,

            status TEXT NOT NULL
                CHECK (
                    status IN (
                        'in_progress',
                        'completed',
                        'failed'
                    )
                ),

            created_at TEXT NOT NULL,

            completed_at TEXT,

            FOREIGN KEY (run_id)
                REFERENCES workflow_runs(run_id)
        )
        """
    )

    connection.commit()
    connection.close()


def save_campaign(brief, draft):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO campaigns (
            product_description,
            audience,
            campaign_objective,
            tone,
            preferred_words,
            avoided_words,
            headline,
            body,
            cta
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            brief.product_description,
            brief.audience,
            brief.campaign_objective,
            brief.tone,
            brief.preferred_words,
            brief.avoided_words,
            draft.headline,
            draft.body,
            draft.cta
        )
    )

    campaign_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return campaign_id


def get_campaigns():
    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            product_description,
            audience,
            campaign_objective,
            tone,
            preferred_words,
            avoided_words,
            headline,
            body,
            cta
        FROM campaigns
        ORDER BY id DESC
        """
    )

    campaigns = cursor.fetchall()

    connection.close()

    return campaigns


def save_draft_version(
    campaign_id,
    draft,
    source,
    note
):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(version_number)
        FROM draft_versions
        WHERE campaign_id = ?
        """,
        (campaign_id,)
    )

    last_version = cursor.fetchone()[0]

    if last_version is None:
        version_number = 1
    else:
        version_number = last_version + 1

    cursor.execute(
        """
        INSERT INTO draft_versions (
            campaign_id,
            version_number,
            headline,
            body,
            cta,
            source,
            note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            campaign_id,
            version_number,
            draft.headline,
            draft.body,
            draft.cta,
            source,
            note
        )
    )

    cursor.execute(
        """
        UPDATE campaigns
        SET
            headline = ?,
            body = ?,
            cta = ?
        WHERE id = ?
        """,
        (
            draft.headline,
            draft.body,
            draft.cta,
            campaign_id
        )
    )

    connection.commit()
    connection.close()

    return version_number


def get_draft_versions(campaign_id):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            campaign_id,
            version_number,
            headline,
            body,
            cta,
            source,
            note,
            created_at
        FROM draft_versions
        WHERE campaign_id = ?
        ORDER BY version_number DESC
        """,
        (campaign_id,)
    )

    versions = cursor.fetchall()

    connection.close()

    return versions


def save_brand_profile(profile):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO brand_profiles (
            name,
            tone,
            preferred_words,
            avoided_words
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            tone = excluded.tone,
            preferred_words = excluded.preferred_words,
            avoided_words = excluded.avoided_words
        """,
        (
            profile.name,
            profile.tone,
            profile.preferred_words,
            profile.avoided_words
        )
    )

    connection.commit()
    connection.close()


def get_brand_profiles():
    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            tone,
            preferred_words,
            avoided_words
        FROM brand_profiles
        ORDER BY name
        """
    )

    profiles = cursor.fetchall()

    connection.close()

    return profiles


def save_approved_claim(
    brand_profile_id,
    claim_text,
    evidence_note,
    source_reference,
    verification_status
):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO approved_claims (
            brand_profile_id,
            claim_text,
            evidence_note,
            source_reference,
            verification_status
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(brand_profile_id, claim_text)
        DO UPDATE SET
            evidence_note = excluded.evidence_note,
            source_reference = excluded.source_reference,
            verification_status = excluded.verification_status
        """,
        (
            brand_profile_id,
            claim_text,
            evidence_note,
            source_reference,
            verification_status
        )
    )

    connection.commit()
    connection.close()


def get_approved_claims(brand_profile_id):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            claim_text,
            evidence_note,
            source_reference,
            verification_status,
            created_at
        FROM approved_claims
        WHERE brand_profile_id = ?
        ORDER BY id
        """,
        (brand_profile_id,)
    )

    claims = cursor.fetchall()

    connection.close()

    return claims

def create_approval_request(
    campaign_id: int,
    message: CompleteSalesMessage,
) -> int:

    snapshot = json.dumps(
        message.model_dump(),
        indent=2,
    )

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO approval_records (
            campaign_id,
            status,
            reviewer,
            note,
            approved_message_snapshot,
            approved_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            campaign_id,
            "awaiting human approval",
            "",
            "",
            snapshot,
            None,
        ),
    )

    approval_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return approval_id


def decide_approval(
    approval_id: int,
    decision: str,
    reviewer: str,
    note: str,
) -> None:

    normalized_decision = (
        decision.strip().lower()
    )

    if normalized_decision not in {
        "approved",
        "rejected",
    }:
        raise ValueError(
            "Decision must be 'approved' or 'rejected'."
        )

    existing = get_approval_record(
        approval_id
    )


    if existing is None:
        raise ValueError(
            "Approval record was not found."
        )


    if existing.status != "awaiting human approval":
        raise ValueError(
            "This approval request has already been decided."
        )

    if normalized_decision == "approved":

        approved_at = datetime.now(
            timezone.utc
        ).isoformat()

    else:

        approved_at = None

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE approval_records

        SET
            status = ?,
            reviewer = ?,
            note = ?,
            approved_at = ?

        WHERE id = ?
        """,
        (
            normalized_decision,
            reviewer,
            note,
            approved_at,
            approval_id,
        ),
    )

    connection.commit()
    connection.close()


def get_approval_record(
    approval_id: int,
) -> ApprovalRecord | None:

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            campaign_id,
            status,
            reviewer,
            note,
            approved_message_snapshot,
            approved_at

        FROM approval_records

        WHERE id = ?
        """,
        (approval_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return ApprovalRecord(
        id=row["id"],
        campaign_id=row["campaign_id"],
        status=row["status"],
        reviewer=row["reviewer"],
        note=row["note"],
        approved_message_snapshot=(
            row["approved_message_snapshot"]
        ),
        approved_at=row["approved_at"],
    )


def get_latest_approved_record(
    campaign_id: int,
) -> ApprovalRecord | None:

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            campaign_id,
            status,
            reviewer,
            note,
            approved_message_snapshot,
            approved_at

        FROM approval_records

        WHERE
            campaign_id = ?
            AND status = 'approved'

        ORDER BY id DESC

        LIMIT 1
        """,
        (campaign_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return ApprovalRecord(
        id=row["id"],
        campaign_id=row["campaign_id"],
        status=row["status"],
        reviewer=row["reviewer"],
        note=row["note"],
        approved_message_snapshot=(
            row["approved_message_snapshot"]
        ),
        approved_at=row["approved_at"],
    )


def save_campaign_memory(
    memory: CampaignMemory,
) -> None:

    evidence_json = json.dumps(
        memory.evidence_boundaries
    )

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO campaign_memories (
            campaign_id,
            approved_angle,
            approved_big_idea,
            approved_message,
            evidence_boundaries,
            outcome_context
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(campaign_id)
        DO UPDATE SET

            approved_angle =
                excluded.approved_angle,

            approved_big_idea =
                excluded.approved_big_idea,

            approved_message =
                excluded.approved_message,

            evidence_boundaries =
                excluded.evidence_boundaries,

            outcome_context =
                excluded.outcome_context,

            updated_at =
                CURRENT_TIMESTAMP
        """,
        (
            memory.campaign_id,
            memory.approved_angle,
            memory.approved_big_idea,
            memory.approved_message,
            evidence_json,
            memory.outcome_context,
        ),
    )

    connection.commit()
    connection.close()


def get_campaign_memories() -> list[CampaignMemory]:

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            campaign_id,
            approved_angle,
            approved_big_idea,
            approved_message,
            evidence_boundaries,
            outcome_context

        FROM campaign_memories

        ORDER BY updated_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    memories = []

    for row in rows:

        evidence_boundaries = json.loads(
            row["evidence_boundaries"]
        )

        memory = CampaignMemory(
            campaign_id=row["campaign_id"],
            approved_angle=row["approved_angle"],
            approved_big_idea=(
                row["approved_big_idea"]
            ),
            approved_message=(
                row["approved_message"]
            ),
            evidence_boundaries=(
                evidence_boundaries
            ),
            outcome_context=(
                row["outcome_context"]
            ),
        )

        memories.append(
            memory
        )

    return memories


def create_visual_approval_record(
    campaign_id: int,
    visual_path: str,
    visual_sha256: str,
    generation_spec_snapshot: str,
    visual_review_snapshot: str,
) -> int:

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    existing = cursor.execute(
        """
        SELECT id, status
        FROM visual_approval_records
        WHERE visual_path = ?
          AND visual_sha256 = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            visual_path,
            visual_sha256,
        ),
    ).fetchone()

    if existing is not None:

        connection.close()

        raise ValueError(
            (
                "This exact visual already has "
                "an approval record. "
                f"Record {existing[0]} has status "
                f"'{existing[1]}'."
            )
        )

    cursor.execute(
        """
        INSERT INTO visual_approval_records (
            campaign_id,
            visual_path,
            visual_sha256,
            generation_spec_snapshot,
            visual_review_snapshot,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            campaign_id,
            visual_path,
            visual_sha256,
            generation_spec_snapshot,
            visual_review_snapshot,
            "awaiting human approval",
        ),
    )

    approval_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return approval_id


def get_visual_approval_record(
    approval_id: int,
) -> VisualApprovalRecord | None:

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    row = cursor.execute(
        """
        SELECT
            id,
            campaign_id,
            visual_path,
            visual_sha256,
            generation_spec_snapshot,
            visual_review_snapshot,
            status,
            reviewer,
            note,
            approved_visual_snapshot_path,
            approved_visual_sha256,
            created_at,
            decided_at

        FROM visual_approval_records

        WHERE id = ?
        """,
        (approval_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return VisualApprovalRecord(
        id=row[0],
        campaign_id=row[1],
        visual_path=row[2],
        visual_sha256=row[3],
        generation_spec_snapshot=row[4],
        visual_review_snapshot=row[5],
        status=row[6],
        reviewer=row[7],
        note=row[8],
        approved_visual_snapshot_path=row[9],
        approved_visual_sha256=row[10],
        created_at=row[11],
        decided_at=row[12],
    )


def finalize_visual_approval_record(
    approval_id: int,
    decision: str,
    reviewer: str,
    note: str,
    decided_at: str,
    approved_visual_snapshot_path: str | None,
    approved_visual_sha256: str | None,
) -> None:

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE visual_approval_records

        SET
            status = ?,
            reviewer = ?,
            note = ?,
            approved_visual_snapshot_path = ?,
            approved_visual_sha256 = ?,
            decided_at = ?

        WHERE id = ?
          AND status = 'awaiting human approval'
        """,
        (
            decision,
            reviewer,
            note,
            approved_visual_snapshot_path,
            approved_visual_sha256,
            decided_at,
            approval_id,
        ),
    )

    if cursor.rowcount != 1:

        connection.rollback()
        connection.close()

        raise ValueError(
            (
                "Visual approval record does not exist "
                "or has already been decided."
            )
        )

    connection.commit()
    connection.close()


def save_visual_asset(
    asset: VisualAsset,
) -> int:

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    existing = cursor.execute(
        """
        SELECT
            id,
            approved_snapshot_path,
            sha256

        FROM visual_assets

        WHERE approval_record_id = ?
        """,
        (
            asset.approval_record_id,
        ),
    ).fetchone()

    if existing is not None:

        existing_id = existing[0]
        existing_path = existing[1]
        existing_sha256 = existing[2]

        if (
            existing_path
            != asset.approved_snapshot_path
            or existing_sha256
            != asset.sha256
        ):

            connection.close()

            raise RuntimeError(
                (
                    "Existing visual asset for this "
                    "approval does not match the "
                    "current approved snapshot."
                )
            )

        connection.close()

        return existing_id

    cursor.execute(
        """
        INSERT INTO visual_assets (
            campaign_id,
            visual_path,
            approved_snapshot_path,
            sha256,
            channel,
            strategy_angle,
            visual_job,
            created_at,
            approval_record_id,
            usage_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            asset.campaign_id,
            asset.visual_path,
            asset.approved_snapshot_path,
            asset.sha256,
            asset.channel,
            asset.strategy_angle,
            asset.visual_job,
            asset.created_at,
            asset.approval_record_id,
            asset.usage_status,
        ),
    )

    asset_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return asset_id


def get_visual_assets(
    campaign_id: int | None = None,
) -> list[VisualAsset]:

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    if campaign_id is None:

        rows = cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                visual_path,
                approved_snapshot_path,
                sha256,
                channel,
                strategy_angle,
                visual_job,
                created_at,
                approval_record_id,
                usage_status

            FROM visual_assets

            ORDER BY
                created_at DESC,
                id DESC
            """
        ).fetchall()

    else:

        rows = cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                visual_path,
                approved_snapshot_path,
                sha256,
                channel,
                strategy_angle,
                visual_job,
                created_at,
                approval_record_id,
                usage_status

            FROM visual_assets

            WHERE campaign_id = ?

            ORDER BY
                created_at DESC,
                id DESC
            """,
            (
                campaign_id,
            ),
        ).fetchall()

    connection.close()

    assets = []

    for row in rows:

        asset = VisualAsset(
            id=row[0],
            campaign_id=row[1],
            visual_path=row[2],
            approved_snapshot_path=row[3],
            sha256=row[4],
            channel=row[5],
            strategy_angle=row[6],
            visual_job=row[7],
            created_at=row[8],
            approval_record_id=row[9],
            usage_status=row[10],
        )

        assets.append(
            asset
        )

    return assets


def save_campaign_outcome(
    outcome: CampaignOutcome,
) -> int:

    validate_campaign_outcome(
        outcome
    )

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO campaign_outcomes (
            campaign_id,
            channel,
            impressions,
            clicks,
            conversions,
            spend,
            revenue,
            measured_from,
            measured_to,
            source,
            data_quality
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            outcome.campaign_id,
            outcome.channel,
            outcome.impressions,
            outcome.clicks,
            outcome.conversions,
            outcome.spend,
            outcome.revenue,
            outcome.measured_from,
            outcome.measured_to,
            outcome.source,
            outcome.data_quality,
        ),
    )

    outcome_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return outcome_id


def get_campaign_outcomes(
    campaign_id: int | None = None,
) -> list[CampaignOutcome]:

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    if campaign_id is None:

        rows = cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                channel,
                impressions,
                clicks,
                conversions,
                spend,
                revenue,
                measured_from,
                measured_to,
                source,
                data_quality,
                created_at

            FROM campaign_outcomes

            ORDER BY
                measured_from DESC,
                id DESC
            """
        ).fetchall()

    else:

        rows = cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                channel,
                impressions,
                clicks,
                conversions,
                spend,
                revenue,
                measured_from,
                measured_to,
                source,
                data_quality,
                created_at

            FROM campaign_outcomes

            WHERE campaign_id = ?

            ORDER BY
                measured_from DESC,
                id DESC
            """,
            (
                campaign_id,
            ),
        ).fetchall()

    connection.close()

    outcomes = []

    for row in rows:

        outcome = CampaignOutcome(
            id=row[0],
            campaign_id=row[1],
            channel=row[2],
            impressions=row[3],
            clicks=row[4],
            conversions=row[5],
            spend=row[6],
            revenue=row[7],
            measured_from=row[8],
            measured_to=row[9],
            source=row[10],
            data_quality=row[11],
            created_at=row[12],
        )

        outcomes.append(
            outcome
        )

    return outcomes


def create_workflow_run_record(
    run: WorkflowRun,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workflow_runs (
            run_id,
            workflow_name,
            started_at,
            completed_at,
            status,
            config_snapshot,
            current_stage,
            failure
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run.run_id,
            run.workflow_name,
            run.started_at,
            run.completed_at,
            run.status,
            run.config_snapshot,
            run.current_stage,
            run.failure,
        ),
    )

    connection.commit()
    connection.close()


def get_workflow_run(
    run_id: str,
) -> WorkflowRun | None:

    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            run_id,
            workflow_name,
            started_at,
            completed_at,
            status,
            config_snapshot,
            current_stage,
            failure

        FROM workflow_runs

        WHERE run_id = ?
        """,
        (
            run_id,
        ),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return WorkflowRun(
        run_id=row[0],
        workflow_name=row[1],
        started_at=row[2],
        completed_at=row[3],
        status=row[4],
        config_snapshot=row[5],
        current_stage=row[6],
        failure=row[7],
    )


def update_workflow_run_stage(
    run_id: str,
    stage: str,
) -> None:

    stage = stage.strip()


    if not stage:

        raise ValueError(
            "Workflow stage cannot be empty."
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE workflow_runs

        SET current_stage = ?

        WHERE run_id = ?
          AND status = 'running'
        """,
        (
            stage,
            run_id,
        ),
    )

    if cursor.rowcount != 1:

        connection.rollback()
        connection.close()

        raise ValueError(
            (
                "Workflow run does not exist "
                "or is no longer running."
            )
        )

    connection.commit()
    connection.close()


def complete_workflow_run_record(
    run_id: str,
    completed_at: str,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE workflow_runs

        SET
            status = 'completed',
            completed_at = ?,
            current_stage = 'completed',
            failure = NULL

        WHERE run_id = ?
          AND status = 'running'
        """,
        (
            completed_at,
            run_id,
        ),
    )

    if cursor.rowcount != 1:

        connection.rollback()
        connection.close()

        raise ValueError(
            (
                "Workflow run does not exist "
                "or has already reached a "
                "terminal status."
            )
        )

    cursor.execute(
        """
        UPDATE idempotency_records

        SET
            status = 'completed',
            completed_at = ?

        WHERE run_id = ?
          AND status = 'in_progress'
        """,
        (
            completed_at,
            run_id,
        ),
    )

    cursor.execute(
        """
        DELETE FROM workflow_leases
        WHERE run_id = ?
        """,
        (
            run_id,
        ),
    )

    connection.commit()
    connection.close()


def fail_workflow_run_record(
    run_id: str,
    completed_at: str,
    failure: str,
) -> None:

    failure = failure.strip()


    if not failure:

        failure = (
            "Workflow failed without "
            "a supplied failure summary."
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE workflow_runs

        SET
            status = 'failed',
            completed_at = ?,
            failure = ?

        WHERE run_id = ?
          AND status = 'running'
        """,
        (
            completed_at,
            failure,
            run_id,
        ),
    )

    if cursor.rowcount != 1:

        connection.rollback()
        connection.close()

        raise ValueError(
            (
                "Workflow run does not exist "
                "or has already reached a "
                "terminal status."
            )
        )

    cursor.execute(
        """
        UPDATE idempotency_records

        SET
            status = 'failed',
            completed_at = ?

        WHERE run_id = ?
          AND status = 'in_progress'
        """,
        (
            completed_at,
            run_id,
        ),
    )

    cursor.execute(
        """
        DELETE FROM workflow_leases
        WHERE run_id = ?
        """,
        (
            run_id,
        ),
    )

    connection.commit()
    connection.close()


def get_recent_workflow_runs(
    limit: int = 20,
) -> list[WorkflowRun]:

    if limit < 1:

        raise ValueError(
            "Limit must be at least 1."
        )

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            run_id,
            workflow_name,
            started_at,
            completed_at,
            status,
            config_snapshot,
            current_stage,
            failure

        FROM workflow_runs

        ORDER BY started_at DESC

        LIMIT ?
        """,
        (
            limit,
        ),
    ).fetchall()

    connection.close()

    return [
        WorkflowRun(
            run_id=row[0],
            workflow_name=row[1],
            started_at=row[2],
            completed_at=row[3],
            status=row[4],
            config_snapshot=row[5],
            current_stage=row[6],
            failure=row[7],
        )

        for row in rows
    ]


def save_workflow_checkpoint_record(
    checkpoint: WorkflowCheckpoint,
) -> int:

    connection = get_connection()
    cursor = connection.cursor()

    existing = cursor.execute(
        """
        SELECT
            id,
            artifact_reference,
            artifact_hash,
            valid

        FROM workflow_checkpoints

        WHERE run_id = ?
          AND stage = ?
          AND artifact_type = ?
        """,
        (
            checkpoint.run_id,
            checkpoint.stage,
            checkpoint.artifact_type,
        ),
    ).fetchone()

    if existing is not None:

        existing_id = existing[0]
        existing_reference = existing[1]
        existing_hash = existing[2]
        existing_valid = bool(
            existing[3]
        )

        if (
            existing_reference
            == checkpoint.artifact_reference
            and existing_hash
            == checkpoint.artifact_hash
            and existing_valid
        ):

            connection.close()

            return existing_id

        connection.close()

        raise RuntimeError(
            (
                "A checkpoint already exists "
                "for this run/stage/artifact type "
                "but points to different state."
            )
        )

    cursor.execute(
        """
        INSERT INTO workflow_checkpoints (
            run_id,
            stage,
            artifact_type,
            artifact_reference,
            artifact_hash,
            created_at,
            valid
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            checkpoint.run_id,
            checkpoint.stage,
            checkpoint.artifact_type,
            checkpoint.artifact_reference,
            checkpoint.artifact_hash,
            checkpoint.created_at,
            int(checkpoint.valid),
        ),
    )

    checkpoint_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return checkpoint_id


def get_workflow_checkpoints(
    run_id: str,
) -> list[WorkflowCheckpoint]:

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            run_id,
            stage,
            artifact_type,
            artifact_reference,
            artifact_hash,
            created_at,
            valid

        FROM workflow_checkpoints

        WHERE run_id = ?

        ORDER BY id ASC
        """,
        (
            run_id,
        ),
    ).fetchall()

    connection.close()

    return [
        WorkflowCheckpoint(
            id=row[0],
            run_id=row[1],
            stage=row[2],
            artifact_type=row[3],
            artifact_reference=row[4],
            artifact_hash=row[5],
            created_at=row[6],
            valid=bool(
                row[7]
            ),
        )

        for row in rows
    ]


def invalidate_workflow_checkpoint(
    checkpoint_id: int,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE workflow_checkpoints

        SET valid = 0

        WHERE id = ?
          AND valid = 1
        """,
        (
            checkpoint_id,
        ),
    )

    connection.commit()
    connection.close()


def claim_idempotent_workflow_record(
    record: IdempotencyRecord,
    run: WorkflowRun,
) -> tuple[
    IdempotencyRecord,
    WorkflowRun,
    bool,
]:

    if record.run_id != run.run_id:

        raise ValueError(
            (
                "Idempotency record and "
                "workflow run have different "
                "run IDs."
            )
        )

    if record.status != "in_progress":

        raise ValueError(
            (
                "A newly claimed idempotency "
                "record must start as in_progress."
            )
        )

    if run.status != "running":

        raise ValueError(
            (
                "A newly claimed workflow "
                "must start as running."
            )
        )

    connection = get_connection()

    try:

        connection.execute(
            "BEGIN IMMEDIATE"
        )

        existing_row = connection.execute(
            """
            SELECT
                idempotency_key,
                operation,
                request_fingerprint,
                run_id,
                status,
                created_at,
                completed_at

            FROM idempotency_records

            WHERE idempotency_key = ?
            """,
            (
                record.idempotency_key,
            ),
        ).fetchone()

        if existing_row is not None:

            existing_record = (
                IdempotencyRecord(
                    idempotency_key=(
                        existing_row[0]
                    ),

                    operation=(
                        existing_row[1]
                    ),

                    request_fingerprint=(
                        existing_row[2]
                    ),

                    run_id=(
                        existing_row[3]
                    ),

                    status=(
                        existing_row[4]
                    ),

                    created_at=(
                        existing_row[5]
                    ),

                    completed_at=(
                        existing_row[6]
                    ),
                )
            )

            if (
                existing_record.operation
                != record.operation
            ):

                raise ValueError(
                    (
                        "Idempotency key was reused "
                        "for a different operation."
                    )
                )

            if (
                existing_record
                .request_fingerprint
                != record.request_fingerprint
            ):

                raise ValueError(
                    (
                        "Idempotency key was reused "
                        "with a different request."
                    )
                )

            run_row = connection.execute(
                """
                SELECT
                    run_id,
                    workflow_name,
                    started_at,
                    completed_at,
                    status,
                    config_snapshot,
                    current_stage,
                    failure

                FROM workflow_runs

                WHERE run_id = ?
                """,
                (
                    existing_record.run_id,
                ),
            ).fetchone()

            if run_row is None:

                raise RuntimeError(
                    (
                        "Idempotency record points "
                        "to a missing WorkflowRun."
                    )
                )

            existing_run = WorkflowRun(
                run_id=run_row[0],

                workflow_name=run_row[1],

                started_at=run_row[2],

                completed_at=run_row[3],

                status=run_row[4],

                config_snapshot=run_row[5],

                current_stage=run_row[6],

                failure=run_row[7],
            )

            expected_status = {
                "running": "in_progress",
                "completed": "completed",
                "failed": "failed",
            }[
                existing_run.status
            ]

            if (
                existing_record.status
                != expected_status
            ):

                raise RuntimeError(
                    (
                        "Idempotency record and "
                        "WorkflowRun status have drifted."
                    )
                )

            connection.commit()

            return (
                existing_record,
                existing_run,
                False,
            )

        connection.execute(
            """
            INSERT INTO workflow_runs (
                run_id,
                workflow_name,
                started_at,
                completed_at,
                status,
                config_snapshot,
                current_stage,
                failure
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run.run_id,
                run.workflow_name,
                run.started_at,
                run.completed_at,
                run.status,
                run.config_snapshot,
                run.current_stage,
                run.failure,
            ),
        )

        connection.execute(
            """
            INSERT INTO idempotency_records (
                idempotency_key,
                operation,
                request_fingerprint,
                run_id,
                status,
                created_at,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.idempotency_key,
                record.operation,
                record.request_fingerprint,
                record.run_id,
                record.status,
                record.created_at,
                record.completed_at,
            ),
        )

        connection.commit()

        return (
            record,
            run,
            True,
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def get_idempotency_record(
    idempotency_key: str,
) -> IdempotencyRecord | None:

    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            idempotency_key,
            operation,
            request_fingerprint,
            run_id,
            status,
            created_at,
            completed_at

        FROM idempotency_records

        WHERE idempotency_key = ?
        """,
        (
            idempotency_key,
        ),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return IdempotencyRecord(
        idempotency_key=row[0],
        operation=row[1],
        request_fingerprint=row[2],
        run_id=row[3],
        status=row[4],
        created_at=row[5],
        completed_at=row[6],
    )


def claim_workflow_lease_record(
    lease: WorkflowLease,
) -> WorkflowLease:

    connection = get_connection()

    try:

        connection.execute(
            "BEGIN IMMEDIATE"
        )

        run_row = connection.execute(
            """
            SELECT status
            FROM workflow_runs
            WHERE run_id = ?
            """,
            (
                lease.run_id,
            ),
        ).fetchone()

        if run_row is None:

            raise ValueError(
                "Workflow run does not exist."
            )

        if run_row[0] != "running":

            raise ValueError(
                (
                    "Workflow lease can only "
                    "be acquired for a running run."
                )
            )

        existing = connection.execute(
            """
            SELECT
                run_id,
                worker_id,
                heartbeat_at,
                lease_expires_at

            FROM workflow_leases

            WHERE run_id = ?
            """,
            (
                lease.run_id,
            ),
        ).fetchone()

        if existing is not None:

            existing_lease = WorkflowLease(
                run_id=existing[0],
                worker_id=existing[1],
                heartbeat_at=existing[2],
                lease_expires_at=existing[3],
            )

            if (
                existing_lease.worker_id
                == lease.worker_id
            ):

                connection.commit()

                return existing_lease

            raise RuntimeError(
                (
                    "Workflow run already has "
                    "a lease owned by another worker."
                )
            )

        connection.execute(
            """
            INSERT INTO workflow_leases (
                run_id,
                worker_id,
                heartbeat_at,
                lease_expires_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                lease.run_id,
                lease.worker_id,
                lease.heartbeat_at,
                lease.lease_expires_at,
            ),
        )

        connection.commit()

        return lease

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def get_workflow_lease(
    run_id: str,
) -> WorkflowLease | None:

    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            run_id,
            worker_id,
            heartbeat_at,
            lease_expires_at

        FROM workflow_leases

        WHERE run_id = ?
        """,
        (
            run_id,
        ),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return WorkflowLease(
        run_id=row[0],
        worker_id=row[1],
        heartbeat_at=row[2],
        lease_expires_at=row[3],
    )


def update_workflow_lease_record(
    run_id: str,
    worker_id: str,
    heartbeat_at: str,
    lease_expires_at: str,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE workflow_leases

        SET
            heartbeat_at = ?,
            lease_expires_at = ?

        WHERE run_id = ?
          AND worker_id = ?
          AND EXISTS (
              SELECT 1
              FROM workflow_runs
              WHERE workflow_runs.run_id = ?
                AND workflow_runs.status = 'running'
          )
        """,
        (
            heartbeat_at,
            lease_expires_at,
            run_id,
            worker_id,
            run_id,
        ),
    )

    if cursor.rowcount != 1:

        connection.rollback()
        connection.close()

        raise RuntimeError(
            (
                "Workflow heartbeat was rejected. "
                "The run may be terminal or the "
                "lease may belong to another worker."
            )
        )

    connection.commit()
    connection.close()


def get_running_workflow_runs(
) -> list[WorkflowRun]:

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            run_id,
            workflow_name,
            started_at,
            completed_at,
            status,
            config_snapshot,
            current_stage,
            failure

        FROM workflow_runs

        WHERE status = 'running'

        ORDER BY started_at ASC
        """
    ).fetchall()

    connection.close()

    return [
        WorkflowRun(
            run_id=row[0],
            workflow_name=row[1],
            started_at=row[2],
            completed_at=row[3],
            status=row[4],
            config_snapshot=row[5],
            current_stage=row[6],
            failure=row[7],
        )

        for row in rows
    ]


def fail_workflow_if_stale(
    run_id: str,
    checked_at: str,
    failure: str,
) -> bool:

    connection = get_connection()

    try:

        connection.execute(
            "BEGIN IMMEDIATE"
        )

        run_row = connection.execute(
            """
            SELECT status
            FROM workflow_runs
            WHERE run_id = ?
            """,
            (
                run_id,
            ),
        ).fetchone()

        if (
            run_row is None
            or run_row[0] != "running"
        ):

            connection.commit()

            return False

        lease_row = connection.execute(
            """
            SELECT lease_expires_at
            FROM workflow_leases
            WHERE run_id = ?
            """,
            (
                run_id,
            ),
        ).fetchone()

        checked_time = (
            datetime.fromisoformat(
                checked_at
            )
        )

        if lease_row is not None:

            expiry_time = (
                datetime.fromisoformat(
                    lease_row[0]
                )
            )

            if expiry_time > checked_time:

                connection.commit()

                return False

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE workflow_runs

            SET
                status = 'failed',
                completed_at = ?,
                failure = ?

            WHERE run_id = ?
              AND status = 'running'
            """,
            (
                checked_at,
                failure,
                run_id,
            ),
        )

        cursor.execute(
            """
            UPDATE idempotency_records

            SET
                status = 'failed',
                completed_at = ?

            WHERE run_id = ?
              AND status = 'in_progress'
            """,
            (
                checked_at,
                run_id,
            ),
        )

        cursor.execute(
            """
            DELETE FROM workflow_leases
            WHERE run_id = ?
            """,
            (
                run_id,
            ),
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def append_workflow_event_record(
    event: WorkflowEvent,
) -> None:

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO workflow_events (
                event_id,
                run_id,
                event_type,
                stage,
                occurred_at,
                message,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.run_id,
                event.event_type,
                event.stage,
                event.occurred_at,
                event.message,
                json.dumps(
                    event.metadata,
                    ensure_ascii=False,
                    sort_keys=True,
                    default=str,
                ),
            ),
        )

        connection.commit()

    finally:

        connection.close()


def get_workflow_events(
    run_id: str,
) -> list[WorkflowEvent]:

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            event_id,
            run_id,
            event_type,
            stage,
            occurred_at,
            message,
            metadata_json

        FROM workflow_events

        WHERE run_id = ?

        ORDER BY
            occurred_at ASC,
            rowid ASC
        """,
        (
            run_id,
        ),
    ).fetchall()

    connection.close()

    return [
        WorkflowEvent(
            event_id=row[0],
            run_id=row[1],
            event_type=row[2],
            stage=row[3],
            occurred_at=row[4],
            message=row[5],
            metadata=(
                json.loads(
                    row[6]
                )
            ),
        )

        for row in rows
    ]


def count_workflow_events(
    run_id: str,
) -> int:

    connection = get_connection()

    row = connection.execute(
        """
        SELECT COUNT(*)

        FROM workflow_events

        WHERE run_id = ?
        """,
        (
            run_id,
        ),
    ).fetchone()

    connection.close()

    return int(
        row[0]
    )

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
    VisualApprovalRecord,
    VisualAsset,
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

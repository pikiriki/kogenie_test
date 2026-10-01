import json
import sqlite3

from datetime import datetime, timezone

from models import (
    ApprovalRecord,
    CompleteSalesMessage,
)


DATABASE_NAME = "copy_studio.db"


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

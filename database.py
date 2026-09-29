import sqlite3


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
        CREATE TABLE IF NOT EXISTS draft_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            headline TEXT NOT NULL,
            body TEXT NOT NULL,
            cta TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
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


def save_draft_version(campaign_id, draft):
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
            cta
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            campaign_id,
            version_number,
            draft.headline,
            draft.body,
            draft.cta
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
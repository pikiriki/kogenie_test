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

    connection.commit()

    campaign_id = cursor.lastrowid

    connection.close()

    return campaign_id
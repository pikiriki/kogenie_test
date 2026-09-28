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

    connection.commit()
    connection.close()
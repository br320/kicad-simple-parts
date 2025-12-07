import sqlite3
from pathlib import Path


DATABASE_PATH = Path("kicad_parts.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            value TEXT,
            footprint TEXT,
            symbol TEXT,
            datasheet TEXT,
            lifecycle_state TEXT DEFAULT 'prototype',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS manufacturer_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id INTEGER NOT NULL,
            mfg TEXT NOT NULL,
            mfgpn TEXT NOT NULL,
            datasheet TEXT,
            is_preferred BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
            UNIQUE(mfg, mfgpn)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS component_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id INTEGER NOT NULL,
            revision TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            value TEXT,
            footprint TEXT,
            symbol TEXT,
            datasheet TEXT,
            lifecycle_state TEXT,
            change_message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
            UNIQUE(component_id, revision)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")


if __name__ == "__main__":
    init_db()

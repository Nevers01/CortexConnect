import os
import sqlite3
from models.server import Server

APP_DIR = os.path.join(os.path.expanduser("~"), ".cortex-connect")
DB_PATH = os.path.join(APP_DIR, "servers.db")


def init_db():
    os.makedirs(APP_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                username TEXT NOT NULL,
                password TEXT DEFAULT '',
                notes TEXT DEFAULT ''
            )
        """)
        conn.commit()


def get_servers():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                name,
                type,
                host,
                port,
                username,
                password,
                notes
            FROM servers
            ORDER BY name
        """)

        rows = cur.fetchall()

        return [
            Server(
                id=row["id"],
                name=row["name"],
                type=row["type"],
                host=row["host"],
                port=row["port"],
                username=row["username"],
                password=row["password"],
                notes=row["notes"],
            )
            for row in rows
        ]


def add_server(name, server_type, host, port, username, password, notes):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO servers (name, type, host, port, username, password, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, server_type, host, port, username, password, notes))
        conn.commit()


def update_server(server_id, name, server_type, host, port, username, password, notes):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE servers
            SET name=?, type=?, host=?, port=?, username=?, password=?, notes=?
            WHERE id=?
        """, (name, server_type, host, port, username, password, notes, server_id))
        conn.commit()


def delete_server(server_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM servers WHERE id=?", (server_id,))
        conn.commit()
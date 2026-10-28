"""
SQLite database setup voor LogSync.
Slaat credentials en upload history op.
"""
import sqlite3
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet

DB_PATH = Path(__file__).parent / "logsync.db"
KEY_PATH = Path(__file__).parent / "logsync.key"


def get_or_create_key() -> bytes:
    """Genereer of laad encryptiesleutel voor credentials."""
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()
    key = Fernet.generate_key()
    KEY_PATH.write_bytes(key)
    KEY_PATH.chmod(0o600)
    return key


def encrypt(value: str) -> str:
    f = Fernet(get_or_create_key())
    return f.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    f = Fernet(get_or_create_key())
    return f.decrypt(value.encode()).decode()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS services (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            enabled     INTEGER NOT NULL DEFAULT 0,
            config      TEXT NOT NULL DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS uploads (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT NOT NULL,
            qso_count   INTEGER NOT NULL DEFAULT 0,
            uploaded_at TEXT NOT NULL DEFAULT (datetime('now')),
            results     TEXT NOT NULL DEFAULT '{}'
        );

        -- Standaard services invoegen als ze nog niet bestaan
        INSERT OR IGNORE INTO services (id, name, enabled, config) VALUES
            ('lotw',    'Logbook of the World', 0, '{}'),
            ('eqsl',    'eQSL.cc',              0, '{}'),
            ('qrz',     'QRZ Logbook',          0, '{}'),
            ('clublog', 'Club Log',              0, '{}'),
            ('hrdlog',  'HRDLog.net',            0, '{}');
    """)
    conn.commit()
    conn.close()


def get_services() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM services ORDER BY name").fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["config"] = json.loads(d["config"])
        # Verwijder encryptie-wrapper uit config voor weergave (wachtwoorden leeg tonen)
        safe_config = {}
        for k, v in d["config"].items():
            safe_config[k] = "" if k.endswith("_enc") else v
        d["safe_config"] = safe_config
        result.append(d)
    return result


def get_service(service_id: str) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["config"] = json.loads(d["config"])
    return d


def save_service(service_id: str, enabled: bool, config: dict):
    """Sla service config op. Wachtwoorden worden versleuteld."""
    encrypted_config = {}
    for k, v in config.items():
        if k.endswith("_password") or k.endswith("_key") or k.endswith("_secret"):
            if v:  # Alleen opslaan als er een waarde is
                encrypted_config[k + "_enc"] = encrypt(v)
            else:
                # Behoudt bestaande versleutelde waarde als input leeg is
                existing = get_service(service_id)
                if existing and k + "_enc" in existing["config"]:
                    encrypted_config[k + "_enc"] = existing["config"][k + "_enc"]
        else:
            encrypted_config[k] = v

    conn = get_db()
    conn.execute(
        "UPDATE services SET enabled = ?, config = ? WHERE id = ?",
        (1 if enabled else 0, json.dumps(encrypted_config), service_id)
    )
    conn.commit()
    conn.close()


def get_decrypted_config(service_id: str) -> dict:
    """Haal config op met gedecodeerde wachtwoorden."""
    service = get_service(service_id)
    if not service:
        return {}
    config = service["config"]
    result = {}
    for k, v in config.items():
        if k.endswith("_enc"):
            plain_key = k[:-4]  # Verwijder _enc suffix
            try:
                result[plain_key] = decrypt(v)
            except Exception:
                result[plain_key] = ""
        else:
            result[k] = v
    return result


def save_upload(filename: str, qso_count: int, results: dict) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO uploads (filename, qso_count, results) VALUES (?, ?, ?)",
        (filename, qso_count, json.dumps(results))
    )
    conn.commit()
    upload_id = cur.lastrowid
    conn.close()
    return upload_id


def get_uploads(limit: int = 50) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM uploads ORDER BY uploaded_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["results"] = json.loads(d["results"])
        result.append(d)
    return result

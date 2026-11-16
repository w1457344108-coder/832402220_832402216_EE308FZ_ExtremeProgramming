"""SQLite persistence layer for contacts and multiple contact methods."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from flask import current_app, g

VALID_METHOD_TYPES = ("phone", "email", "social", "address", "other")


def _utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_db() -> sqlite3.Connection:
    """Get a request-scoped SQLite connection with foreign keys enabled."""
    if "db" not in g:
        conn = sqlite3.connect(current_app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db


def close_db(_err: Exception | None = None) -> None:
    """Close the request-scoped SQLite connection if opened."""
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db() -> None:
    """Create tables and indexes if they do not already exist."""
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL DEFAULT '',
            title TEXT NOT NULL DEFAULT '',
            notes TEXT NOT NULL DEFAULT '',
            is_favorite INTEGER NOT NULL DEFAULT 0 CHECK (is_favorite IN (0, 1)),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS contact_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            method_type TEXT NOT NULL CHECK (
                method_type IN ('phone', 'email', 'social', 'address', 'other')
            ),
            label TEXT NOT NULL DEFAULT '',
            value TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_contacts_favorite
            ON contacts (is_favorite, name);
        CREATE INDEX IF NOT EXISTS idx_methods_contact
            ON contact_methods (contact_id, sort_order);
        """
    )
    db.commit()


def normalize_methods(raw_methods: Any) -> list[dict[str, str]]:
    """Validate and normalize a list of contact method dicts."""
    if raw_methods is None:
        return []
    if not isinstance(raw_methods, list):
        raise ValueError("Field 'methods' must be a list.")

    normalized: list[dict[str, str]] = []
    for idx, item in enumerate(raw_methods):
        if not isinstance(item, dict):
            raise ValueError(f"Contact method at index {idx} must be an object.")
        method_type = str(item.get("method_type", "other")).strip().lower()
        if method_type not in VALID_METHOD_TYPES:
            raise ValueError(
                f"Invalid method_type '{method_type}'. Expected one of: {', '.join(VALID_METHOD_TYPES)}."
            )
        value = str(item.get("value", "")).strip()
        if not value:
            continue
        label = str(item.get("label", "")).strip()
        normalized.append(
            {
                "method_type": method_type,
                "label": label,
                "value": value,
            }
        )
    return normalized


def normalize_contact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize incoming contact fields."""
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    name = str(payload.get("name", "")).strip()
    if not name:
        raise ValueError("Contact name is required.")

    return {
        "name": name,
        "company": str(payload.get("company", "")).strip(),
        "title": str(payload.get("title", "")).strip(),
        "notes": str(payload.get("notes", "")).strip(),
        "is_favorite": bool(payload.get("is_favorite", False)),
        "methods": normalize_methods(payload.get("methods", [])),
    }


def _row_to_contact(row: sqlite3.Row, methods: list[dict[str, Any]]) -> dict[str, Any]:
    """Convert a database contact row and its methods into a JSON-serializable dict."""
    return {
        "id": row["id"],
        "name": row["name"],
        "company": row["company"],
        "title": row["title"],
        "notes": row["notes"],
        "is_favorite": bool(row["is_favorite"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "methods": methods,
    }


def _fetch_methods_map(db: sqlite3.Connection, contact_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
    """Batch-load contact methods for a list of contact IDs."""
    if not contact_ids:
        return {}

    placeholders = ",".join("?" for _ in contact_ids)
    rows = db.execute(
        f"""
        SELECT id, contact_id, method_type, label, value, sort_order
        FROM contact_methods
        WHERE contact_id IN ({placeholders})
        ORDER BY sort_order ASC, id ASC
        """,
        contact_ids,
    ).fetchall()

    grouped: dict[int, list[dict[str, Any]]] = {cid: [] for cid in contact_ids}
    for row in rows:
        grouped[row["contact_id"]].append(
            {
                "id": row["id"],
                "method_type": row["method_type"],
                "label": row["label"],
                "value": row["value"],
                "sort_order": row["sort_order"],
            }
        )
    return grouped


def get_contact_counts() -> dict[str, int]:
    """Return total and bookmarked contact counts."""
    db = get_db()
    row = db.execute(
        """
        SELECT
            COUNT(*) AS total_count,
            COALESCE(SUM(is_favorite), 0) AS favorite_count
        FROM contacts
        """
    ).fetchone()
    return {
        "total_count": int(row["total_count"]),
        "favorite_count": int(row["favorite_count"]),
    }


def list_contacts(
    query: str = "",
    favorite_only: bool = False,
    sort_by: str = "favorites",
) -> list[dict[str, Any]]:
    """List contacts filtered by optional search query and favorite status."""
    db = get_db()
    clauses: list[str] = []
    params: list[Any] = []

    if favorite_only:
        clauses.append("c.is_favorite = 1")

    cleaned_query = query.strip()
    if cleaned_query:
        like_pattern = f"%{cleaned_query}%"
        clauses.append(
            """
            (
                c.name LIKE ?
                OR c.company LIKE ?
                OR c.title LIKE ?
                OR c.notes LIKE ?
                OR EXISTS (
                    SELECT 1 FROM contact_methods cm
                    WHERE cm.contact_id = c.id
                      AND (cm.value LIKE ? OR cm.label LIKE ?)
                )
            )
            """
        )
        params.extend([like_pattern] * 6)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    order_map = {
        "favorites": "c.is_favorite DESC, LOWER(c.name) ASC, c.id DESC",
        "name": "LOWER(c.name) ASC, c.id DESC",
        "recent": "c.updated_at DESC, c.id DESC",
    }
    order_sql = order_map.get(sort_by, order_map["favorites"])

    rows = db.execute(
        f"""
        SELECT c.*
        FROM contacts c
        {where_sql}
        ORDER BY {order_sql}
        """,
        params,
    ).fetchall()

    methods_map = _fetch_methods_map(db, [row["id"] for row in rows])
    return [_row_to_contact(row, methods_map.get(row["id"], [])) for row in rows]


def get_contact(contact_id: int) -> dict[str, Any] | None:
    """Return a single contact by ID or None if not found."""
    db = get_db()
    row = db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if row is None:
        return None
    methods_map = _fetch_methods_map(db, [contact_id])
    return _row_to_contact(row, methods_map.get(contact_id, []))


def _insert_methods(db: sqlite3.Connection, contact_id: int, methods: list[dict[str, str]]) -> None:
    """Insert ordered contact methods for a given contact."""
    db.executemany(
        """
        INSERT INTO contact_methods (contact_id, method_type, label, value, sort_order)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (contact_id, m["method_type"], m["label"], m["value"], idx)
            for idx, m in enumerate(methods)
        ],
    )


def create_contact(data: dict[str, Any]) -> dict[str, Any]:
    """Insert a new contact and its contact methods."""
    normalized = normalize_contact_payload(data)
    db = get_db()
    now = _utc_now_iso()

    cursor = db.execute(
        """
        INSERT INTO contacts (name, company, title, notes, is_favorite, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            normalized["name"],
            normalized["company"],
            normalized["title"],
            normalized["notes"],
            1 if normalized["is_favorite"] else 0,
            now,
            now,
        ),
    )
    contact_id = int(cursor.lastrowid)
    _insert_methods(db, contact_id, normalized["methods"])
    db.commit()
    created = get_contact(contact_id)
    assert created is not None
    return created


def update_contact(contact_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
    """Update an existing contact and replace its contact methods."""
    db = get_db()
    existing = db.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if existing is None:
        return None

    normalized = normalize_contact_payload(data)
    now = _utc_now_iso()
    db.execute(
        """
        UPDATE contacts
        SET name = ?, company = ?, title = ?, notes = ?, is_favorite = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            normalized["name"],
            normalized["company"],
            normalized["title"],
            normalized["notes"],
            1 if normalized["is_favorite"] else 0,
            now,
            contact_id,
        ),
    )
    db.execute("DELETE FROM contact_methods WHERE contact_id = ?", (contact_id,))
    _insert_methods(db, contact_id, normalized["methods"])
    db.commit()
    return get_contact(contact_id)


def set_contact_favorite(contact_id: int, is_favorite: bool | None = None) -> dict[str, Any] | None:
    """Set or toggle the bookmark status of a contact."""
    db = get_db()
    row = db.execute("SELECT is_favorite FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if row is None:
        return None

    next_value = (not bool(row["is_favorite"])) if is_favorite is None else bool(is_favorite)
    db.execute(
        "UPDATE contacts SET is_favorite = ?, updated_at = ? WHERE id = ?",
        (1 if next_value else 0, _utc_now_iso(), contact_id),
    )
    db.commit()
    return get_contact(contact_id)


def delete_contact(contact_id: int) -> bool:
    """Delete a contact by ID. Returns True if a row was removed."""
    db = get_db()
    cursor = db.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    db.commit()
    return cursor.rowcount > 0


DEMO_CONTACTS: list[dict[str, Any]] = [
    {
        "name": "Lin Wei",
        "company": "Fuzhou Cloud Tech",
        "title": "Backend Lead",
        "is_favorite": True,
        "notes": "Key project collaborator for API & database review.",
        "methods": [
            {"method_type": "phone", "label": "Mobile", "value": "13800138001"},
            {"method_type": "phone", "label": "Office", "value": "0591-88886601"},
            {"method_type": "email", "label": "Work", "value": "linwei@fzcloud.example"},
            {"method_type": "social", "label": "WeChat", "value": "linwei_dev"},
            {"method_type": "address", "label": "Office", "value": "No. 2 Xueyuan Rd, Fuzhou"},
        ],
    },
    {
        "name": "Chen Yu",
        "company": "Minjiang Design Studio",
        "title": "UI/UX Designer",
        "is_favorite": True,
        "notes": "Handles interface review and demo assets.",
        "methods": [
            {"method_type": "phone", "label": "Mobile", "value": "13900139002"},
            {"method_type": "email", "label": "Personal", "value": "chenyu.design@example.com"},
            {"method_type": "social", "label": "GitHub", "value": "@chenyu-ui"},
        ],
    },
    {
        "name": "Zhang Min",
        "company": "FZU-MU Software Lab",
        "title": "Teaching Assistant",
        "is_favorite": False,
        "notes": "Weekly sprint check-ins on Thursdays.",
        "methods": [
            {"method_type": "phone", "label": "Campus", "value": "0591-22860000"},
            {"method_type": "email", "label": "Academic", "value": "zhangmin@fzu.example.edu"},
            {"method_type": "address", "label": "Lab", "value": "Qishan Campus Bldg 3, Room 402"},
        ],
    },
    {
        "name": "Alex Morgan",
        "company": "Maynooth Partner Team",
        "title": "QA Engineer",
        "is_favorite": False,
        "notes": "Cross-timezone integration testing partner.",
        "methods": [
            {"method_type": "phone", "label": "Work", "value": "00353-1-7086000"},
            {"method_type": "email", "label": "Work", "value": "alex.morgan@mu.example.ie"},
            {"method_type": "email", "label": "Backup", "value": "amorgan.qa@example.org"},
            {"method_type": "social", "label": "LinkedIn", "value": "in/alex-morgan-qa"},
        ],
    },
]


def seed_demo_contacts() -> int:
    """Insert synthetic demo contacts that do not already exist by exact name."""
    db = get_db()
    existing_names = {
        row["name"] for row in db.execute("SELECT name FROM contacts").fetchall()
    }
    created = 0
    for contact in DEMO_CONTACTS:
        if contact["name"] not in existing_names:
            create_contact(contact)
            created += 1
    return created

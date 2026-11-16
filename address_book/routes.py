"""HTTP routes for the Address Book web UI and JSON/Excel endpoints."""

from __future__ import annotations

import io
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, send_file

from .db import (
    create_contact,
    delete_contact,
    get_contact,
    get_contact_counts,
    list_contacts,
    seed_demo_contacts,
    set_contact_favorite,
    update_contact,
)
from .excel_service import (
    build_template_xlsx,
    export_contacts_to_xlsx,
    import_contacts_from_xlsx,
)

bp = Blueprint("main", __name__)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _parse_bool_arg(raw: str | None) -> bool:
    """Parse common truthy query string flags."""
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes"}


@bp.get("/")
def index():
    """Render the main Address Book web interface."""
    return render_template("index.html")


@bp.get("/api/health")
def health():
    """Return service health and contact counts."""
    return jsonify({"status": "ok", **get_contact_counts()})


@bp.get("/api/contacts")
def api_list_contacts():
    """List contacts with optional search query, bookmark filter, and sort order."""
    query = request.args.get("q", "")
    favorite_only = _parse_bool_arg(request.args.get("favorite"))
    sort_by = request.args.get("sort", "favorites")
    contacts = list_contacts(query=query, favorite_only=favorite_only, sort_by=sort_by)
    return jsonify({"contacts": contacts, **get_contact_counts()})


@bp.post("/api/contacts")
def api_create_contact():
    """Create a new contact and associated contact methods."""
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON payload."}), 400
    try:
        contact = create_contact(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"contact": contact, **get_contact_counts()}), 201


@bp.get("/api/contacts/<int:contact_id>")
def api_get_contact(contact_id: int):
    """Retrieve a single contact by ID."""
    contact = get_contact(contact_id)
    if contact is None:
        return jsonify({"error": "Contact not found."}), 404
    return jsonify({"contact": contact})


@bp.put("/api/contacts/<int:contact_id>")
def api_update_contact(contact_id: int):
    """Update an existing contact and its contact methods."""
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON payload."}), 400
    try:
        contact = update_contact(contact_id, payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if contact is None:
        return jsonify({"error": "Contact not found."}), 404
    return jsonify({"contact": contact, **get_contact_counts()})


@bp.patch("/api/contacts/<int:contact_id>/favorite")
def api_toggle_favorite(contact_id: int):
    """Toggle or explicitly set a contact's bookmark status."""
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    explicit_value = payload.get("is_favorite")
    if explicit_value is not None and not isinstance(explicit_value, bool):
        return jsonify({"error": "Field 'is_favorite' must be a boolean."}), 400

    contact = set_contact_favorite(contact_id, explicit_value)
    if contact is None:
        return jsonify({"error": "Contact not found."}), 404
    return jsonify({"contact": contact, **get_contact_counts()})


@bp.delete("/api/contacts/<int:contact_id>")
def api_delete_contact(contact_id: int):
    """Delete a contact by ID."""
    removed = delete_contact(contact_id)
    if not removed:
        return jsonify({"error": "Contact not found."}), 404
    return jsonify({"deleted": True, **get_contact_counts()})


@bp.post("/api/contacts/seed-demo")
def api_seed_demo():
    """Insert synthetic demo contacts for quick demonstration and testing."""
    created_count = seed_demo_contacts()
    return jsonify({"created_count": created_count, **get_contact_counts()})


@bp.get("/api/contacts/export")
def api_export_contacts():
    """Export all or filtered contacts to an Excel (.xlsx) spreadsheet."""
    favorite_only = _parse_bool_arg(request.args.get("favorite"))
    query = request.args.get("q", "")
    contacts = list_contacts(query=query, favorite_only=favorite_only, sort_by="favorites")
    xlsx_bytes = export_contacts_to_xlsx(contacts)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "bookmarked_" if favorite_only else ""
    filename = f"contacts_{suffix}{timestamp}.xlsx"
    return send_file(
        io.BytesIO(xlsx_bytes),
        mimetype=XLSX_MIME,
        as_attachment=True,
        download_name=filename,
    )


@bp.get("/api/contacts/template")
def api_download_template():
    """Download a sample Excel (.xlsx) import template."""
    xlsx_bytes = build_template_xlsx()
    return send_file(
        io.BytesIO(xlsx_bytes),
        mimetype=XLSX_MIME,
        as_attachment=True,
        download_name="contacts_import_template.xlsx",
    )


@bp.post("/api/contacts/import")
def api_import_contacts():
    """Import contacts from an uploaded Excel (.xlsx) file."""
    uploaded = request.files.get("file")
    if uploaded is None or not uploaded.filename:
        return jsonify({"error": "Please select an .xlsx file to upload."}), 400

    if not uploaded.filename.lower().endswith(".xlsx"):
        return jsonify({"error": "Only .xlsx Excel files are supported."}), 400

    duplicate_mode = request.form.get("duplicate_mode", "skip")
    try:
        result = import_contacts_from_xlsx(uploaded.read(), duplicate_mode=duplicate_mode)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({**result, **get_contact_counts()})

"""Excel export, template generation, and import services using openpyxl."""

from __future__ import annotations

import io
import re
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils.exceptions import InvalidFileException

from .db import DEMO_CONTACTS, create_contact, find_contact_by_name, update_contact

VALID_DUPLICATE_MODES = {"skip", "update", "allow"}

EXPORT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("name", "Name"),
    ("is_favorite", "Favorite"),
    ("company", "Company"),
    ("title", "Title"),
    ("phone", "Phone Numbers"),
    ("email", "Emails"),
    ("social", "Social Media"),
    ("address", "Addresses"),
    ("other", "Other Contacts"),
    ("notes", "Notes"),
)

COLUMN_WIDTHS: dict[int, int] = {
    1: 20,
    2: 12,
    3: 22,
    4: 20,
    5: 32,
    6: 34,
    7: 30,
    8: 34,
    9: 26,
    10: 32,
}

HEADER_ALIASES: dict[str, str] = {
    "name": "name",
    "full name": "name",
    "contact name": "name",
    "姓名": "name",
    "favorite": "is_favorite",
    "favorites": "is_favorite",
    "bookmark": "is_favorite",
    "bookmarked": "is_favorite",
    "starred": "is_favorite",
    "收藏": "is_favorite",
    "是否收藏": "is_favorite",
    "company": "company",
    "organization": "company",
    "公司": "company",
    "单位": "company",
    "title": "title",
    "job title": "title",
    "role": "title",
    "职位": "title",
    "phone": "phone",
    "phones": "phone",
    "phone number": "phone",
    "phone numbers": "phone",
    "mobile": "phone",
    "telephone": "phone",
    "电话": "phone",
    "电话号码": "phone",
    "手机号": "phone",
    "email": "email",
    "emails": "email",
    "e-mail": "email",
    "email address": "email",
    "email addresses": "email",
    "邮箱": "email",
    "电子邮件": "email",
    "social": "social",
    "socials": "social",
    "social media": "social",
    "wechat": "social",
    "社交账号": "social",
    "社交媒体": "social",
    "address": "address",
    "addresses": "address",
    "physical address": "address",
    "地址": "address",
    "实体地址": "address",
    "other": "other",
    "other contacts": "other",
    "其他": "other",
    "其他联系方式": "other",
    "notes": "notes",
    "note": "notes",
    "remarks": "notes",
    "备注": "notes",
}

METHOD_COLUMN_KEYS = ("phone", "email", "social", "address", "other")
TRUTHY_VALUES = {"1", "true", "yes", "y", "是", "收藏", "★"}


def _cell_to_text(value: Any) -> str:
    """Convert an Excel cell value to trimmed string without trailing '.0' on whole floats."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _format_methods_cell(methods: list[dict[str, Any]], method_type: str) -> str:
    """Format all methods of a given type for a single Excel cell."""
    parts: list[str] = []
    for method in methods:
        if method.get("method_type") != method_type:
            continue
        label = str(method.get("label", "")).strip()
        value = str(method.get("value", "")).strip()
        if not value:
            continue
        parts.append(f"{label}: {value}" if label else value)
    return "; ".join(parts)


def _parse_methods_cell(raw_text: str, method_type: str) -> list[dict[str, str]]:
    """Parse semicolon- or newline-separated contact methods from a cell string."""
    if not raw_text:
        return []

    parsed: list[dict[str, str]] = []
    tokens = [chunk.strip() for chunk in re.split(r"[;\n]+", raw_text) if chunk.strip()]
    for token in tokens:
        label = ""
        value = token
        if ":" in token:
            candidate_label, candidate_value = token.split(":", 1)
            stripped_value = candidate_value.lstrip()
            # Avoid splitting URL schemes such as "https://example.com" when unlabeled.
            if candidate_label.strip() and stripped_value and not candidate_value.startswith("//"):
                label = candidate_label.strip()
                value = stripped_value.strip()
        if value:
            parsed.append({"method_type": method_type, "label": label, "value": value})
    return parsed


def _build_workbook(contacts: list[dict[str, Any]]) -> bytes:
    """Build an .xlsx workbook bytes buffer from a list of contact dicts."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Contacts"
    ws.freeze_panes = "A2"

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(fill_type="solid", start_color="334155", end_color="334155")
    header_alignment = Alignment(horizontal="left", vertical="center")
    cell_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    for col_idx, (_key, title) in enumerate(EXPORT_COLUMNS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=title)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        ws.column_dimensions[cell.column_letter].width = COLUMN_WIDTHS.get(col_idx, 20)

    ws.row_dimensions[1].height = 24

    for row_idx, contact in enumerate(contacts, start=2):
        methods = contact.get("methods", [])
        row_values = [
            contact.get("name", ""),
            "Yes" if contact.get("is_favorite") else "No",
            contact.get("company", ""),
            contact.get("title", ""),
            _format_methods_cell(methods, "phone"),
            _format_methods_cell(methods, "email"),
            _format_methods_cell(methods, "social"),
            _format_methods_cell(methods, "address"),
            _format_methods_cell(methods, "other"),
            contact.get("notes", ""),
        ]
        for col_idx, text_val in enumerate(row_values, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=str(text_val))
            # Force text format so phone numbers keep leading zeros in Excel.
            cell.number_format = "@"
            cell.alignment = cell_alignment

    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()


def export_contacts_to_xlsx(contacts: list[dict[str, Any]]) -> bytes:
    """Export the given contacts list to an Excel (.xlsx) byte payload."""
    return _build_workbook(contacts)


def build_template_xlsx() -> bytes:
    """Build a sample import template workbook with two synthetic example rows."""
    return _build_workbook(DEMO_CONTACTS[:2])


def import_contacts_from_xlsx(file_bytes: bytes, duplicate_mode: str = "skip") -> dict[str, Any]:
    """Parse an uploaded .xlsx file and insert or update contacts in the database."""
    mode = (duplicate_mode or "skip").strip().lower()
    if mode not in VALID_DUPLICATE_MODES:
        raise ValueError("Invalid duplicate_mode. Expected 'skip', 'update', or 'allow'.")

    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    try:
        wb = load_workbook(io.BytesIO(file_bytes), data_only=True)
    except (InvalidFileException, OSError, KeyError, ValueError) as exc:
        raise ValueError("Unable to read Excel file. Please upload a valid .xlsx workbook.") from exc

    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError("The Excel worksheet is empty.")

    header_map: dict[int, str] = {}
    for col_idx, raw_header in enumerate(rows[0]):
        normalized = _cell_to_text(raw_header).lower()
        canonical = HEADER_ALIASES.get(normalized)
        if canonical and canonical not in header_map.values():
            header_map[col_idx] = canonical

    if "name" not in header_map.values():
        raise ValueError("Missing required 'Name' column in the first row.")

    imported_contacts: list[dict[str, Any]] = []
    updated_contacts: list[dict[str, Any]] = []
    errors: list[str] = []
    skipped_count = 0

    for row_number, row in enumerate(rows[1:], start=2):
        row_texts = {
            field: _cell_to_text(row[col_idx]) if col_idx < len(row) else ""
            for col_idx, field in header_map.items()
        }
        if not any(row_texts.values()):
            continue

        name = row_texts.get("name", "").strip()
        if not name:
            skipped_count += 1
            errors.append(f"Row {row_number}: skipped because Name is empty.")
            continue

        methods: list[dict[str, str]] = []
        for method_type in METHOD_COLUMN_KEYS:
            methods.extend(_parse_methods_cell(row_texts.get(method_type, ""), method_type))

        fav_raw = row_texts.get("is_favorite", "").strip().lower()
        is_favorite = fav_raw in TRUTHY_VALUES
        contact_payload = {
            "name": name,
            "company": row_texts.get("company", ""),
            "title": row_texts.get("title", ""),
            "notes": row_texts.get("notes", ""),
            "is_favorite": is_favorite,
            "methods": methods,
        }

        existing = find_contact_by_name(name) if mode in {"skip", "update"} else None
        if existing is not None:
            if mode == "skip":
                skipped_count += 1
                errors.append(f"Row {row_number}: skipped duplicate contact '{name}'.")
                continue
            updated = update_contact(int(existing["id"]), contact_payload)
            if updated is not None:
                updated_contacts.append(updated)
            continue

        created = create_contact(contact_payload)
        imported_contacts.append(created)

    return {
        "imported_count": len(imported_contacts),
        "updated_count": len(updated_contacts),
        "skipped_count": skipped_count,
        "errors": errors,
        "contacts": imported_contacts + updated_contacts,
    }

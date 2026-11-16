"""Tests for Excel export, template download, import, and validation."""

from __future__ import annotations

import io

from openpyxl import Workbook, load_workbook


def test_excel_export_layout_and_round_trip_import(client, tmp_path):
    seed_contacts = [
        {
            "name": "Zhang San",
            "company": "Fuzhou Lab",
            "title": "Researcher",
            "is_favorite": True,
            "notes": "实验室联系人",
            "methods": [
                {"method_type": "phone", "label": "Mobile", "value": "0591-12345678"},
                {"method_type": "phone", "label": "Backup", "value": "008613800138000"},
                {"method_type": "email", "label": "Work", "value": "zhang@lab.example"},
                {"method_type": "social", "label": "WeChat", "value": "zhang_wx"},
                {"method_type": "address", "label": "Office", "value": "福州市大学城学园路2号"},
                {"method_type": "other", "label": "", "value": "https://example.com/zhang"},
            ],
        },
        {
            "name": "Li Si",
            "company": "MU Partner",
            "title": "QA",
            "is_favorite": False,
            "notes": "",
            "methods": [
                {"method_type": "email", "label": "", "value": "lisi@example.org"},
            ],
        },
    ]

    created_ids = []
    for item in seed_contacts:
        resp = client.post("/api/contacts", json=item)
        assert resp.status_code == 201
        created_ids.append(resp.get_json()["contact"]["id"])

    export_resp = client.get("/api/contacts/export")
    assert export_resp.status_code == 200
    exported_bytes = export_resp.data

    wb = load_workbook(io.BytesIO(exported_bytes))
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    assert headers == [
        "Name",
        "Favorite",
        "Company",
        "Title",
        "Phone Numbers",
        "Emails",
        "Social Media",
        "Addresses",
        "Other Contacts",
        "Notes",
    ]
    assert ws.max_row == 3  # 1 header + 2 contacts (one row per contact)
    assert ws.cell(row=2, column=1).value == "Zhang San"
    assert ws.cell(row=2, column=2).value == "Yes"
    assert ws.cell(row=2, column=5).number_format == "@"
    assert "0591-12345678" in ws.cell(row=2, column=5).value
    assert "008613800138000" in ws.cell(row=2, column=5).value

    # Delete original records, then re-import exported Excel and verify round-trip fidelity
    for cid in created_ids:
        client.delete(f"/api/contacts/{cid}")

    import_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(exported_bytes), "contacts.xlsx")},
        content_type="multipart/form-data",
    )
    assert import_resp.status_code == 200
    import_data = import_resp.get_json()
    assert import_data["imported_count"] == 2
    assert import_data["skipped_count"] == 0

    reloaded = client.get("/api/contacts").get_json()["contacts"]
    by_name = {c["name"]: c for c in reloaded}
    assert by_name["Zhang San"]["is_favorite"] is True
    assert by_name["Zhang San"]["notes"] == "实验室联系人"
    assert len(by_name["Zhang San"]["methods"]) == 6
    assert any(
        m["method_type"] == "phone" and m["value"] == "008613800138000"
        for m in by_name["Zhang San"]["methods"]
    )
    assert any(
        m["method_type"] == "other" and m["value"] == "https://example.com/zhang"
        for m in by_name["Zhang San"]["methods"]
    )
    assert any(
        m["method_type"] == "address" and m["value"] == "福州市大学城学园路2号"
        for m in by_name["Zhang San"]["methods"]
    )
    assert by_name["Li Si"]["is_favorite"] is False


def test_import_rejects_invalid_headers_and_bad_extensions(client):
    txt_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(b"not excel"), "contacts.csv")},
        content_type="multipart/form-data",
    )
    assert txt_resp.status_code == 400

    wb = Workbook()
    ws = wb.active
    ws.append(["Company", "Phone Numbers"])
    ws.append(["FZU", "123456"])
    buf = io.BytesIO()
    wb.save(buf)

    missing_name_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(buf.getvalue()), "missing_name.xlsx")},
        content_type="multipart/form-data",
    )
    assert missing_name_resp.status_code == 400
    assert "Name" in missing_name_resp.get_json()["error"]


def test_template_download_and_partial_row_skip(client):
    tmpl_resp = client.get("/api/contacts/template")
    assert tmpl_resp.status_code == 200
    assert len(tmpl_resp.data) > 0

    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Phone Numbers"])
    ws.append(["", "13800000000"])  # missing name -> skipped with error message
    ws.append(["Valid Contact", "13900000000"])
    buf = io.BytesIO()
    wb.save(buf)

    resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(buf.getvalue()), "partial.xlsx")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["imported_count"] == 1
    assert data["skipped_count"] == 1
    assert len(data["errors"]) == 1

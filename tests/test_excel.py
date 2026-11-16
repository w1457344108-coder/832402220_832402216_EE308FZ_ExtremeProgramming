"""Tests for Excel export, template download, import, and validation."""

from __future__ import annotations

import io

from openpyxl import Workbook, load_workbook


def test_import_chinese_header_aliases_preserves_methods_and_favorites(client):
    """Chinese headers map to the same fields as the documented English headers."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["姓名", "电话", "邮箱", "收藏"])
    sheet.append(["测试甲", "手机: 008613800138000; 办公: 0591-00112233", "工作: first@example.com", "是"])
    sheet.append(["测试乙", "00012345", "second@example.com", "否"])
    buffer = io.BytesIO()
    workbook.save(buffer)

    response = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(buffer.getvalue()), "chinese_headers.xlsx")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    result = response.get_json()
    assert result["imported_count"] == 2
    assert result["updated_count"] == 0
    assert result["skipped_count"] == 0
    assert result["errors"] == []
    assert result["total_count"] == 2
    assert result["favorite_count"] == 1

    contacts = client.get("/api/contacts").get_json()["contacts"]
    by_name = {contact["name"]: contact for contact in contacts}
    assert by_name["测试甲"]["is_favorite"] is True
    assert by_name["测试乙"]["is_favorite"] is False
    assert {
        (method["method_type"], method["label"], method["value"])
        for method in by_name["测试甲"]["methods"]
    } == {
        ("phone", "手机", "008613800138000"),
        ("phone", "办公", "0591-00112233"),
        ("email", "工作", "first@example.com"),
    }
    assert {
        (method["method_type"], method["value"])
        for method in by_name["测试乙"]["methods"]
    } == {("phone", "00012345"), ("email", "second@example.com")}


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


def test_import_duplicate_modes(client):
    client.post(
        "/api/contacts",
        json={
            "name": "Lin Wei",
            "company": "Old Co",
            "methods": [{"method_type": "phone", "label": "Mobile", "value": "13800000001"}],
        },
    )

    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Company", "Favorite", "Phone Numbers"])
    ws.append(["lin wei", "New Co", "Yes", "Work: 0591-88889999"])
    buf = io.BytesIO()
    wb.save(buf)
    xlsx_bytes = buf.getvalue()

    # 1. Default skip mode keeps existing contact unchanged
    skip_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(xlsx_bytes), "dup.xlsx"), "duplicate_mode": "skip"},
        content_type="multipart/form-data",
    )
    assert skip_resp.status_code == 200
    skip_data = skip_resp.get_json()
    assert skip_data["imported_count"] == 0
    assert skip_data["updated_count"] == 0
    assert skip_data["skipped_count"] == 1
    assert skip_data["total_count"] == 1

    # 2. Update mode updates the existing contact in place
    upd_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(xlsx_bytes), "dup.xlsx"), "duplicate_mode": "update"},
        content_type="multipart/form-data",
    )
    assert upd_resp.status_code == 200
    upd_data = upd_resp.get_json()
    assert upd_data["updated_count"] == 1
    assert upd_data["total_count"] == 1
    contacts = client.get("/api/contacts").get_json()["contacts"]
    assert contacts[0]["company"] == "New Co"
    assert contacts[0]["is_favorite"] is True
    assert contacts[0]["methods"][0]["value"] == "0591-88889999"

    # 3. Allow mode creates an additional entry
    allow_resp = client.post(
        "/api/contacts/import",
        data={"file": (io.BytesIO(xlsx_bytes), "dup.xlsx"), "duplicate_mode": "allow"},
        content_type="multipart/form-data",
    )
    assert allow_resp.status_code == 200
    assert allow_resp.get_json()["imported_count"] == 1
    assert allow_resp.get_json()["total_count"] == 2

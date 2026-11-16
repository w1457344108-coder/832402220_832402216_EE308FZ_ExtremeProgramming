"""Tests for contact CRUD, multiple contact methods, and bookmarking."""

from __future__ import annotations

import pytest

def test_index_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Address Book" in response.data
    assert b"themeSelect" in response.data
    assert b"langToggleBtn" in response.data


def test_create_update_delete_contact_with_multiple_methods(client):
    payload = {
        "name": "Lin Wei",
        "company": "Fuzhou Tech",
        "title": "Engineer",
        "is_favorite": False,
        "notes": "Key collaborator",
        "methods": [
            {"method_type": "phone", "label": "Mobile", "value": "13800138000"},
            {"method_type": "phone", "label": "Office", "value": "0591-88886666"},
            {"method_type": "email", "label": "Work", "value": "linwei@example.com"},
            {"method_type": "social", "label": "WeChat", "value": "linwei_wx"},
            {"method_type": "address", "label": "Home", "value": "Fuzhou University"},
        ],
    }

    create_resp = client.post("/api/contacts", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.get_json()["contact"]
    contact_id = created["id"]

    assert created["name"] == "Lin Wei"
    assert created["is_favorite"] is False
    assert len(created["methods"]) == 5
    assert created["methods"][1]["value"] == "0591-88886666"

    update_payload = {
        **payload,
        "title": "Senior Engineer",
        "methods": [
            {"method_type": "phone", "label": "Mobile", "value": "01012345678"},
            {"method_type": "email", "label": "Personal", "value": "lin@mail.example"},
        ],
    }
    update_resp = client.put(f"/api/contacts/{contact_id}", json=update_payload)
    assert update_resp.status_code == 200
    updated = update_resp.get_json()["contact"]
    assert updated["title"] == "Senior Engineer"
    assert len(updated["methods"]) == 2
    assert updated["methods"][0]["value"] == "01012345678"

    delete_resp = client.delete(f"/api/contacts/{contact_id}")
    assert delete_resp.status_code == 200
    assert client.get(f"/api/contacts/{contact_id}").status_code == 404


def test_bookmark_toggle_and_filtering(client):
    alice = client.post(
        "/api/contacts",
        json={"name": "Alice", "is_favorite": False, "methods": []},
    ).get_json()["contact"]
    bob = client.post(
        "/api/contacts",
        json={"name": "Bob", "is_favorite": True, "methods": []},
    ).get_json()["contact"]

    # Toggle Alice to bookmarked
    toggle_resp = client.patch(f"/api/contacts/{alice['id']}/favorite", json={})
    assert toggle_resp.status_code == 200
    assert toggle_resp.get_json()["contact"]["is_favorite"] is True

    # Unbookmark Bob explicitly
    unfav_resp = client.patch(
        f"/api/contacts/{bob['id']}/favorite",
        json={"is_favorite": False},
    )
    assert unfav_resp.status_code == 200
    assert unfav_resp.get_json()["contact"]["is_favorite"] is False

    fav_list_resp = client.get("/api/contacts?favorite=1")
    assert fav_list_resp.status_code == 200
    data = fav_list_resp.get_json()
    assert data["total_count"] == 2
    assert data["favorite_count"] == 1
    assert [c["name"] for c in data["contacts"]] == ["Alice"]


def test_validation_and_search(client):
    bad_resp = client.post("/api/contacts", json={"name": "   "})
    assert bad_resp.status_code == 400

    bad_method_resp = client.post(
        "/api/contacts",
        json={
            "name": "Valid Name",
            "methods": [{"method_type": "fax", "value": "123"}],
        },
    )
    assert bad_method_resp.status_code == 400

    client.post(
        "/api/contacts",
        json={
            "name": "Chen Yu",
            "company": "Minjiang Studio",
            "methods": [{"method_type": "social", "label": "GitHub", "value": "@chenyu"}],
        },
    )

    search_resp = client.get("/api/contacts?q=@chenyu")
    assert search_resp.status_code == 200
    results = search_resp.get_json()["contacts"]
    assert len(results) == 1
    assert results[0]["name"] == "Chen Yu"


@pytest.mark.parametrize("query", ["13800138", "cloud lab"])
def test_search_by_partial_phone_or_company(client, query):
    """Match method values and company substrings without returning unrelated rows."""
    for payload in [
        {
            "name": "Review Contact",
            "company": "Fuzhou Cloud Lab",
            "methods": [{"method_type": "phone", "value": "008613800138000"}],
        },
        {"name": "Unrelated Contact", "company": "Design Studio", "methods": []},
    ]:
        assert client.post("/api/contacts", json=payload).status_code == 201

    response = client.get("/api/contacts", query_string={"q": query})
    assert response.status_code == 200
    assert [c["name"] for c in response.get_json()["contacts"]] == ["Review Contact"]


def test_sort_name_ignores_case_and_bookmark_priority(client):
    """Explicit name sorting takes priority over bookmark status and insertion order."""
    for name, favorite in [("Zoe", True), ("bella", False), ("Aaron", False)]:
        response = client.post(
            "/api/contacts", json={"name": name, "is_favorite": favorite}
        )
        assert response.status_code == 201

    response = client.get("/api/contacts?sort=name")
    assert response.status_code == 200
    assert [c["name"] for c in response.get_json()["contacts"]] == ["Aaron", "bella", "Zoe"]


def test_sort_recent_moves_updated_contact_first(client, monkeypatch):
    """Verify timestamp ordering before and after an update without sleeping."""
    timestamps = iter([
        "2026-11-01T10:00:00+00:00",
        "2026-11-01T10:00:01+00:00",
        "2026-11-01T10:00:02+00:00",
        "2026-11-01T10:00:03+00:00",
    ])
    monkeypatch.setattr("address_book.db._utc_now_iso", lambda: next(timestamps))
    contacts = []
    for name in ["Oldest", "Middle", "Newest"]:
        response = client.post("/api/contacts", json={"name": name})
        assert response.status_code == 201
        contacts.append(response.get_json()["contact"])

    response = client.get("/api/contacts?sort=recent")
    assert response.status_code == 200
    assert [c["name"] for c in response.get_json()["contacts"]] == ["Newest", "Middle", "Oldest"]

    response = client.put(
        f"/api/contacts/{contacts[0]['id']}", json={"name": "Oldest Updated"}
    )
    assert response.status_code == 200
    response = client.get("/api/contacts?sort=recent")
    assert response.status_code == 200
    assert [c["name"] for c in response.get_json()["contacts"]] == [
        "Oldest Updated", "Newest", "Middle"
    ]


def test_sort_recent_breaks_equal_timestamp_ties_by_id(client, monkeypatch):
    """Contacts created in one second have a deterministic newest-ID-first order."""
    monkeypatch.setattr(
        "address_book.db._utc_now_iso", lambda: "2026-11-01T10:00:00+00:00"
    )
    contact_ids = []
    for name in ["First", "Second", "Third"]:
        response = client.post("/api/contacts", json={"name": name})
        assert response.status_code == 201
        contact_ids.append(response.get_json()["contact"]["id"])
    response = client.get("/api/contacts?sort=recent")
    assert response.status_code == 200
    assert [c["id"] for c in response.get_json()["contacts"]] == contact_ids[::-1]

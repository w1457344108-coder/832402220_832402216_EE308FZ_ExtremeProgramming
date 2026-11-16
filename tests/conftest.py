"""Shared pytest fixtures for the Address Book application."""

from __future__ import annotations

import pytest

from address_book import create_app


@pytest.fixture()
def app(tmp_path):
    """Create a Flask app configured with an isolated temporary SQLite database."""
    db_file = tmp_path / "test_address_book.db"
    flask_app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(db_file),
        }
    )
    yield flask_app


@pytest.fixture()
def client(app):
    """Return a Flask test client."""
    return app.test_client()

"""Flask application factory for the Address Book web app."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify

from .db import close_db, init_db
from .routes import bp as main_bp


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application instance."""
    root_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(root_dir / "templates"),
        static_folder=str(root_dir / "static"),
    )

    os.makedirs(app.instance_path, exist_ok=True)
    default_db = os.path.join(app.instance_path, "address_book.db")
    app.config.from_mapping(
        DATABASE=os.environ.get("ADDRESS_BOOK_DB", default_db),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10 MB upload cap for Excel files
    )

    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    app.register_blueprint(main_bp)

    @app.errorhandler(413)
    def handle_file_too_large(_err: Exception):
        return jsonify({"error": "Uploaded file exceeds the 10 MB size limit."}), 413

    return app

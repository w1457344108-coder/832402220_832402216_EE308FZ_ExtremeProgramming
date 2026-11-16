# Code Style & Engineering Standards

This document defines the coding, module design, data handling, and Git workflow conventions for the **832402220_832402216_EE308FZ_ExtremeProgramming** repository.

## 1. Python Backend Conventions

- **Style**: Follow PEP 8 (4-space indentation, `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants).
- **Modularity**: Keep database access (`address_book/db.py`), Excel serialization (`address_book/excel_service.py`), and HTTP routing (`address_book/routes.py`) separated by responsibility.
- **Docstrings & Comments**: Every public function and module includes a concise docstring describing purpose and inputs/outputs; inline comments explain non-obvious constraints (such as preserving leading zeros in Excel text cells).
- **Error Handling**: Validate user inputs and uploaded files at API boundaries and return clear JSON error messages with appropriate HTTP status codes (`400`, `404`).

## 2. Frontend Conventions (HTML / CSS / JS)

- **Structure**: Keep markup in `templates/index.html`, styling in `static/css/style.css`, and behavior in `static/js/app.js`.
- **Naming**: Use semantic `kebab-case` CSS classes and `camelCase` JavaScript functions/variables.
- **Security**: Escape dynamic text rendered into HTML to prevent XSS when displaying imported contact names or notes.
- **Feedback**: Surface explicit success/error toast notifications for create, update, delete, bookmark toggle, and Excel import/export actions.

## 3. Data & Excel Handling Rules

- Treat phone numbers, IDs, and social handles as strings (`TEXT` in SQLite and `'@'` text cell format in `openpyxl`) so leading zeros (e.g., `0591-88886666`, `01012345678`) are never stripped.
- Export one contact per row and one information type per column; validate required headers (`Name`) before modifying database rows during import.
- Keep demonstration datasets synthetic.

## 4. Git Commit & Pull Request Conventions

- Use authentic Git identities for each contributor.
- Write concise imperative commit messages with conventional prefixes:
  - `feat:` new functionality
  - `fix:` bug fix
  - `test:` test additions or updates
  - `docs:` documentation updates
  - `style:` UI or formatting adjustments
- Never commit `.db` runtime databases, `__pycache__/`, `.venv/`, or IDE caches.
- Run `pytest -v` before opening or merging a Pull Request, and include verification notes in the PR description.

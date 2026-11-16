# Address Book Web App — EE308FZ Extreme Programming

A lightweight full-stack Address Book application built with **Python Flask**, **SQLite**, **openpyxl**, and modern **HTML/CSS/JavaScript** for the *Software Engineering (FZU–MU)* Extreme Programming assignment.

## Features

- **Bookmark Contacts (1.1)**: Star/unstar important or frequent contacts, persist favorite status in SQLite, and switch between **All Contacts** and **Bookmarked** views with one click.
- **Multiple Contact Methods (1.2)**: Associate multiple phone numbers, email addresses, social media handles, physical addresses, and custom methods (with labels such as `Mobile`, `Work`, `WeChat`, `Home`) with each contact.
- **Excel Import & Export (1.3)**:
  - **Export**: Each contact occupies one row and each category of information occupies a dedicated column (`Name`, `Favorite`, `Company`, `Title`, `Phone Numbers`, `Emails`, `Social Media`, `Addresses`, `Other Contacts`, `Notes`). Phone values are stored as text to preserve leading zeros, and switching to the Bookmarked view switches the export action to export only bookmarked contacts.
  - **Import**: Upload `.xlsx` spreadsheets to batch-import contacts with header validation, configurable duplicate-name handling (`skip` / `update` / `allow`), and row-level feedback. Includes a downloadable template and sample file (`samples/demo_contacts.xlsx`).
- **Contact Management, Themes & Bilingual UI**: Search across names, companies, notes, and contact details; create, edit, and delete contacts; copy contact methods with one click; switch between **Light**, **Dark**, **Ocean Breeze**, and **Warm Paper** themes as well as **English / 中文** interface languages.

## Project Structure

```text
.
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── address_book/
│   ├── __init__.py            # Flask app factory & config
│   ├── db.py                  # SQLite schema & CRUD/bookmark persistence
│   ├── excel_service.py       # Excel export/import & validation logic
│   └── routes.py              # REST API & HTML page routes
├── templates/
│   └── index.html             # Single-page UI template
├── static/
│   ├── css/style.css          # Responsive UI styles
│   └── js/app.js              # Interactive frontend logic
├── samples/
│   └── demo_contacts.xlsx     # Sample Excel file for import testing
├── tests/
│   ├── conftest.py            # Pytest fixtures
│   ├── test_contacts_api.py   # API & persistence tests
│   └── test_excel.py          # Excel round-trip & validation tests
└── docs/
    ├── CODE_STYLE.md          # Team code & Git standards
    └── COLLABORATION.md       # Fork / PR / Release workflow for teammate
```

## Quick Start

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the application

```bash
python3 app.py
```

Open `http://127.0.0.1:5000` in your browser. (You can override the port via `PORT=5050 python3 app.py`.)

### 3. Run automated tests

```bash
pytest -v
```

## Excel Format Specification

Each row represents one contact, and each column represents one information type:

| Column | Required | Format / Example |
| --- | --- | --- |
| `Name` | Yes | `Lin Wei` |
| `Favorite` | No | `Yes` / `No` (also accepts `1`/`0`, `true`/`false`, `是`/`否`) |
| `Company` | No | `Fuzhou Tech` |
| `Title` | No | `Backend Engineer` |
| `Phone Numbers` | No | `Mobile: 13800138000; Work: 0591-88886666` |
| `Emails` | No | `Work: linwei@example.com; Personal: linwei@mail.com` |
| `Social Media` | No | `WeChat: linwei_wx; GitHub: @linwei` |
| `Addresses` | No | `Campus: Fuzhou University Qishan Campus` |
| `Other Contacts` | No | `Website: https://example.com` |
| `Notes` | No | `Project teammate` |

## Documentation & Collaboration

- Code Standards: [docs/CODE_STYLE.md](docs/CODE_STYLE.md)
- Teammate Fork & PR Guide: [docs/COLLABORATION.md](docs/COLLABORATION.md)

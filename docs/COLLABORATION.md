# Teammate Collaboration Guide (Fork, PR & Release)

This repository implements the core Address Book features on `main` and leaves clear, self-contained tasks for teammate (`832402216`) to review, enhance, test, and submit via **Fork + Pull Request** so both members participate in coding and Git collaboration.

## 1. Git Workflow

1. **Fork** `w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming` to your own GitHub account.
2. **Clone** your fork locally and configure your real Git identity:
   ```bash
   git clone https://github.com/<your-username>/832402220_832402216_EE308FZ_ExtremeProgramming.git
   cd 832402220_832402216_EE308FZ_ExtremeProgramming
   git config user.name "<Your Name>"
   git config user.email "<your-github-email>"
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feat/teammate-enhancements
   ```
4. **Install dependencies and verify baseline**:
   ```bash
   pip install -r requirements.txt
   pytest -v
   python3 app.py
   ```
5. **Make your coding/test/documentation contributions**, re-run `pytest -v`, commit with clear messages, and push:
   ```bash
   git push -u origin feat/teammate-enhancements
   ```
6. **Open a Pull Request** from your fork branch to `w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming:main`.
7. After review and merge, tag and publish a GitHub **Release** (e.g. `v1.0.0`).

## 2. Recommended Coding Tasks for Teammate (`832402216`)

Pick one or more of the following self-contained tasks to implement and verify locally:

1. **Edge-case & UI Interaction Tests (`tests/test_contacts_api.py` / `tests/test_excel.py`)**:
   - Add tests for searching by partial phone number / social media handle, sorting favorites first, and importing spreadsheets with Chinese alias headers (`姓名`, `电话`, `邮箱`, `收藏`).
2. **Frontend Usability Polish (`static/js/app.js`, `static/css/style.css`, `templates/index.html`)**:
   - Add a one-click "Copy" button next to phone numbers / email addresses on contact cards, or keyboard shortcut (`/` to focus search, `Esc` to close modals).
3. **Demo Data & Documentation (`samples/`, `README.md`)**:
   - Add additional realistic synthetic test contacts or document verification screenshots and runtime notes.

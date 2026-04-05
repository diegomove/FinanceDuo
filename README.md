# Els Nostres Dobbers - Couple Finance App

A shared finance app for two people (couple, roommates, or friends) to plan monthly budgets, track expenses, compare expected vs actual spending, and calculate who owes whom.

Built with Flask + SQLite, with a mobile-friendly UI and PWA support.

## Features

- Monthly planning: income and expected expenses
- Expense tracking with split modes:
  - 50/50
  - Person 1 only
  - Person 2 only
  - Custom ratio
  - Personal (excluded from shared debt)
- Extra income tracking (refunds, transfers, etc.)
- Shared balance and settlements (payments between people)
- Dashboard with charts (expected vs actual + trends)
- Category management
- Month lifecycle (create, close/reopen, copy fixed expenses)
- PWA install support
- Multi-language UI (Catalan, Spanish, English)

## Tech Stack

- Backend: Python 3.10+ and Flask
- Database: SQLite (local file: finance.db)
- Frontend: Jinja templates + Bootstrap + Chart.js
- PWA: manifest.json + service worker

## Quick Start

### 1) Clone and enter the project

```bash
git clone https://github.com/diegomove/FinanceDuo.git
cd FinanceDuo
```

### 2) Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables (recommended)

```bash
cp .env.example .env
```

Then edit .env with your values.

The app and init_db.py load .env automatically when the file is in the project root (same folder as app.py).

Important variables:

- SECRET_KEY: required for production
- PERSON1_NAME: display name for person 1
- PERSON2_NAME: display name for person 2
- DEFAULT_PASSWORD: initial password used when seeding users
- SESSION_COOKIE_SECURE: set to 1 only when served over HTTPS

### 5) Initialize the database

```bash
python3 init_db.py
```

This creates all tables and seeds default data.

Note: if DEFAULT_PASSWORD is not set, init_db.py generates a random initial password and prints it in the terminal.

### 6) Run the app

```bash
flask --app app run --debug --port 5000
```

Open:

- http://localhost:5000

## First Login

1. Use one of the two seeded users (PERSON1_NAME / PERSON2_NAME).
2. Use the initial password from DEFAULT_PASSWORD (or the one printed by init_db.py).
3. Go to Settings and change the password immediately.

## Typical Monthly Workflow

1. Create a month from the Months screen.
2. Open Budget to set:
   - Income per person
   - Expected expenses by category
3. Add real expenses in Expenses.
4. Check Balance to see who owes whom.
5. Register settlements when payments are made.
6. Review Dashboard and Trends.
7. Close the month when finished.

## Reinitialize the Database

Warning: this deletes all saved data.

```bash
rm -f finance.db
python3 init_db.py
```

## Security and Deployment Notes

- Do not commit local secrets or data files.
  - .env and finance.db are gitignored by default.
- Use a strong SECRET_KEY in production.
- Set SESSION_COOKIE_SECURE=1 only behind HTTPS.
- Do not run with debug enabled in production.
- Prefer running behind a production WSGI server and reverse proxy.

## Deploy As An Online App

You can host this project so both users can access it from phone or desktop like a normal app.

### Option 1: PythonAnywhere (recommended for this stack)

PythonAnywhere is a simple way to host Flask + SQLite apps.

1. Create a PythonAnywhere account.
2. Open a Bash console and clone your repository.
3. Create a virtual environment and install dependencies.

```bash
cd /home/yourusername
git clone https://github.com/diegomove/FinanceDuo.git
cd FinanceDuo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create .env and configure at least:
  - SECRET_KEY
  - PERSON1_NAME
  - PERSON2_NAME
  - SESSION_COOKIE_SECURE=1
5. Initialize the database once:

```bash
python3 init_db.py
```

6. Create a new Flask web app in the PythonAnywhere Web tab.
7. Point the web app to:
  - Source code: /home/yourusername/FinanceDuo
  - Virtualenv: /home/yourusername/FinanceDuo/venv
8. In the WSGI file, load the app object from app.py:

```python
import sys

path = "/home/yourusername/FinanceDuo"
if path not in sys.path:
   sys.path.append(path)

from app import app as application
```

9. Add a static files mapping for /static to /home/yourusername/FinanceDuo/static.
10. Reload the web app.

After that, you can use your PythonAnywhere URL as your shared finance app.

### Option 2: Render / Railway / Fly.io

You can deploy there too, but keep in mind:

- SQLite requires persistent disk/volume.
- If filesystem is ephemeral, your data may be lost on restart.
- Set all environment variables from .env.example in the platform dashboard.
- Run python3 init_db.py once after first deploy.

For production process management, use Gunicorn (install it first) with an entrypoint similar to:

```bash
gunicorn app:app
```

### Option 3: VPS (full control)

Use a VPS with:

- Gunicorn for Flask
- Nginx as reverse proxy
- HTTPS via Let's Encrypt
- systemd service for auto-restart

This option gives maximum control but requires server administration.

## Use It Like An App (PWA)

Once deployed with HTTPS, users can install it like an app:

1. Open the site in Chrome, Edge, or Safari.
2. Choose Install App or Add To Home Screen.
3. Launch it from the device home screen/app launcher.

The project already includes manifest and service worker support for this.

## Project Structure

```text
app.py
config.py
init_db.py
schema.sql
requirements.txt
translations.py
models/
routes/
static/
templates/
```

## Troubleshooting

- ModuleNotFoundError: No module named flask
  - Activate your virtual environment and run pip install -r requirements.txt.

- I cannot submit forms (400/403)
  - Ensure you are using the app from the same origin (host/port) and that your browser allows cookies.

- My .env changes are not applied when running init_db.py
  - Make sure .env is in the project root and run commands from that same folder.
  - If you changed PERSON1_NAME or PERSON2_NAME after creating finance.db, recreate the DB:
    - rm -f finance.db
    - python3 init_db.py

- Styles/scripts seem stale after updates
  - Hard refresh the browser or clear site data/service worker cache.

## Contributing

1. Create a branch
2. Make your changes
3. Test locally
4. Open a Pull Request with a clear description

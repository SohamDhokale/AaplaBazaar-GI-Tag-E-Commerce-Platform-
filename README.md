# AaplaBazaar Market

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Project-Active-blue)

AaplaBazaar is a modern, multilingual e‑commerce platform focused on authentic Indian products. It provides user accounts, product browsing and search, cart and wishlist management, secure checkout (COD and UPI), order tracking with SMS notifications, and an admin interface for managing products and orders.

## Features

- User registration, login, profile and address management
- Product catalog, categories, search and sorting
- Shopping cart with quantity updates and totals
- Wishlist with authenticated access
- Checkout with UPI QR and Cash on Delivery
- Order tracking and SMS notifications via Twilio
- Multilingual UI (English, Hindi, Marathi) using Flask‑Babel
- Admin dashboard to manage products and orders
- Responsive frontend (Bootstrap, Font Awesome, Swiper)

## Tech Stack

- Backend: `Flask`, `Flask‑Login`, `Flask‑WTF`, `Flask‑SQLAlchemy`
- Frontend: `HTML`, `CSS (Bootstrap)`, `JavaScript`
- Database: SQLite by default; PostgreSQL supported via `psycopg2`
- Internationalization: `Flask‑Babel`
- Notifications: `Twilio`
- Optional payments: `Stripe` SDK present for future use; UPI/COD currently enabled

## Project Structure

```
├── app.py               # App factory, config, Babel, DB init
├── models.py            # SQLAlchemy models
├── forms.py             # WTForms forms
├── routes.py            # Flask routes (store + admin)
├── translations.py      # i18n strings
├── utils.py             # Twilio SMS + helpers
├── templates/           # Jinja templates (store + admin)
├── static/              # CSS/JS assets
├── instance/aaplabazaar.db  # SQLite database (optional)
├── pyproject.toml       # Python dependencies
└── README.md
```

## Installation

Prerequisites:
- `Python 3.11+`
- Optional: `PostgreSQL` (if using `DATABASE_URL`)
- Optional: Twilio account (for SMS notifications)

Steps (Windows PowerShell):
1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `./.venv/Scripts/Activate.ps1`
2. Install dependencies from `pyproject.toml`:
   - `pip install .`
   - If you prefer, install directly: `pip install flask flask-login flask-wtf flask-sqlalchemy flask-babel email-validator psycopg2-binary sqlalchemy twilio stripe werkzeug wtforms trafilatura`

## Configuration

Set environment variables to configure the application. Sensible defaults are applied when not provided.

- `SESSION_SECRET` (required in production): Secret key for sessions. Default: `aaplabazaar_secret_key`.
- `DATABASE_URL` (optional): SQLAlchemy DB URI. Default: `sqlite:///aaplabazaar.db`.
  - Example (PostgreSQL): `postgresql+psycopg2://user:password@localhost:5432/aaplabazaar`
- `TWILIO_ACCOUNT_SID` (optional): Twilio Account SID for SMS.
- `TWILIO_AUTH_TOKEN` (optional): Twilio Auth Token for SMS.
- `TWILIO_PHONE_NUMBER` (optional): Twilio phone number used to send messages.
- `BABEL_DEFAULT_LOCALE` (optional): Default UI language. Default: `en`.
- `BABEL_SUPPORTED_LOCALES` (optional): Supported languages. Default: `["en", "hi", "mr"]`.
- `UPI_VPA` (optional, set via `app.config`): Default UPI VPA shown in checkout.
- `UPI_PAYEE_NAME` (optional, set via `app.config`): Payee name for UPI checkout.

PowerShell examples:
- `$env:SESSION_SECRET = "change_me_production_secret"`
- `$env:DATABASE_URL = "sqlite:///aaplabazaar.db"`
- `$env:TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
- `$env:TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
- `$env:TWILIO_PHONE_NUMBER = "+1XXXXXXXXXX"`

Note: If Twilio vars are missing, SMS sending is skipped gracefully (logged only).

## Usage

Local development:
- Set Flask environment and run:
  - `$env:FLASK_APP = "app.py"`
  - `$env:FLASK_ENV = "development"`
  - `flask run`
- Open `http://localhost:5000`

Examples:
- Switch language: `http://localhost:5000/?lang=hi` or `?lang=mr`
- Browse products with search: `http://localhost:5000/products?search=spices&sort=price_low`
- Admin dashboard: `http://localhost:5000/admin` (requires a user with `is_admin=True` in DB)

Production (Linux/macOS example):
- `gunicorn -w 4 -b 0.0.0.0:8000 "app:app"`

## Contribution Guidelines

- Fork the repo and create a feature branch (e.g., `feature/upi-qr`)
- Follow PEP8 and project conventions; keep changes focused and minimal
- Write clear commit messages and update documentation when needed
- Test locally (`flask run`) before opening a Pull Request
- Open a PR with a concise description, screenshots for UI changes, and notes on config/env impacts

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it. See the MIT badge above for summary, and include proper attribution when redistributing.

## Badges & Status

- Build/CI: Configure your preferred CI to add status badges
- Coverage: Add coverage badge when tests are available
- Internationalization: English, Hindi, Marathi via `Flask‑Babel`

## Support & Contact

- Issues: Please open a GitHub issue describing the problem or feature request
- Contact: maintainer@example.com (replace with your preferred contact)
- SMS Notifications: Twilio trial accounts can only send to verified numbers; see Twilio console for verification

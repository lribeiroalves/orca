# ORCA

Web application for personal financial management with tracking of income, expenses, balances, invoices, and installment purchases.

## Overview

ORCA is a Flask-based system with a modular architecture using SQLAlchemy, Flask-Migrate, Dynaconf, and Flask-Admin.

### Core features
- user registration;
- income and expense tracking;
- monthly and bank-based balance management;
- invoice and installment purchase control;
- admin panel at `/admin`;
- charts and period-based reports;
- SQLite for local development and Docker for deployment.

## Project structure

```text
orca/
├── app/
│   ├── blueprint/
│   ├── ext/
│   ├── seeders/
│   ├── static/
│   └── templates/
├── config/
│   └── settings.toml
├── instance/
├── migrations/
├── .github/workflows/deploy.yml
├── .env.example
├── .gitignore
├── Makefile
├── dockerfile
├── requirements.in
├── requirements.txt
├── README.md
├── README-PT-BR-compact.md
├── README-EN.md
└── app.py
```

## Requirements

- Python 3.11+
- pip
- virtualenv
- Git
- Docker (optional for deployment)

## Local setup

### 1) Clone the repository

```bash
git clone <repository-url>
cd orca
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

Or use:

```bash
make requirements
```

### 3) Configure the `.env`

Create a file named `.env` at the project root:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=replace-with-a-strong-secret
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////absolute/path/to/orca/instance/database.db
```

Example:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=local-secret-key
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////home/your-user/orca/instance/database.db
```

```bash
mkdir -p instance
```

## Run locally

```bash
make run
```

The app will be available at:

```text
http://127.0.0.1:5000
```

## Migrations

The project uses Flask-Migrate/Alembic and applies migrations automatically on app startup.

```bash
flask --app app db migrate -m "message"
flask --app app db upgrade
```

## Seeders

To populate the database in development mode:

```bash
flask --app app populate-development
```

## Automatic deployment

The pipeline in [/.github/workflows/deploy.yml](.github/workflows/deploy.yml) does the following:

1. builds the Docker image;
2. pushes it to Docker Hub;
3. connects to the remote server via SSH;
4. pulls the latest image and updates the container with `docker compose up -d`.

Expected GitHub secrets:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SSH_HOST`
- `SSH_USER`
- `SSH_KEY`
- `SSH_PORT`

## Makefile

Available shortcuts:

```bash
make venv
make requirements
make run
make clear-cache
```

## Notes

- use SQLite for local development and testing;
- keep `.env` out of version control;
- keep `requirements.in` as the source of dependencies;
- regenerate `requirements.txt` with `pip-compile` whenever dependencies change.

---

## References

- [README.md](README.md)
- [README-PT-BR-compact.md](README-PT-BR-compact.md)

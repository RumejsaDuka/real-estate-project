# Real Estate Project

A Django real estate website with a PostgreSQL database backend.

## Requirements

- Python 3.13 or newer
- PostgreSQL
- A PostgreSQL database named `real_estate`

The database connection is configured in `config/settings.py`. Make sure PostgreSQL is running and that your local database settings match your machine.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Apply database migrations:

```powershell
python manage.py migrate
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

Run the development server:

```powershell
python manage.py runserver
```

Then open:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Useful Commands

Check the project:

```powershell
python manage.py check
```

Create migrations after model changes:

```powershell
python manage.py makemigrations
python manage.py migrate
```

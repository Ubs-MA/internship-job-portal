# Internship & Job Portal

A complete Django-based web application for students and companies.

## Features
- User registration with Student/Company roles
- Companies can post jobs and internships
- Students can browse, view details, and apply
- CV upload and profile management
- Separate dashboards for students and companies
- View applicants and download CVs
- Optional contact email

## Tech Stack
- Django
- SQLite (development)
- HTML templates (simple & clean)

## Setup
```bash
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

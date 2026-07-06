# SportSlot 🏟️

Sports venue booking platform for Almaty. Users can browse sports venues,
check details and reviews, book time slots, and manage their bookings.

**KBTU — Web Development Final Project (Django Templates + Django REST Framework)**

## Group Members

- Boris Nurdaulet
- Kudaikul Aruzhan
- Kapsikh Aibyn

## Features

- Browse sports venues with filtering by sport type (football, basketball, tennis, etc.)
- Venue detail pages with description, price, and user reviews
- Book a venue for a specific date and time (with slot availability check)
- Manage personal bookings: view, update, cancel
- Add venues to favorites
- User registration, login, and logout
- REST API with token-based authentication (Django REST Framework)

## Tech Stack

- **Backend:** Django, Django REST Framework, django-cors-headers
- **Frontend:** Django Templates, HTML/CSS
- **Database:** SQLite
- **Auth:** Django session auth (frontend) + DRF token auth (API)

## Setup

```bash
git clone https://github.com/NurdauletBoris/SportSlot.git
cd SportSlot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

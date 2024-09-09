#!/usr/bin/env bash
rm -fr faroldesantamartaapp/__pycache__
rm -fr faroldesantamartaapp/migrations/__pycache__
rm -f faroldesantamartaapp/migrations/0001_initial.py
rm -fr faroldesantamartaapp/tests/__pycache__
rm -fr faroldesantamartaproject/__pycache__
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata roles
python manage.py loaddata users
python manage.py loaddata statuses
python manage.py loaddata courses
python manage.py loaddata feedbacks
python manage.py loaddata events
python manage.py loaddata products


@echo off
del /q /s /f /a *.pyc
del /q /s /f /a *.pyo
del /q /s /f /a *.pyd
del /q /s /f /a *.pyw
del /q /s /f /a *.pyz
del /q /s /f /a sqlite3.db
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
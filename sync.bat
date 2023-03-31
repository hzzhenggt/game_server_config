@echo off
chcp 65001
python manage.py makemigrations
python manage.py migrate
@REM python manage.py collectstatic --noinput
pause
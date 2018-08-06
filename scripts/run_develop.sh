#!/bin/bash -x

crontab /code/cronjobs
service cron start

. /venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate --no-input
python3 manage.py createinitialrevisions
python3 manage.py runserver 0.0.0.0:8000

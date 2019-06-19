#!/bin/bash -x

export PYTHONUNBUFFERED=1
crontab /code/cronjobs
crond -L /tmp/cron.logs

pip3 install -r requirements.txt
python3 manage.py migrate --no-input
python3 manage.py createinitialrevisions
python3 manage.py runserver 0.0.0.0:8000

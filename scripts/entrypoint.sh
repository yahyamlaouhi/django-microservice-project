#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py wait_for_db
python manage.py migrate


python manage.py populate_hotels --customer_number 10 --staff_number 10 --hotel_owner_number 20 --hotel_number 10 --room_number 40 --meals_number 10

# delete all migrations file
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -d
# sudo docker rm dbfarkitohotel

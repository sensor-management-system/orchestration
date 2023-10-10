#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

set -e

cd /usr/cv/app

apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py loaddata default_community_data.json
python manage.py loaddata hydro_community_data.json
python manage.py collectstatic --noinput
exec gunicorn cv.wsgi:application --bind 0:8000 --reload --log-level debug --timeout 50

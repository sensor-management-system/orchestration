#!/bin/bash

# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

set -e

apt-get update
apt-get install -y  --no-install-recommends \
  gcc \
  libssl-dev \
  libffi-dev \
  musl-dev \
  cargo \
  g++
apt-get clean
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

# execute the database migrations at startup
python manage.py db upgrade

# create and load TSM endpoint fixture
if [ ! -z ${TSM_ENDPOINTS+x} ]; then
    echo $TSM_ENDPOINTS > /tmp/tsm_endpoint_fixture.json
    python manage.py loaddata /tmp/tsm_endpoint_fixture.json --skip-empty-file
fi

# trigger the reindex of es
while ! python3 manage.py es reindex
do
    sleep 10
done

exec gunicorn -b 0.0.0.0:5000 manage:app --reload --log-level debug --timeout 50

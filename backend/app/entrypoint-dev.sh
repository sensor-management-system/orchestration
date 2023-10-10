#!/bin/bash

# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
python manage.py db upgrade
python -c 'import os; print(os.getenv("TSM_ENDPOINTS"))' > /tmp/tsm_endpoint_fixture.json
python manage.py loaddata /tmp/tsm_endpoint_fixture.json --skip-empty-file

while ! python3 manage.py es reindex
do
    sleep 10
done
exec gunicorn -b 0.0.0.0:5000 manage:app --reload --log-level debug --timeout 50

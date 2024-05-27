#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


echo "[LOG] Using database: $1"
echo "[LOG] Running migrations"
python manage.py db upgrade
echo "[LOG] Insert fixtures"
python -c 'import os; print(os.getenv("TSM_ENDPOINTS"))' > /tmp/tsm_endpoint_fixture.json
python manage.py loaddata /tmp/tsm_endpoint_fixture.json
echo "[LOG] Starting gunicorn on port $2"
gunicorn -b 0.0.0.0:5000 manage:app --reload

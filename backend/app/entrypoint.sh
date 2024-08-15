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

if ! [ -x "$(command -v nproc)" ]; then
    CPUS=2
else
    CPUS=$(nproc)
fi
WORKERS=$(( 2 * $CPUS + 1 ))

# execute the database migrations at startup
python3 manage.py db upgrade

# create and load TSM endpoint fixture
if [ ! -z ${TSM_ENDPOINTS} ]; then
    echo $TSM_ENDPOINTS > /tmp/tsm_endpoint_fixture.json
    python3 manage.py loaddata /tmp/tsm_endpoint_fixture.json
fi

# trigger the reindex of es
while ! python3 manage.py es reindex
do
    sleep 10
done

exec gunicorn --access-logfile - --workers=$WORKERS --bind 0.0.0.0:5000 manage:app

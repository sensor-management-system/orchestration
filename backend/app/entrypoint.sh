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

pip install --no-cache-dir -r requirements.txt

if ! [ -x "$(command -v nproc)" ]; then
    CPUS=2
else
    CPUS=$(nproc)
fi
WORKERS=$(( 2 * $CPUS + 1 ))

exec gunicorn --access-logfile - --workers=$WORKERS --bind 0.0.0.0:5000 manage:app


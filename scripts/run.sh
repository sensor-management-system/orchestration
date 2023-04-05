#!/bin/sh

# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


echo "[LOG] Using database: $1"
echo "[LOG] Running migrations"
python manage.py db upgrade
echo "[LOG] Starting gunicorn on port $2"
gunicorn -b 0.0.0.0:5000 manage:app --reload
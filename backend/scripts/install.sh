#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


# Install essential packages from Apt
apt-get update -y
apt-get install -y  --no-install-recommends gcc libssl-dev libffi-dev musl-dev cargo curl python3-distutils g++

apt-get clean

pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo ""
echo "Successfully installed the requirements."
echo ""

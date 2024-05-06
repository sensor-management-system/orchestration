#!/bin/bash

# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

# Script to check the validation of the openapi specs.
# 1) Download the file from the running server
# 2) Format it (for easier debugging)
# 3) Run the openapi validation

set -e
url="https://localhost/backend/api/v1/openapi.json"
path="./openapi.json"

# Download it
curl $url -s -k > $path

jq . $path > ${path}.formatted
mv ${path}.formatted ${path}

# Run the check
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli:v7.5.0 \
       docker-entrypoint.sh validate \
       -i /local/openapi.json

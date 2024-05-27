#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2023 - 2024
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Be aware of the port of the db
docker-compose -f "${DIR_SCRIPT}/docker-compose.yml" exec -u $UID db bash -c "psql db_dev postgres -p 5433 < /mnt/sql/preset-development-and-test-data.sql"

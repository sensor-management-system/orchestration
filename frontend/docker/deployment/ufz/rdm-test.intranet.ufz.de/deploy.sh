#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2020 - 2024
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

cd "$(dirname "$0")"
docker-compose pull && docker-compose up -d

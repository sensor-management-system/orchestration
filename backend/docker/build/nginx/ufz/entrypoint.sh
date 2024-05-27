#!/bin/sh

# SPDX-FileCopyrightText: 2022 - 2024
# - Hannes Bohring <hannes.bohring@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

# run entrypoint script from master image
sh /docker-entrypoint.sh "$@"

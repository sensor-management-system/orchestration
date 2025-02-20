# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM postgres:15-alpine

COPY mq/db/mqtt_auth.sql /docker-entrypoint-initdb.d/10_mqtt_auth.sql
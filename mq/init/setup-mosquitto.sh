#!/bin/bash

# SPDX-FileCopyrightText: 2024
# - Joost Hemmen <joost.hemmen@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

set -e
apk update
apk add --no-cache gettext postgresql-client
pip install --upgrade pip --quiet --root-user-action=ignore
pip install psycopg --quiet --root-user-action=ignore

# Fill environment variables into mosquitto.conf

envsubst < "/etc/mq_init/mosquitto.dev.template" > /etc/mosquitto/mosquitto.conf

if [ "$MQTT_TLS" = "true" ]; then
    envsubst < "/etc/mq_init/mosquitto.tls.template" >> /etc/mosquitto/mosquitto.conf
fi
echo "Created mosquitto.conf"

# Create mqtt-backend-user in mq_db
MQTT_BACKEND_PASSWORD_HASH=$(/etc/mq_init/pbkdf2_hash.py ${MQTT_BACKEND_PASSWORD})
PGPASSWORD=${MQ_PG_PASSWORD} psql -v ON_ERROR_STOP=1 -h "$MQ_PG_HOST" -p "$MQ_PG_PORT" --username "$MQ_PG_USER" --dbname "$MQ_PG_DB" <<-EOSQL
    INSERT INTO mqtt_user (username, password_hash, is_active, is_admin)
    VALUES ('$MQTT_BACKEND_USER', '$MQTT_BACKEND_PASSWORD_HASH', true, true)
    ON CONFLICT (username) DO UPDATE
    SET password_hash = EXCLUDED.password_hash,
        is_active = EXCLUDED.is_active,
        is_admin = EXCLUDED.is_admin;
EOSQL

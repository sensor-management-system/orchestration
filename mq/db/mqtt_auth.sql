-- SPDX-FileCopyrightText: 2024
-- - Joost Hemmen <joost.hemmen@ufz.de>
-- - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
--
-- SPDX-License-Identifier: EUPL-1.2
CREATE TABLE IF NOT EXISTS mqtt_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS mqtt_user_acl (
    id SERIAL PRIMARY KEY,
    mqtt_user_id INTEGER NOT NULL REFERENCES mqtt_user(id),
    topic VARCHAR(255) NOT NULL,
    rw INTEGER NOT NULL
);

ALTER TABLE mqtt_user_acl ADD FOREIGN KEY (mqtt_user_id) REFERENCES mqtt_user(id);

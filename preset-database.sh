#!/usr/bin/env bash
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Be aware of the port of the db
docker-compose -f "${DIR_SCRIPT}/docker-compose.yml" exec -u $UID db bash -c "psql db_dev postgres -p 5433 < /mnt/sql/preset-development-and-test-data.sql"
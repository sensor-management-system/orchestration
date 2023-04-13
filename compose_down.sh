#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


SESSION="SMS_Development"

# set up tmux
tmux start-server

tmux kill-session -t $SESSION

DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="${DIR_SCRIPT}/docker/env.dev"

2>/dev/null 1>/dev/null docker exec sms_web whoami
DOCKER_COMPOSE_IS_DOWN=$?
if [ "$DOCKER_COMPOSE_IS_DOWN" != "1" ] ; then
    echo "docker-compose services still running!"
    echo "I'll stop them for you ..."

    docker-compose  -f "${DIR_SCRIPT}/docker-compose.yml" --env-file "$ENV_FILE" down  --remove-orphans

    echo "... finished."
fi

echo "docker-compose services are down."

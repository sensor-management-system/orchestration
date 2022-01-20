#!/usr/bin/env bash

SESSION="SMS_Development"

# set up tmux
tmux start-server

tmux kill-session -t $SESSION


2>/dev/null 1>/dev/null docker exec sms_web whoami
DOCKER_COMPOSE_IS_DOWN=$?
if [ "$DOCKER_COMPOSE_IS_DOWN" != "1" ] ; then
    echo "docker-compose services still running!"
    echo "I'll stop them for you ..."

    docker-compose --env-file docker/env.dev down  --remove-orphans

    echo "... finished."
fi

echo "docker-compose services are down."

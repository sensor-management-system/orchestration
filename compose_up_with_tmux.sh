#!/usr/bin/env bash

SESSION="SMS_Development"

# set up tmux
tmux start-server

# check if session is up
tmux has-session -t $SESSION 2>/dev/null
SESSION_NOT_FOUND=$?
if [ "$SESSION_NOT_FOUND" != "0" ] ; then
  # create a new tmux session
  tmux new-session -d -s $SESSION -n logs-watcher
  else tmux attach-session -t $SESSION
fi

DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

2>/dev/null 1>/dev/null docker-compose  -f "${DIR_SCRIPT}/docker-compose.yml" --env-file docker/env.dev exec nginx whoami
DOCKER_COMPOSE_IS_NOT_RUNNING=$?

if [ "$DOCKER_COMPOSE_IS_NOT_RUNNING" != "0" ] ; then
    echo "docker-compose services are not running!"
    echo "I'll start them for you ..."

    docker-compose -f "${DIR_SCRIPT}/docker-compose.yml" --env-file docker/env.dev  up -d

    while [ "$DOCKER_COMPOSE_IS_NOT_RUNNING" != "0" ] ; do
        sleep 2
        echo "..."
        2>/dev/null 1>/dev/null docker-compose -f "${DIR_SCRIPT}/docker-compose.yml" --env-file docker/env.dev exec nginx whoami
        DOCKER_COMPOSE_IS_NOT_RUNNING=$?
    done
    sleep 1
    echo "... finished."
fi

## split window
tmux split-window -h
tmux split-window -v
tmux split-window -v

tmux selectp -t 1
tmux splitw -v
tmux selectp -t 2
tmux splitw -v
tmux selectp -t 3
tmux splitw -v
tmux selectp -t 4
tmux splitw -v

#

tmux selectp -t 0  -T dev
tmux selectp -t 1  -T sms_backend
tmux selectp -t 2  -T sms_cv
tmux selectp -t 3  -T sms_web
tmux selectp -t 4  -T sms_db
tmux selectp -t 5  -T sms_minio
tmux selectp -t 6  -T sms_frontend

# logs monitoring
tmux selectp -t 1
tmux send-keys "docker logs sms_backend  -f" C-m

tmux selectp -t 6
tmux send-keys "docker logs sms_frontend -f" C-m

tmux selectp -t 2
tmux send-keys "docker logs sms_cv -f" C-m

tmux selectp -t 3
tmux send-keys "docker logs sms_web -f" C-m

tmux selectp -t 4
tmux send-keys "docker logs sms_db -f" C-m

tmux selectp -t 5
tmux send-keys "docker logs sms_minio -f" C-m

tmux set -g pane-border-status bottom

tmux selectp -t 0


tmux select-window -t $SESSION:0

# Finished setup, attach to the tmux session!
tmux attach-session -t $SESSION


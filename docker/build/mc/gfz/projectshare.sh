#!/bin/sh

# This is the script to copy the content from one folder
# to another and make some cleanup.
# This runs in a docker container in order to run with the
# user and group ids of the project share technical account.

for SERVICE in backend-db vocabulary-db minio
do

    # We must make sure that our target folder exists.
    mkdir -p /mnt/sms-backup/${SERVICE}
    # Then we run a little cleanup for target folder
    # (remove files older then cleanup days).
    find /mnt/sms-backup/${SERVICE} -type f -mtime +${CLEANUP:-180} -exec rm {} \;
    # We want to know what our latest file is.
    LATEST_DUMP=$(ls -Art /srv/docker/service/${SERVICE}/backups | tail -n 1)
    # And then we copy it over to our target folder.
    cp -r /srv/docker/service/${SERVICE}/backups/${LATEST_DUMP} /mnt/sms-backup/${SERVICE}/${LATEST_DUMP}
done

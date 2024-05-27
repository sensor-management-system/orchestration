#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


# This is the script to copy the content from one folder
# to another and make some cleanup.
# This runs in a docker container in order to run with the
# user and group ids of the project share technical account.

for SERVICE in backend-db vocabulary-db idl-db minio
do

    # We must make sure that our target folder exists.
    mkdir -p /mnt/sms-backup/${SERVICE}
    if [ $? -ne 0 ]
    then
        echo "Could not create the folder /mnt/sms-backup/${SERVICE}"
        echo "Abandon..."
        exit 1
    fi
    # Then we run a little cleanup for target folder
    # (remove files older then cleanup days).
    find /mnt/sms-backup/${SERVICE} -type f -mtime +${CLEANUP:-180} -exec rm {} \;
    # We want to know what our latest file is.
    LATEST_DUMP=$(ls -Art /srv/docker/service/${SERVICE}/backups | tail -n 1)
    # Now we check if we have enough space left on the project share.
    SIZE_LATEST_DUMP=$(du -Pk /srv/docker/service/${SERVICE}/backups/${LATEST_DUMP} | awk '{print $1}')
    CURRENT_SPACE_ON_TARGET=$(df -Pk /mnt/sms-backup | awk '/[0-9]%/{print $(NF-2)}')
    if [ $CURRENT_SPACE_ON_TARGET -lt $SIZE_LATEST_DUMP ]
    then
        echo "Not enough space left on the project share to store the backup there"
        echo "Abandon..."
        exit 1
    fi
    # And then we copy it over to our target folder.
    cp -r /srv/docker/service/${SERVICE}/backups/${LATEST_DUMP} /mnt/sms-backup/${SERVICE}/${LATEST_DUMP}
    if [ $? -ne 0 ]
    then
        echo "Could not copy the file /srv/docker/service/${SERVICE}/backups/${LATEST_DUMP} to /mnt/sms-backup/${SERVICE}"
        echo "Abandon..."
        exit 1
    fi
done

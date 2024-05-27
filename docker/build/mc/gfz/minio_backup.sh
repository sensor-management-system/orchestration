#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


# This is a script to make backups of the minio server from within the gitlab CI.
# We need to mount the target folder under /backups
# And we need to provide the user and group id of the user that should be able
# to handle our backup later.

# First we have to create the alias for an easier access.
/usr/bin/mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} --api S3v4

# We use 2 folders here. One as a working directory for the backups
# which is /backup-creation
mkdir -p /backup-creation/files
# And the other one is /backup which is a mount into the running container.
# It is used to store the backend afterwards

/usr/bin/mc mirror --preserve minio/${MINIO_BUCKET_NAME} /backup-creation/files
/usr/bin/mc stat --recursive minio/${MINIO_BUCKET_NAME} > /backup-creation/metadata.txt

tar zcvf /backups/minio_backup.tar.gz /backup-creation


# Now we are done with the backup itself - but as we run it in a docker-container
# and mount our backup folder under /backups, we also want the normal user to
# be able to edit / remove the files afterwards.
# In the mc docker image we only have the root user. So we can easily add a new
# one with the GROUP_ID and USER_ID variables
# We can easliy add a new one (but we also need to check existing ones)

# the getent will return a colon seperated one line list of entries
# the name is the first one (or it returns nothing at all)
GROUPNAME=$(getent group ${GROUP_ID:-1000} | awk -F ':' '{print $1}')
if [ -z $GROUPNAME ]
then
    GROUPNAME=backupgroup
    groupadd -g ${GROUP_ID:-1000} ${GROUPNAME}
fi
USERNAME=$(getent passwd ${USER_ID:-1000} | awk -F ':' '{print $1}')
if [ -z $USERNAME ]
then
    USERNAME=backupuser
    useradd -u ${USER_ID:-1000} ${USERNAME}
fi

chown --recursive ${USERNAME}:${GROUPNAME} /backups

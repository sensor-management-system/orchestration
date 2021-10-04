#!/bin/sh

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
# We can easliy add a new one

groupadd -g ${GROUP_ID:-1000} backupgroup
useradd -u ${USER_ID:-1000} backupuser

chown --recursive backupuser:backupgroup /backups

# Now we are done - and another process can care about the bundling and compressing
# the files (no tar in the mc image).

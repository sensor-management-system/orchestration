#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0


# Wait until the minio server is online
until curl -f http://minio:9000/minio/health/live
do
    sleep 5
done

/usr/bin/mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} --api S3v4

/usr/bin/mc mb --quiet minio/${MINIO_BUCKET_NAME}
/usr/bin/mc anonymous set download minio/${MINIO_BUCKET_NAME}
exit 0

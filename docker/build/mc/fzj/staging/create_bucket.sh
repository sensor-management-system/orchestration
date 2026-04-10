#!/bin/sh

# SPDX-FileCopyrightText: 2021 - 2026
# - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3, https://www.fz-juelich.de/en/ibg/ibg-3)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


echo "Waiting for MinIO to start..."
until curl -f http://minio:9000/minio/health/live
do
  sleep 5
done

echo "MinIO is ready! Configuring root alias..."
/usr/bin/mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} --api S3v4

echo "Creating FZJ bucket..."
/usr/bin/mc mb --quiet --ignore-existing minio/${MINIO_BUCKET_NAME}

echo "Setting anonymous download policy for FZJ..."
/usr/bin/mc anonymous set download minio/${MINIO_BUCKET_NAME}

echo "FZJ bucket initialization complete!"
exit 0


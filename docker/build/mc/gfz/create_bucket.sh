#!/bin/sh

# Wait until the minio server is online
until curl -f http://minio:9000/minio/health/live
do
    sleep 5
done

/usr/bin/mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} --api S3v4

/usr/bin/mc mb --quiet minio/${MINIO_BUCKET_NAME}
/usr/bin/mc anonymous set download minio/${MINIO_BUCKET_NAME}
exit 0

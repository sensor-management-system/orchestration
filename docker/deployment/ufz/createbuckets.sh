#!/usr/bin/env sh

while ! nc -z minio 9000; do echo 'Wait minio to startup...' && sleep 0.1; done;
sleep 5

mc config host add myminio http://minio:9000 \$MINIO_ACCESS_KEY \$MINIO_SECRET_KEY

mc mb myminio/\$MINIO_BUCKET_NAME
mc policy download myminio/\$MINIO_BUCKET_NAME

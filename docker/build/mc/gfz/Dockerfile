FROM minio/mc:latest

RUN \
    microdnf update --nodocs && \
    microdnf install tar gzip && \
    microdnf clean all

COPY ./minio_backup.sh /backup.sh
RUN chmod +x /backup.sh

COPY ./create_bucket.sh /create_bucket.sh
RUN chmod +x /create_bucket.sh

ENTRYPOINT ["/bin/sh", "-c"]
# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM minio/mc:RELEASE.2023-02-16T19-20-11Z

RUN \
    microdnf update --nodocs && \
    microdnf install tar gzip findutils python3 && \
    microdnf clean all && \
    pip3 install requests boto3==1.23.10

COPY ./minio_backup.py /backup.py
RUN chmod +x /backup.py

COPY ./create_bucket.sh /create_bucket.sh
RUN chmod +x /create_bucket.sh

COPY ./projectshare.sh /projectshare.sh
RUN chmod +x /projectshare.sh

ENTRYPOINT ["/bin/sh", "-c"]
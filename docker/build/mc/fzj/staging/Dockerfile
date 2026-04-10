# SPDX-FileCopyrightText: 2021 - 2026
# - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3, https://www.fz-juelich.de/en/ibg/ibg-3)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM minio/mc:RELEASE.2023-02-16T19-20-11Z

# Install dependencies
RUN microdnf update --nodocs && \
    microdnf install -y tar gzip findutils python3 && \
    microdnf clean all && \
    pip3 install --no-cache-dir requests boto3==1.23.10

# Copy the script and make it executable
COPY ./create_bucket.sh /create_bucket.sh
RUN chmod +x /create_bucket.sh

# Start the script automatically
ENTRYPOINT ["/create_bucket.sh"]
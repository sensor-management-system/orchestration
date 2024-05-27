# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM python:3.9-slim-buster

RUN apt-get update && apt-get -y install openssl

RUN pip install --upgrade pip --no-cache-dir

RUN pip install zeroc-icecertutils

WORKDIR /icessl

ADD ice-ca-certs.py .

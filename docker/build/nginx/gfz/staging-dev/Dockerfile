# SPDX-FileCopyrightText: 2021-2023
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0


FROM nginx:alpine as webserver
# HTTPS for application, backend, cv and minio
EXPOSE 3000
# HTTP for Backend and CV
EXPOSE 3001
# Minio console
EXPOSE 3002

COPY dist/latest /usr/share/nginx/html/latest
COPY dist/manual /usr/share/nginx/html/manual
COPY ./docker/build/nginx/gfz/staging-dev/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/build/nginx/gfz/staging-dev/default.conf /etc/nginx/conf.d/default.conf

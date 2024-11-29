# SPDX-FileCopyrightText: 2020 - 2024
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM node:20.17.0-bullseye AS js-builder

ARG SMS_VERSION_ARG=develop
ENV SMS_VERSION=$SMS_VERSION_ARG

RUN mkdir /smsfrontend
COPY ./frontend /smsfrontend
WORKDIR /smsfrontend

# set version in package.json
RUN sed -i 's/"version": ".*"/"version": "'"$SMS_VERSION"'"/' package.json

RUN npm ci
RUN npm run build

FROM nginx:1.27.3-alpine AS webserver

COPY --from=js-builder /smsfrontend/dist/ /usr/share/nginx/html

COPY ./frontend/docker/generic-image/default.conf /etc/nginx/conf.d/default.conf

COPY ./frontend/docker/generic-image/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

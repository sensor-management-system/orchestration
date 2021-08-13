# Web client of the Sensor Management System software developed within
# the Helmholtz DataHub Initiative by GFZ and UFZ.
#
# Copyright (C) 2020
# - Martin Abbrent (UFZ, martin.abbrent@ufz.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ
#   (UFZ, https://www.ufz.de)
#
# Parts of this program were developed within the context of the
# following publicly funded projects or measures:
# - Helmholtz Earth and Environment DataHub
#   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
#
# Licensed under the HEESIL, Version 1.0 or - as soon they will be
# approved by the "Community" - subsequent versions of the HEESIL
# (the "Licence").
#
# You may not use this work except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://gitext.gfz-potsdam.de/software/heesil
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the Licence for the specific language governing
# permissions and limitations under the Licence.

FROM node:16.0.0-buster as js-builder

# First the urls for sms backend and cv backend
ARG SMS_BACKEND_URL_ARG
ENV SMS_BACKEND_URL $SMS_BACKEND_URL_ARG

ARG CV_BACKEND_URL_ARG
ENV CV_BACKEND_URL $CV_BACKEND_URL_ARG

ENV INSTITUTE ufz

# Then the client id for open id connect and the authority to contact
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG

ARG AUTHORITY_ARG
ENV NUXT_ENV_AUTHORITY $AUTHORITY_ARG

# The redirect uris (those must be different per host on that the frontend runs)
ARG HOST_ARG
ENV BASE_URL /sms
ENV NUXT_ENV_REDIRECT_URI https://${HOST_ARG}${BASE_URL}/login-callback
ENV NUXT_ENV_POST_LOGOUT_REDIRECT_URI https://${HOST_ARG}${BASE_URL}/logout-callback
ENV NUXT_ENV_SILENT_REDIRECT_URI https://${HOST_ARG}${BASE_URL}/silent-callback

# And those remaining settings
ENV NUXT_ENV_RESPONSE_TYPE id_token
ENV NUXT_ENV_SCOPE openid profile email
ENV NUXT_ENV_FILTER_PROTOCOL_CLAIMS false
ENV NUXT_ENV_AUTOMATIC_SILENT_RENEW false
# TODO; Check here if we still need this one
ENV NUXT_ENV_SILENT_RENEW_INTERVAL 6900000
ENV NUXT_ENV_LOAD_USER_INFO true
ENV NUXT_ENV_PUBLIC_PATH=""

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG

RUN mkdir /smsfrontend
COPY . /smsfrontend
WORKDIR /smsfrontend
RUN npm ci
RUN npm run build

FROM nginx:alpine as webserver

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="Martin Abbrent <martin.abbrent@ufz.de>" \
    org.opencontainers.image.title="Sensor management frontend" \
    org.opencontainers.image.authors=" \
      Marc Hanisch <marc.hanisch@gfz-potsdam.de>  \
      Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>  \
      Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>"  \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.created=$BUILD_DATE

COPY --from=js-builder /smsfrontend/dist/ /usr/share/nginx/html/rdm/svm

# SPDX-FileCopyrightText: 2020 - 2024
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM node:18.18.0-buster as js-builder

# First the urls for sms backend, cv backend
ARG SMS_BACKEND_URL_ARG
ENV SMS_BACKEND_URL $SMS_BACKEND_URL_ARG

ARG CV_BACKEND_URL_ARG
ENV CV_BACKEND_URL $CV_BACKEND_URL_ARG

ENV INSTITUTE ufz

# Then the client id for open id connect and the authority to contact
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG

# The redirect uris (those must be different per host on that the frontend runs)
ARG BASE_URL_ARG=/sms
ENV BASE_URL $BASE_URL_ARG

ARG NUXT_ENV_PID_BASE_URL
ENV NUXT_ENV_PID_BASE_URL $NUXT_ENV_PID_BASE_URL

# And those remaining settings
ENV NUXT_ENV_SCOPE openid profile email offline_access

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG

# PKCE
ARG NUXT_ENV_OIDC_SCHEME
ENV NUXT_ENV_OIDC_SCHEME $NUXT_ENV_OIDC_SCHEME

ARG NUXT_ENV_OIDC_WELL_KNOWN
ENV NUXT_ENV_OIDC_WELL_KNOWN $NUXT_ENV_OIDC_WELL_KNOWN

ARG NUXT_ENV_OIDC_REFRESH_TOKEN
ENV NUXT_ENV_OIDC_REFRESH_TOKEN $NUXT_ENV_OIDC_REFRESH_TOKEN

ARG NUXT_ENV_OIDC_REFRESH_EXPIRE
ENV NUXT_ENV_OIDC_REFRESH_EXPIRE $NUXT_ENV_OIDC_REFRESH_EXPIRE

ARG NUXT_ENV_OIDC_GRANT_TYPE
ENV NUXT_ENV_OIDC_GRANT_TYPE $NUXT_ENV_OIDC_GRANT_TYPE

ARG NUXT_ENV_OIDC_CHALLANGE
ENV NUXT_ENV_OIDC_CHALLANGE $NUXT_ENV_OIDC_CHALLANGE

ARG NUXT_ENV_OIDC_LOGIN_PARAMS
ENV NUXT_ENV_OIDC_LOGIN_PARAMS $NUXT_ENV_OIDC_LOGIN_PARAMS

ARG NUXT_ENV_OIDC_LOGIN_PARAMS
ENV NUXT_ENV_OIDC_LOGIN_PARAMS $NUXT_ENV_OIDC_LOGIN_PARAMS

ARG NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME
ENV NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME $NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME

ARG NUXT_ENV_OIDC_RESPONSE_TYPE
ENV NUXT_ENV_OIDC_RESPONSE_TYPE $NUXT_ENV_OIDC_RESPONSE_TYPE

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

COPY --from=js-builder /smsfrontend/dist/ /usr/share/nginx/html/rdm/sms
COPY ./docker/deployment/ufz/default.conf /etc/nginx/conf.d/default.conf

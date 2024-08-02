# SPDX-FileCopyrightText: 2021 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
# - Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3, https://www.fz-juelich.de/en/ibg/ibg-3)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM node:18.18.0-buster as js-builder

# First the urls for sms backend and cv backend
ENV SMS_BACKEND_URL /backend/api/v1
ENV CV_BACKEND_URL https://sms-cv.helmholtz.cloud/sms/cv/api/v1
ENV IDL_SYNC_URL /idl/api/hifis/sync-groups

ENV INSTITUTE fzj

# Then the client id for open id connect and the authority to contact
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG
ENV NUXT_ENV_OIDC_WELL_KNOWN https://login.helmholtz.de/oauth2/.well-known/openid-configuration
ENV NUXT_ENV_OIDC_SCHEME true

ENV NUXT_ENV_SCOPE profile openid email eduperson_principal_name

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG

ENV NUXT_ENV_OIDC_REFRESH_TOKEN refresh_token
ENV NUXT_ENV_OIDC_REFRESH_EXPIRE 28800
ENV NUXT_ENV_OIDC_RESPONSE_TYPE code
ENV NUXT_ENV_OIDC_GRANT_TYPE authorization_code
ENV NUXT_ENV_OIDC_CHALLANGE S256
ENV NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME 1800000

ENV NUXT_ENV_PID_BASE_URL https://hdl.handle.net

ARG SMS_VERSION_ARG=staging
ENV SMS_VERSION $SMS_VERSION_ARG

RUN mkdir /smsfrontend
COPY ./frontend /smsfrontend
WORKDIR /smsfrontend
RUN sed -i 's/"version": ".*"/"version": "'"$SMS_VERSION"'"/' package.json
RUN npm ci
RUN npm run build

FROM nginx:alpine as webserver
EXPOSE 443
EXPOSE 8443
COPY --from=js-builder /smsfrontend/dist/ /usr/share/nginx/html
COPY ./docker/build/nginx/fzj/staging/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/build/nginx/fzj/staging/default.conf /etc/nginx/conf.d/default.conf

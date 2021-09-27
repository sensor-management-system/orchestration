# Web client of the Sensor Management System software developed within
# the Helmholtz DataHub Initiative by GFZ and UFZ.
#
# Copyright (C) 2020
# - Wilhelm Becker (GFZ, wilhelm.becker@gfz-potsdam.de)
# - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
# - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for
#   Geosciences (GFZ, https://www.gfz-potsdam.de)
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

ENV INSTITUTE gfz

# Then the parameter and endpoints for open id connect
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG

ARG AUTHORITY_ARG
ENV NUXT_ENV_AUTHORITY $AUTHORITY_ARG

ARG OIDC_TOKEN_ARG
ENV NUXT_ENV_OIDC_TOKEN $OIDC_TOKEN_ARG

ARG OIDC_REFRESH_TOKEN_ARG
ENV NUXT_ENV_OIDC_REFRESH_TOKEN $OIDC_REFRESH_TOKEN_ARG

ARG OIDC_REFRESH_EXPIRE_ARG
ENV NUXT_ENV_OIDC_REFRESH_EXPIRE $OIDC_REFRESH_EXPIRE_ARG

ARG OIDC_RESPONSE_TYPE_ARG
ENV NUXT_ENV_OIDC_RESPONSE_TYPE $OIDC_RESPONSE_TYPE_ARG

ARG OIDC_GRANT_TYPE_ARG
ENV NUXT_ENV_OIDC_GRANT_TYPE $OIDC_GRANT_TYPE_ARG

ARG OIDC_CHALLANGE_ARG
ENV NUXT_ENV_OIDC_CHALLANGE $OIDC_CHALLANGE_ARG

# And those remaining settings
# the following is the ufz setting
#ENV NUXT_ENV_SCOPE openid profile email
# and this is our setting
ENV NUXT_ENV_SCOPE profile

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG

RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm ci
RUN npm run build

FROM nginx:alpine as webserver
COPY --from=js-builder /ssmfrontend/dist/ /usr/share/nginx/html

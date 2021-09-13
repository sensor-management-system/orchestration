# Web client of the Sensor Management System software developed within
# the Helmholtz DataHub Initiative by GFZ and UFZ.
# 
# Copyright (C) 2020-2021
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
ENV SMS_BACKEND_URL /backend/api/v1
ENV CV_BACKEND_URL /cv/api/v1

ENV INSTITUTE gfz

# Then the client id for open id connect and the authority to contact
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG

# For the moment we stay with the dev idp
ENV NUXT_ENV_AUTHORITY https://idp-dev.gfz-potsdam.de/cas/oidc/authorize

# And those remaining settings
# the following is the ufz setting
#ENV NUXT_ENV_SCOPE openid profile email
# and this is our setting
ENV NUXT_ENV_SCOPE profile

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG


RUN mkdir /smsfrontend
COPY ./frontend /smsfrontend
WORKDIR /smsfrontend
RUN npm ci
RUN npm run build

FROM nginx:alpine as webserver
EXPOSE 80
EXPOSE 443
EXPOSE 8443
COPY --from=js-builder /smsfrontend/dist/ /usr/share/nginx/html
COPY ./docker/build/nginx/gfz/prod/default.conf /etc/nginx/conf.d/default.conf



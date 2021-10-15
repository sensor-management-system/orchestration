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

FROM node:16.0.0-buster

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

# VERY IMPORTANT: That is the root path of the application and all additional files on the server
ENV BASE_URL /sms

# And those remaining settings
ENV NUXT_ENV_SCOPE openid profile email

# The allowed mime types
ARG ALLOWED_MIME_TYPES_ARG
ENV NUXT_ENV_ALLOWED_MIMETYPES $ALLOWED_MIME_TYPES_ARG

RUN mkdir /smsfrontend
COPY . /smsfrontend
WORKDIR /smsfrontend
RUN npm ci
RUN npm run build

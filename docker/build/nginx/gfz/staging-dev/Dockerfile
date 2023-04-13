# SPDX-FileCopyrightText: 2021
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

# Web client of the Sensor Management System software developed within
# the Helmholtz DataHub Initiative by GFZ and UFZ.
# 
# Copyright (C) 2020-2021
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

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

FROM nginx:alpine

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

COPY ./dist/ /usr/share/nginx/html/rdm/svm

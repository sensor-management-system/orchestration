# SPDX-FileCopyrightText: 2021 - 2024
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM node:18.18.0-buster as js-builder

RUN mkdir /smsfrontend
COPY . /smsfrontend
WORKDIR /smsfrontend
RUN npm ci

ENTRYPOINT [ "npm", "run", "build" ]

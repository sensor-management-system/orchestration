# SPDX-FileCopyrightText: 2022 - 2023
# - Hannes Bohring <hannes.bohring@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

FROM nginx:1.25-alpine

COPY ./backend/docker/build/nginx/ufz/nginx.conf /etc/nginx/nginx.conf
COPY ./backend/docker/build/nginx/ufz/default.conf /etc/nginx/conf.d/default.conf

COPY ./backend/docker/build/nginx/ufz/entrypoint.sh /custom-entrypoint.sh

COPY ./backend/app/project/static /usr/share/nginx/html/static

RUN chmod 555 /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
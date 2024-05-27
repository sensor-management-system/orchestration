# SPDX-FileCopyrightText: 2022 - 2024
# - Hannes Bohring <hannes.bohring@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

FROM nginx:1.24-alpine

COPY default.conf /etc/nginx/conf.d/default.conf

COPY entrypoint.sh /custom-entrypoint.sh

RUN chmod 555 /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]


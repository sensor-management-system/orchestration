<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Important Information

With important information we mean theses kind of information you'll need to connect you application with the client to keycloak.

- Make sure you have selected the right realm `local-dev`
- The Client ID
  - Go to `clients` in left menu
  - Select the client you want, e.g. `sms-client`
  - there you find the `Client ID`
- The Client Secret
  - Go to `clients` in left menu
  - Select the client you want, e.g. `sms-client`
  - go to `Credentials` tab
  - there you find the `Client Secret`
- Well Known Url
  - Go to `realm settings` in left menu
  - in the current `general` tab you find the `Endpoints`
  - Select the `OpenID Endpoint Configuration`
  - e.g. `http://keycloak:KEYCLOAK_PORT/realms/local-dev/.well-known/openid-configuration`

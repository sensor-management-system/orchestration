<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
# Keycloak

## Purpose
The purpose of this keycloak is to avoid the dependency to the [Helmholtz AAI](https://hifis.net/aai/) and to mock its behavior.

## Documents

- [Configuration.md](./docs/Configration.md)
  - Contains all information how the Keycloak was setup
- [Important Information.md](./docs/Important Information.md)
  - Contains information you need to connect an application to a client and where to find that information
- [Specification for sms.md](./docs/Specification for sms.md)
  - Contains information specific for the time.IO client:
    - Created groups
    - Created users
    - __Which environment variables you need to set__
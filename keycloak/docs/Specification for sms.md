<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Specification for SMS configuration

## Environment Variables

```
...
NUXT_ENV_OIDC_TOKEN=http://keycloak:${KEYCLOAK_PORT}/realms/local-dev/protocol/openid-connect/token
NUXT_ENV_CLIENT_ID=sms-client
WELL_KNOWN_URL=http://keycloak:${KEYCLOAK_PORT}/realms/local-dev/.well-known/openid-configuration
...
OIDC_WELL_KNOWN_URL=${WELL_KNOWN_URL} # for local sms-idl
```
- __NOTE__
  - The order of the variables is important:
    - e.g.: If you use `NUXT_ENV_OIDC_TOKEN=http://keycloak:${KEYCLOAK_PORT}/realms/local-dev/protocol/openid-connect/token` the __KEYCLOAK_PORT__ must be declared before that line in you env-file


## Created groups:

  - `a:a:a:group:VO:Group1:admin#`
  - `a:a:a:group:VO:Group1:member#`
  - `a:a:a:group:VO:Group2:admin#`
  - `a:a:a:group:VO:Group2:member#`
  - `Exportcontrol`

- __Note__:

  - Please note that the `VO` name must be added to the `ALLOWED_VOS` environment variable of the `tsm-frontend` to make the group selectable

## Created user:
  - __Note__:  All users have the password `password`


| Username | Groups                                                           | Purpose                                                      |
| -------- |------------------------------------------------------------------| ------------------------------------------------------------ |
| `user1`  | `a:a:a:group:VO:Group1:admin#`, `a:a:a:group:VO:Group2:admin#`, `Exportcontrol` | a user with role `admin` in two valid groups                 |
| `user2`  | `a:a:a:group:VO:Group1:admin#`, `a:a:a:group:VO:Group2:member#`  | - a user with role `admin` in one group of `user1`<br />-  a user with role `member` in one group of `user1` |
| `user3`  | `a:a:a:group:VO:Group1:member#`                                  | a user with role `member` in one group of `user1`            |
| `user4`  | -                                                                | a user not in any group                                      |


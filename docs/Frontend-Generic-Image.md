<!--
SPDX-FileCopyrightText: 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Generic Frontend Image
## Description
Currently the several institutes need several Dockerfiles to build the SMS Frontend for their several deployments, because environment variables need to be passed during build time and baked into the resulting html, js, css.

With the new generic image we try to tackle that problem and provide one image to suite all deployments and make it possible to set frontend side environments during runtime.
## How it works
The key to the solution is how the environment variables in the sms frontend are declared, e.g. `const NUXT_ENV_OIDC_REFRESH_TOKEN = process.env.NUXT_ENV_OIDC_REFRESH_TOKEN || 'NUXT_ENV_OIDC_REFRESH_TOKEN_ENV_PLACEHOLDER'`.
With `process.env.NUXT_ENV_OIDC_REFRESH_TOKEN` environment variables can be directly passed. This is useful for development.

During build time no environment variables are passed expect `SMS_VERSION_ARG`, therefore all variables will have the `<..._ENV_PLACEHOLDER>` string as values, e.g. `const NUXT_ENV_OIDC_REFRESH_TOKEN ='NUXT_ENV_OIDC_REFRESH_TOKEN_ENV_PLACEHOLDER'`.

The new Dockerfile has a entrypoint script, that searches for these placeholder strings and replaces them with the actual values passed to the container during runtime.

Another challenge is that the several institutes have different configurations for the nginx. The solution is to provide these configuration files as volume mounts in the several deployments. The new image comes with a minimal `default.conf` for the nginx, which can be replaced by volume mounts.

The new image will be added to the container registry of the sms and build in the pipeline for every new version of the sms. 
## How to use it
### Important
You must provide your own nginx configuration files and mount them to the right places during runtime.
__Important__ is the correct definition of the location of the frontend. 
See the following example, for a working nginx configuration.

### Example
Here is an example, how to use it with a minimal nginx configuration file and a docker-compose.yml.
The goal of this example is to make the frontend available under the path `/sms`. 

#### nginx config
`default.conf`:
```
server {
  listen       80;
  listen  [::]:80;
  server_name  localhost;
  root /usr/share/nginx/html/;

  location /sms {
    alias /usr/share/nginx/html/;
    index index.html;
    try_files $uri $uri/ /index.html;
  }
}

```

#### docker-compose.yml
`docker-compose.yml`

```yaml
services:
  sms:
    image: path-to-correct-frontend-image-in-hzdr-registry:1.0.0 # the real image will be accessable in https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/container_registry and be build for every new version in the ci/cd pipeline
    ports:
      - 80:80
    volumes:
      - "./nginx-example/default.conf:/etc/nginx/conf.d/default.conf"
    environment:
      - "NUXT_ENV_OIDC_REFRESH_TOKEN_ENV_PLACEHOLDER=refresh_token"
      - "NUXT_ENV_OIDC_REFRESH_EXPIRE_ENV_PLACEHOLDER=2592000"
      - "NUXT_ENV_OIDC_RESPONSE_TYPE_ENV_PLACEHOLDER=code"
      - "NUXT_ENV_OIDC_GRANT_TYPE_ENV_PLACEHOLDER=authorization_code"
      - "NUXT_ENV_CLIENT_ID_ENV_PLACEHOLDER=sms-client"
      - "NUXT_ENV_SCOPE_ENV_PLACEHOLDER=openid profile eduperson_principal_name email offline_access"
      - "NUXT_ENV_OIDC_CHALLANGE_ENV_PLACEHOLDER=S256"
      - "SMS_BACKEND_URL_ENV_PLACEHOLDER=/backend/api/v1"
      - "CV_BACKEND_URL_ENV_PLACEHOLDER=/cv/api/v1"
      - "IDL_SYNC_URL_ENV_PLACEHOLDER=http://localhost/idl/api/hifis/sync-groups/"
      - "INSTITUTE_ENV_PLACEHOLDER=ufz"
      - "NUXT_ENV_PID_BASE_URL_ENV_PLACEHOLDER=https://hdl.handle.net"
      - "NUXT_ENV_OIDC_WELL_KNOWN_ENV_PLACEHOLDER=http://keycloak:8082/keycloak/realms/local-dev/.well-known/openid-configuration"
      - "NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME_ENV_PLACEHOLDER=900000"
      - "BASE_URL_ENV_PLACEHOLDER=/sms"
      
      
```

With this setup, you could access the sms under `<my-fancy-domain>/sms`
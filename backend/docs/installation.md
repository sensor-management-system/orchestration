<!--
SPDX-FileCopyrightText: 2020 - 2021
- Martin Abbrent <martin.abbrent@ufz.de>
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
- Norman Ziegner <norman.ziegner@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Installation

There are multiple ways to install the application. This document describes a [Compose](#compose),  
a [Docker](#docker) and a [Local](#local) installation. The preferred and easiest way to quickly get  
it running is [Compose](#compose). Once you finished the installation navigate to  
[http://localhost:5000/rdm/svm-api/v1/ping](http://localhost:5000/rdm/svm-api/v1/ping) in your browser. You should see:

```json
{
"message": "Pong",
"status": "success"
}

```

## Dependencies


- Get docker. See the [official site](https://docs.docker.com/engine/install/) for installation info for your platform.
- Install docker-compose. Windows and Mac users should have docker-compose 
 by default as it is part of Docker toolbox. For Linux users, see the [official guide](https://docs.docker.com/compose/install/). 

## Compose
**Note:** To generate self singed certificate you can use the python script `ngnix/certs/ice-ca-certs.py`. The script requires the python library *zeroc-icecertutils*, which you can install with `pip install zeroc-icecertutils`. Make sure you execute the script inside the target folder `nginx/certs`.
1. copy the file `env.template`. Fill the variables and rename it to .env.dev
2. Start the containers and run them in background:

    ```bash
    docker-compose --env-file ./app_env/.env.dev  up -d
    ```

    This will take a few minutes the first time. Subsequent builds will be much faster since Docker caches
    the images once they are downloaded.

    You can watch the output of the containers witch `docker-compose logs`:

    ```bash
    docker-compose logs --follow 
    ```


**Note:** When ORM models change create alembic migration scripts

   1. create script
       ```bash
       docker-compose exec app python3 manage.py db migrate
       ```
   2. apply script
        ```bash
        docker-compose exec app python3 manage.py db upgrade
        ```

## Docker

1. Build image

    ```bash
    docker build -t registry.hzdr.de/hub-terra/sms/backend:`date +%Y-%m-%d`-1 \
        --build-arg BUILD_DATE=$(date --utc +%FT%TZ) \
        --build-arg VCS_REF=$(git rev-parse HEAD) .
    ```


2. When running it the first time you have to create the database tables before:

    When running the application container standalone (in contrast to the  
    Docker [Compose](#compose) variant) you have to explicitly specify a database URL.

    ```bash
    docker run --rm \
         -e DATABASE_URL="postgres://postgres:postgres@localhost:5432/db_dev" \
         -e APP_SETTINGS="project.config.DevelopmentConfig" \
         registry.hzdr.de/hub-terra/sms/backend:latest \
         python manage.py db upgrade
    ```

4. Run the container

    ```bash
    docker run --rm -p 127.0.0.1:5000:5000 \
         -e DATABASE_URL="postgres://postgres:postgres@localhost:5432/db_dev" \
         -e APP_SETTINGS="project.config.DevelopmentConfig" \
         -e FLASK_DEBUG=1 \
         registry.hzdr.de/hub-terra/sms/backend:latest
    ```

##  Local

### Dependencies required to run the Server

- Python >= 3.6
- PostgreSQL
- Elasticsearch
- Minio

To run the server local without docker, please execute the following from the app directory:

1. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Create the database. For that we first open the psql shell.
```bash
sudo -u postgres psql
 ```
Then:
```sql
CREATE DATABASE db_dev
```
Once database created, exit the psql shell with `\q` followed by ENTER.

After that, Create the tables.
```bash
python3 manage.py db upgrade
```

3. Start development server:


    ```bash
    export FLASK_APP=project/__init__.py
    python manage.py run
    ```

## UFZ WOMBAT K8s

(Re-) creation of database schema:

1. Connect to running backend container shell

    ```bash
    kubectl --context=wombat-stage-intern exec custom-rdm-svm-5f4fd99776-j4fjz --container=frontend sh -ti
    ```

2. Temporarily change the database credentials to adm-user to allow schema modification
3. Run `python manage.py db upgrade`


After recreation of database schema:

```postgresql
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO rdm_sis_stage_rw;
```
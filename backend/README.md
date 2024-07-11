<!--
SPDX-FileCopyrightText: 2020 - 2023
- Martin Abbrent <martin.abbrent@ufz.de>
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Norman Ziegner <norman.ziegner@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# API for Sensor Management System SMS

[![pipeline status](https://gitlab.hzdr.de/hub-terra/sms/backend/badges/master/pipeline.svg)](https://gitlab.hzdr.de/hub-terra/sms/backend/-/commits/master)
[![version](https://img.shields.io/badge/version-v1.0-lightgrey.svg)](./README.md) [![python](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg?style=?style=plastic&logo=python)](#)
[![pylint](https://img.shields.io/badge/lint%20score-9.97/10-yellowgreen.svg )](https://gitlab.hzdr.de/hub-terra/sms/backend/-/jobs?job=unittest-lint)
[![r_licenses](https://img.shields.io/badge/requirements_licenses-check-redyellow.svg?style=plastic&logo=open-source-initiative)](./docs/requirements_licenses.md)
[![openapi](https://img.shields.io/badge/Swagger-2.0-green.svg?style=?style=plastic&logo=openapi-initiative)](./app/project/static/swagger.json)
[![licences](https://img.shields.io/badge/licenses-MIT-green.svg?style=?style=plastic&logo=)](#)

![Data model](docs/images/alembic_version_0740d341ea8e.png)

RESTful API service in Python for managing sensor metadata using [flask](https://flask.palletsprojects.com/en/1.1.x/).

### Documentation

This Project uses OpenAPI to describe both the service model (the API in general, endpoints, request
metadata like headers, authentication strategies, response metadata, etc.),
and it also covers the HTTP request/response body using a bunch of keywords
based on JSON Schema.

[See Swagger file in gitlab](app/project/static/swagger.json)
Or  navigate to **`$HOST/rdm/svm-api/v1/docs`**

[For Health check navigate to $HOST/rdm/svm-api/v1/healthcheck**]()


### Technical Specs

- python 3.6+: Python Language supported and tested
- Flask: Micro Python Web Framework, good for microservice development and python WSGI apps.
- [OpenAPI](https://swagger.io/specification/) 3: specification to describe both the service model
- [Flask-REST-JSONAPI](https://flask-rest-jsonapi.readthedocs.io/en/latest/index.html):
flask plugin for JSON Schema to describe an instance of JSON data, like the a HTTP request
 or response.
- [Docker](https://docs.docker.com/get-started/overview/): A containerization tool for better devops
- [Docker Compose](https://docs.docker.com/compose/): Tool for defining and running multi-container Docker applications


### Local Development

**Note**: For running elasticsearch it may be necessary to increase the maximal
map count for the virtual memory:

```
sudo sysctl vm.max_map_count=262144
```

### Migration

To generate migrations as SQL scripts, instead of running them against the database use `sqlmigrate`:

`alembic upgrade <migration_file_name> --sql > migration.sql`

An example:

`pythonupgrade  0139893c4e15  --sql > migration.sql`

#### How to pass a mocked JWT to the API for testing

To work with mocked JWT you need at first to change the app setting in the `compose.env` file:

`APP_SETTINGS=project.config.TestingConfig`
Then you can get the JWT by running:

`docker-compose exec app  python manage.py test project.tests.generate_test_jwt`

#### Dummy & demo data

To fill the database with demo data for testing you can use the demo sql data as follows:
> docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
```
docker cp ./backend/data/emo_paltforms_data.sql orchestration_db_1:/docker-entrypoint-initdb.d/dump.sql
docker-compose exec db -u postgres psql postgres postgres -f docker-entrypoint-initdb.d/dump.sql
```

### Usage

After having installed the dependencies, then just run the following commands to use it:

[Simple CRUD](docs/usage.md)

### Test

[How to run the tests](docs/test.md)

### Filter & Include & sort

[How to user filters](docs/filtering.md)

## FAQ

### What is the connection between the user subject and the username from the IDL?

We use the users subject entry as a user readable unque identifier for our
users. It looks like

```
username@institute.org
```

In past it was identical to the `sub` entry in the userinfo response of
the IDP instances (both at UFZ and GFZ).

With the switch to the Helmholtz AAI, this changed.
We introducted the `OIDC_USERNAME_CLAIM` environment variable
(default to `sub`) to make it configurable from which attribute of the user
response we want to fill our subject entry in the user table.

The Helmholtz AAI fills `sub` with cryptic uuid, which is unique, but not
user friendly readable. However it gives the `eduperson_principal_name`
which is exactly what we used for subject in the past.

In any case the interaction with the IDL will use the subject from our
users table to search for usernames within the IDL.
So both should be identical.

In case you want to use the `gfz-idl` implementation, as well as the
Helmholtz AAI, make sure that you set the `OIDC_USERNAME_CLAIM` variable
to `eduperson_principal_name`.

### Can I import devices?

There is an csv importer script. You can find more details [here](./csv_importer/readme.md).

## CLI commands for admins

<details>
<summary>CLI commands</summary>


**user deactivation/reactivation**

When attend to deactivate/activate a user. Use users cli.

```
# Deactivate a user
python manage.py users deactivate srcuserubject@ufz.de

# Deactivated and provide a substituted user
python manage.py users deactivate srcuserubject@ufz.de --dest-user-subject=destusersubject@ufz.de

# Activate a user
python manage.py users reactivate srcuserubject@ufz.de
```

**Model updates & migrations**

When writing changes to the models. Use migrations.

```bash
# To generate a migration after doing a model update
python manage.py db migrate

# To sync Database
python manage.py db upgrade

# To rollback
python manage.py db downgrade
```

**Update of names with latest CV terms**

When the user suggests a new term it can happen that the term
needs renaming after the curation team decided to go with a
slightly different name.

With the following command we can update all the CV related entries
with their latest terms from the CV:

```bash
python manage.py cv apply-current-terms-to-sms
```

**loading of fixture data**

We support a command that mimics the django loaddata command.
It can be used to integrate data from an json file like this:

```javascript
[
  {
    "fields": {
      "name": "some endpoint",
      "url": "http://localhost"
    },
    "model": "TsmEndpoint",
    "pk": 1
  }
]
```

```bash
python3 manage.py loadata path/to/file.json
```
Please note:
- we currently just support json files as input
- there is no support for composed primary keys at the moment
- the pk maps to the id column all of our current cases
- the value for model is the name of the class (not the table).
- field names map to the column names in the SqlAlchemy class
- setting foreign keys will be done with the foreign key attribute and
  not with the sqlalchemy relationship.


</details>

## Deployment

### UFZ
- The following environment variable secrets will be set by the admins of the kubernetes cluster (wombat) and are therefore not appearing in the Dockerfiles nor in the CI pipeline:
  - DATABASE_URL
  - MINIO_SECRET_KEY
  - SMS_IDL_TOKEN
  - PID_SERVICE_PASSWORD

## Authors

- Dirk Pohle
- Kotyba Alhaj Taha
- Martin Abbrent
- Nils Brinckmann
- Norman Ziegner
- Wilhelm Becker
- Tobias Kuhnert

<!--
SPDX-FileCopyrightText: 2021 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Norman Ziegner <norman.ziegner@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Sensor Management System

## Description

The Sensor Management System (SMS) allows the comprehensive
acquisition, administration and export of metadata of platforms,
sensors and measurement configurations by stations and campaigns
operated in the Helmholtz research field Earth & Environment.

Information on specific setups can be summarized and made available
as metadata together with the data for scientific evaluations,
making the data genesis permanently traceable and transparent via
provenance tracking. In the data management cycle, the service
particularly supports the acquisition of additional information
during data collection and prepares the publication of research
data with associated metadata by capturing and providing relevant
information about the measurement setup during data generation.
The service is targeted at the work of scientists and technicians
in the earth and environmental sciences, but also offers sufficient
flexibility for use in other domains as well as individual extension
and customization possibilities due to the use of common standards.

## Changelog

You can find the versions and their changes in [CHANGELOG.md](./CHANGELOG.md).

## Instances

- https://sensors.gfz-potsdam.de
- https://web.app.ufz.de/sms/
- https://sms.atmohub.kit.edu/
- https://ibg3sms.ibg.kfa-juelich.de/ (FZJ intranet only)

## Authors

- [Nils Brinckmann](https://orcid.org/0000-0001-8159-3888)
- Kotyba Alhaj Taha
- Tobias Kuhnert
- [Marc Hanisch](https://orcid.org/0000-0001-5272-4674)
- Maximilian Schaldach
- Florian Gransee
- [Daniel Sielaff](https://orcid.org/0009-0002-8606-9385)
- [Tim Eder](https://orcid.org/0009-0005-1965-931X)
- Luca Johannes Nendel
- [Norman Ziegner](https://orcid.org/0000-0001-7579-216X)
- [Hannes Bohring](https://orcid.org/0009-0007-5103-5886)
- [Rubankumar Moorthy](https://orcid.org/0000-0002-3567-1475)
- Wilhelm Becker
- [Martin Abbrent](https://orcid.org/0000-0003-1252-9107)
- Erik Pongratz
- [Dirk Ecker](https://orcid.org/0000-0003-4241-9208)
- [Christof Lorenz](https://orcid.org/0000-0001-5590-5470)
- [Paul Remmler](https://orcid.org/0000-0001-8900-9009)
- [Vivien Rosin](https://orcid.org/0009-0003-9261-6696)
- Marie Schaeffer
- [Jannes Breier](https://orcid.org/0000-0002-9055-6904)

## API Reference

The openapi specification can be explored interactively on the sms instances.
For example [on sensors.gfz-potsdam.de](https://sensors.gfz-potsdam.de/backend/api/v1/openapi).

## Orchestration

![SMS work flow](docs/images/sms.png)

## Demo instance

If you just want to try out the Sensor Management System, you are welcome to do
so on [our test instance](https://sensors-sandbox.gfz-potsdam.de). 

⚠️ Please be aware that the data you enter there will not be stored permanently
and the instance should not be used for productive work!

## Usage

### Set up Controlled Vocabulary
The sms-cv (controlled vocabulary) is included as a git submodule.

Run the following commands to set up the submodule:
  - `git submodule init`  
  - `git submodule update` 

### Run the application
```
docker compose up -d
```

Visit http://localhost

Use one of the users specified in [keycloak/docs/Specification for sms.md](./keycloak/docs/Specification for sms.md) to login.

#### If you want to change the default variables
- Copy all files ending with
   ```env.template```. Fill the variables and rename it
   to ```env.dev```
```
cp ./docker/env.template ./docker/env.dev
```

- Start the containers and run them in background:

```bash
    docker compose --env-file ./docker/env.dev  up -d
```

## TSM Endpoints

We include all the tsm endpoints in the database and can use the `manage.py loaddata <path>` command to add or
update those.

The current approach is to store them in the TSM_ENDPOINTS env variable as an json array, to write it to an temporary file
and to load it with the `loaddata` command:

```
    - docker compose -f docker/deployment/gfz/staging-dev/docker-compose.yml exec -T backend sh -c "echo '$TSM_ENDPOINTS' > /tmp/tsm_endpoint_fixture.json"
    - docker compose -f docker/deployment/gfz/staging-dev/docker-compose.yml exec -T backend python3 manage.py loaddata /tmp/tsm_endpoint_fixture.json
```

The content of the TSM_ENDPOINTS variable looks like this:

```javascript
[
  {
    "pk": 1,
    "model": "TsmEndpoint",
    "fields": {
      "name": "Specific tsm endpoint",
      "url": "https://somewhere.in.the/web"
    }
  }
]
```

Feel free to add your tsm endpoint here.

Please note: Regarding that we may want to provide a central instance in the future, it makes sense to keep the ids of the
ids of the endpoints distinct. So to have pk=1 for GFZ, pk=2 for UFZ, pk=3 for FZJ, pk=4 for KIT and so on. Doing so can
make an merge of the data much easier (but it is also possible to work around it).

## Export control

The export control workflow implemented in the SMS is there to allow export control
officers on the centres to store information if a device or a platform can be
used for military uses (dual use) and requires extra documents when transported
to different countries.

While the usual handling in the SMS is based on physical devices, the export control
works on their device types - in this case the combination of manufacturer & model - so
that the check needs to be done just once for a group of devices or platforms.

The permission to handle those information is bound to the `EXPORT_CONTROL_VO_LIST`
env variable. It is a comma seperated list that points to the full qualified name
of a virtual organization (VO). If you use a sub group of your VO it will look like this: `urn:geant:helmholtz.de:group:<VO Name>:<Group Name>#login.helmholtz.de`.
The full name of the group muss be added to the `EXPORT_CONTROL_VO_LIST`.

For the GFZ we have a `sensor-management-system-export-control` group within myprofile.
This is visible as `urn:geant:helmholtz.de:gfz:group:sensor-management-system-export-control#idp.gfz-potsdam.de` within the Helmholtz AAI - and this is the value that is
used in the `EXPORT_CONTROL_VO_LIST` variable.

## Restore the backups (gfz)

Please note: Before you try any restore command, try to test the result locally. You can use the orchestration repos docker-compose file
to start the postgres databases. If you replace the `createbuckets` image with the one for `docker/build/mc/gfz/Dockerfile` you can also
test the minio restore (in the GFZ deployments this service is called `mc`).

For staging and prod we create backups on a regular basis (before every deployment for both, and on a daily basis for prod as well).
Those are stored under 

- `/srv/docker/service/backend-db/backups`
- `/srv/docker/service/vocabulary-db/backups`
- `/srv/docker/service/minio/backups`

We also save those backups for the productive machine on a project share
that is mounted on:

- `/mnt/sms-backup`

which can be found here as well:
- `rzv124n.gfz-potsdam.de:/PROJECT_124n_1/sms-backup`

The backups on the vms themselves are stored for 30 days,
the ones on the project share for 180.

The `*-db` backups are `pg_dump` flies in the compressed postgres binary format. Both can be restored with the `pg_restore`.

It should be possible with a command like this (not tested yet):

```
docker-compose -f docker/deployment/gfz/staging/docker-compose.yml exec -T backend-db pg_restore -d backend -Fc --clean --create' < /srv/docker/service/backend-db/backups/example.dump
```

You may also want to use the `-e` flag for pg_restore, so that it stops in the very first error.

It should be possible to restore the vocabulary-db in the very same way.

For the minio the restore is different:

- Make sure your minio server runs and that the bucket was already created.
- Start a new mc container with a bash session and mount your backup tar.gz file somewhere in the container file system.
- Extract all the data in an temporary folder.
- Register the minio client (`mc alias set`). See the /backup.sh command to check how to do it.
- Run the `mc mirror` command with our temporary folder as first argument, and your $minio/$bucket as second argument. You should check the
  possible flags for this command in order to care about creation dates, over the settings for overwriting existing files
  and the option to also remove entries that are not in the backup.
- There is currently no strategy to restore the metadata - we save them to keep track of the user uploads (if the user wasn't allowed
  to upload a file, we can check who was responsible for that)

## Test data for faster development
- You can use your own test data to be inserted directly into the database during your development process
- Do the following steps:
  - __Make sure that you `db` service is up and running__ 
  - `chmod +x preset-database.sh`
  - `cp ./sql/preset-development-and-test-data.sql.example ./sql/preset-development-and-test-data.sql`
  - Update the `./sql/preset-development-and-test-data.sql` file to your needs
    - __HINT__: If you use hard coded IDs make sure to update the corresponding sequences or you'll encounter problems 
  - run `./preset-database.sh`
  - 
## How to add new environment variables to the project
You have to look for many places. Keep in mind, that you always have look in the specific repository (e.g. `frontend` or `backend`) __and__ the orchestration repository 
### Frontend
#### In frontend repository
##### Usage in code
- Access environment variable via `process.env.YOUR_VARIABLE`
- Variable can be used directly if it starts with "NUXT_ENV_" (see Nuxt doc on [environment variables](https://nuxtjs.org/docs/configuration-glossary/configuration-env/))
- Otherwise add `nuxt.config.js` to `env:{...}`, you can then add via `process.env.YOUR_VARIABLE` (see Nuxt doc on topic [environment variables](https://nuxtjs.org/docs/configuration-glossary/configuration-env/))
##### UFZ Dockerfile
Add as new argument/variable to dockerfile
- `docker/deployment/ufz/Dockerfile` 
    ```
    ARG YOUR_VARIABLE
    ENV YOUR_VARIABLE $YOUR_VARIABLE
    ```
##### Institute-specific docker-compose.yaml(s)
Extend the following yamls under `environment` with your variable
- `docker-compose-gfz-local-with-staging-vm.yml`
- `docker-compose-ufz-local.yml`
##### In the CI/CD pipeline
- In the `.gitlab-ci.yml` [Link](https://gitlab.hzdr.de/hub-terra/sms/frontend/-/blob/master/.gitlab-ci.yml) add your variable to the appropriate stages for GFZ (`build-deploy-static-files-gfz`) and UFZ (`build-deploy-image-ufz`)
    - under `variables` add your new environment variable
        -  __be careful__ if you write the value hard-coded or set it via CI/CD variable (see next point "Setting CI/CD in Gitlab")
    - Under `script` add the line `--build-arg NUXT_ENV_[VARIABLE_NAME]=$[VARIABLE_NAME] \` and replace `[VARIABLE_NAME]` with your new variable
###### Setting CI/CD variables in Gitlab
- Go to the HZDR gitlab in the browser to the frontend repository, go to Settings > CI/CD
    - URL: (https://gitlab.hzdr.de/hub-terra/sms/frontend/-/settings/ci_cd)
    - Add under __Variables__ your variable with the appropriate value
#### In the Orchestration repository
##### Update env files
- Extend `docker/env.template` with your environment variable
- Extend `docker/env.dev` with your environment variable
    - You use this when starting the services via the docker-compose.yml in the orchestration repository
##### Extend docker-compose.yml
- Extend the service `frontend` in the section `environment` with your new environment variable

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
We introducted the `OIDC_USERNAME_CLAIM` environment variable for the backend
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

# Orchestration

## How to run

At first generate self signed certificate you can use the python
script `ngnix/certs/ice-ca-certs.py`. The script requires the python library *zeroc-icecertutils*,
which you can install with `pip install zeroc-icecertutils`. Make sure you execute the script inside
the target folder `nginx/certs`.

In case you have an older pip version you may have to run `pip install --upgrade pip`, so that the build process with rust is supported.

1. copy all files ending with
   ```env.template```. Fill the variables and rename it
   to ```env.dev```

2. Start the containers and run them in background:

```bash
    docker-compose --env-file ./docker/env.dev  up -d
```

3. In order to make sure that the search filter work, you have to create
   the search index on the elastic search:

```bash
docker-compose --env-file ./docker/env.dev exec backend python3 manage.py es reindex
```

This ensures that the search index can be used for full text search
**AND** for keyword search (without it search for specific
device types for example will not work).

Please note: You don't have to run the `reindex` on every startup.
It is important to run it initially and after each change in the structure of the
search index as well (new fields to index for example).



You can watch the output of the containers witch `docker-compose logs`:

```bash
docker-compose logs --follow 
```

## Additional step UFZ developer for Frontend local development - Identity Provider

You can't use `localhost` for local development to authenticate against an Identity Provider, but
you can use `localhost.localdomain`
Here's how you can do this on a Linux (Ubuntu) machine (feel free to search for your own operation
system):

- Adjust `hosts` file:
    - sudo edit /etc/hosts
    - add the following line: 127.0.0.1 localhost.localdomain
    - save

Application urls:

__Backend:__  `https://{HOST}/backend`

__Frontend:__ `https://{HOST}/`

__Controlled Vocabulary:__ `https://{HOST}/cv` 

__Minio Console:__ `https://{HOST}:8443/` 

## Restore the backups (gfz)

Please note: Before you try any restore command, try to test the result locally. You can use the orchestration repos docker-compose file
to start the postgres databases. If you replace the `createbuckets` image with the one for `docker/build/mc/gfz/Dockerfile` you can also
test the minio restore (in the GFZ deployments this service is called `mc`).

For staging and prod we create backups on a regular basis (before every deployment for both, and on a daily basis for prod as well).
Those are stored under 

- /srv/docker/service/backend-db/backups
- /srv/docker/service/vocabulary-db/backups
- /srv/docker/service/minio/backups

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

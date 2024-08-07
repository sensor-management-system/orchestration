<!--
SPDX-FileCopyrightText: 2021 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
# GFZ-Specific Instructions

## Restore backups

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

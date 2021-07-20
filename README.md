# Orchestration

## How to run

At first generate self singed certificate you can use the python
script `ngnix/certs/ice-ca-certs.py`. The script requires the python library *zeroc-icecertutils*,
which you can install with `pip install zeroc-icecertutils`. Make sure you execute the script inside
the target folder `nginx/certs`.

1. copy all files ending with
   ```backend.template, cv.template, env.template```. Fill the variables and rename it
   to ```backend.dev cv.dev env.dev```

2. Start the containers and run them in background:

```bash
    docker-compose --env-file ./app_env/.env.dev  up -d
```

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
    - sudo nano /etc/hosts
    - add the following line: 127.0.0.1 localhost.localdomain
    - save

Application urls:

__Backend:__ `https://{HOST}/sms-backend`

__Frontend:__ `https://{HOST}/sms/`

__Controlled Vocabulary:__ `https://{HOST}/sms-cv`

__Minio Console:__ `https://{HOST}:9002/`
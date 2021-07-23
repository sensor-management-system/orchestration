# Orchestration

## How to run

At first generate self signed certificate you can use the python
script `ngnix/certs/ice-ca-certs.py`. The script requires the python library *zeroc-icecertutils*,
which you can install with `pip install zeroc-icecertutils`. Make sure you execute the script inside
the target folder `nginx/certs`.

In case you have an older pip version you may have to run `pip install --upgrade pip`, so that the build process with rust is supported.

1. copy all files ending with
   ```backend.template, cv.template, env.template```. Fill the variables and rename it
   to ```backend.dev cv.dev env.dev```

2. Start the containers and run them in background:

```bash
    docker-compose --env-file ./docker/env.dev  up -d
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
    - sudo edit /etc/hosts
    - add the following line: 127.0.0.1 localhost.localdomain
    - save

Application urls:

__Backend:__  `https://{HOST}/backend` 

__Frontend:__ `https://{HOST}/`

__Controlled Vocabulary:__ `https://{HOST}/cv` 

__Minio Console:__ `https://{HOST}:8443/` 
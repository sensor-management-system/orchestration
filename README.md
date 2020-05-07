# SensorManagement

> a system to manage sensors and platforms

## Build Setup

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).

## Run development environment with docker

### Docker

```bash
docker run --rm -p 127.0.0.1:80:3000 --user node --workdir /home/node \
  -v `pwd`:/home/node node:current-slim \
  bash -c "npm install && npm run dev -- -H 0.0.0.0"
```

### Compose

```bash
docker-compose up -d          # Start container in detached mode
docker-compose logs --follow  # Watch output

```

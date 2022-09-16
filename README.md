# Sensor Management System

> a system to manage sensors and platforms

Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by [GFZ](https://www.gfz-potsdam.de) and
[UFZ](https://www.ufz.de).

## License

The software is distributed within the Helmholtz DataHub Initiative under the
**HEESIL License**. See [LICENSE](LICENSE).

## How to get started

### Development

```bash
# install dependencies
$ npm install --save-dev

# serve for development with hot reload at localhost:3000
$ npm run dev

# or build for production and launch server
$ npm run build
$ npm run start
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).

#### Running tests

Running all tests:
```bash
$ npm run test
```

Running a specific test:
```bash
$ npm run path/to/test.ts
```

#### Running the linter

Running the linter (eslint) over all `*.js`, `*.ts` and `*.vue` files:
```bash
$ npm run lint
```

Fixing linter problems on a specific file:
```bash
$ npm run format path/to/script.ts
```

Fixing problems for all files:
```bash
$ npm run format .
```

**Note:** when used with the `npm` script, the linter ignores all files and
directories that are ignored by `.gitignore` (eg. the `dist` folder).


#### Generating the license file

After installing new dependencies, the license generator needs to be run once and `/generated/licenses.json` commited. 
```bash
$ npm run generate:license-list
```


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
## How to add a new environment variable
Have a look at the readme of the orchestration repository [Link](https://gitlab.hzdr.de/hub-terra/sms/orchestration/-/blob/main/README.md#how-to-add-new-environment-variables-to-the-project)

# Installation

There are multiple ways to install the application. This document describes a [Compose](#compose),  
a [Docker](#docker) and a [Local](#local) installation. The preferred and easiest way to quickly get  
it running is [Compose](#compose). Once you finished the installation navigate to  
[http://localhost:5000/ping](http://localhost:5000/ping]) in your browser. You should see:

```json
{
"message": "Hallo Sensor ;)",
"status": "success"
}

```

## Dependencies

- Docker

There are so many technologies used mentioned in the tech specs and yet the dependencies just one, 
but This is the power of Docker.

## Compose

1. Start the containers and run them in background:

    ```bash
    docker-compose up -d
    ```

    This will take a few minutes the first time. Subsequent builds will be much faster since Docker caches
    the images once they are downloaded.

    You can watch the output of the containers witch `docker-compose logs`:

    ```bash
    docker-compose logs --follow 
    ```


2. When running the first time or when you have to cleanup the database:

    ```bash
    docker-compose exec app python manage.py recreate_db
    ```

## Docker

1. Build image

    ```bash
    docker build -t git.ufz.de:4567/rdm-software/svm/backend:`date +%Y-%m-%d`-1 \
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
         git.ufz.de:4567/rdm-software/svm/backend:latest \
         python manage.py recreate_db
    ```

4. Run the container

    ```bash
    docker run --rm -p 127.0.0.1:5000:5000 \
         -e DATABASE_URL="postgres://postgres:postgres@localhost:5432/db_dev" \
         -e APP_SETTINGS="project.config.DevelopmentConfig" \
         -e FLASK_DEBUG=1 \
         git.ufz.de:4567/rdm-software/svm/backend:latest
    ```

##  Local

To run the server local without docker, please execute the following from the app directory:

1. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Start development server:

    ```bash
    export FLASK_APP=project/__init__.py
    python manage.py run
    ```

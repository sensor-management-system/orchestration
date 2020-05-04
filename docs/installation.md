## Installation:


### Dependencies

- Docker

There are so many technologies used mentioned in the tech specs and yet the dependencies just one, 
but This is the power of Docker.

**Build the image**:

```
$ docker-compose -f docker-compose-dev.yml build
```

This will take a few minutes the first time. Subsequent builds will be much faster since Docker caches
the results of the first build. Once the build is done, fire up the container:

```
$ docker-compose -f docker-compose-dev.yml up -d
```
Navigate to:[http://localhost:5001/sis/v1/ping](http://localhost:5001/ping]) in your browser.

You should see:
```json
{
  "status": "success",
  "message": "Hello Sensor!",
  "jsonapi": {
    "version": "1.0"
  }
}
```

Apply the model to the dev database:
```
$ docker-compose -f docker-compose-dev.yml \
run app python manage.py recreate_db

```

To run the server without docker, please execute the following from the app directory:
Install the dependencies:

```
(env)$ pip install -r requirements.txt

```
then:

```
(env)$ export FLASK_APP=project/__init__.py
(env)$ python manage.py run
```

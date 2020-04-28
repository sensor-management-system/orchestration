# backend

This is the API of the REST service endpoints for managing sensor metadata.

### How to use 

Run the server:
```
(env)$ export FLASK_APP=project/__init__.py
(env)$ python manage.py run
```
Navigate to [http://localhost:5000/users/ping](http://localhost:5000/users/ping]) in your browser. 

You should see:
```json
{
"message": "Hallo Sensor ;)",
"status": "success"
}

```
### Run with Docker

Build the image:

```
$ docker-compose -f docker-compose-dev.yml build
```

This will take a few minutes the first time. Subsequent builds will be much faster since Docker caches
the results of the first build. Once the build is done, fire up the container:

```
$ docker-compose -f docker-compose-dev.yml up -d
```
Navigate to:[http://localhost:5001/users/ping](http://localhost:5001/ping]) in your browser.

Apply the model to the dev database:
```
$ docker-compose -f docker-compose-dev.yml \
run app python manage.py recreate_db

```
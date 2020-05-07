## Run the tests

### Dependencies 

- Docker

all used plugins you can find in the requirement file like:

- Flask-Testing
- unittest

### Test with CL

This registers a command, **test** , to the CLI so that we can run it from the command
line.
```
$ docker-compose exec app python manage.py test

```

### Code Quality

Checking the code for stylistic or programming errors.

```
$ docker-compose exec app flake8 project
```

### Code Coverage

Code coverage is the process of finding areas of the code not exercised by tests.

```
$ docker-compose exec app python manage.py cov

```
## Run the tests

### Dependencies 

- Docker

all used plugins you can find in the requirement file like:

- Flask-Testing
- unittest


This registers a command, **recreate_db** , to the CLI so that we can run it from the command
line. Apply the model to the dev database:
````
$ docker-compose -f docker-compose-dev.yml \
run users python manage.py recreate_db

````
### check the Database
````
$ docker exec -ti $(docker ps -aqf "name=users-db") psql -U postgres
````
````postgresql
# \c users_dev

You are now connected to database "db_dev" as user "postgres".
# \dt
        List of relations
 Schema |    Name    | Type  |  Owner   
--------+------------+-------+----------
 public | contact    | table | postgres
 public | device     | table | postgres
 public | event      | table | postgres
 public | platform   | table | postgres
 public | properties | table | postgres
(5 rows)

# \q
````

### Just run the test

With the containers up and running, run the tests:

```
$ docker-compose -f docker-compose-dev.yml \
run users python manage.py test
```

### Code Quality

Checking the code for stylistic or programming errors.

```
$ docker-compose -f docker-compose-dev.yml run app flake8 project
```

### Code Coverage

Code coverage is the process of finding areas of the code not exercised by tests.

```
$ docker-compose -f docker-compose-dev.yml \
run apps python manage.py cov

```
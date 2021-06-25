## Run the tests

### Dependencies

- Docker

all used plugins you can find in the requirement file like:

- Flask-Testing
- unittest

### Test with CL

This registers a command, **test** , to the CLI so that we can run it from the command line.

```
$ docker-compose exec app python manage.py test

```

### Code Quality & Linting

We are using [tox](https://tox.readthedocs.io/en/latest/) automation project to automate and
standardize linting in Python.

> tox is a generic virtualenv management and test command line tool you can use for:
>
>- checking that your package installs correctly with different Python versions and
   > interpreters
>
>- running your tests in each of the environments, configuring your test tool of choice
>
>- acting as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging
   > CI and shell-based testing.

What will be done in tox:

- [autoflake](https://github.com/myint/autoflake): autoflake removes unused imports and unused
  variables from Python code.
- [isort](https://github.com/PyCQA/isort): to sort the imports.
- [black](https://github.com/psf/black): as a Python code formatter.
- [flake8](https://gitlab.com/pycqa/flake8): to check the style and quality of some python code.

How to run tox:

```
$ docker-compose exec tox
```

### Code Coverage

Code coverage is the process of finding areas of the code not exercised by tests.

```
$ docker-compose exec app python manage.py cov

```
### Run only one test file

```
$ docker-compose exec app python manage.py test project.tests.test_esquerybuilder
```

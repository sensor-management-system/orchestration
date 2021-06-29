# API for Sensor Information System SIS 

[![pipeline status](https://registry.hzdr.de/hub-terra/sms/backend/badges/master/pipeline.svg)](https://registry.hzdr.de/hub-terra/sms/backend/commits/master)
[![version](https://img.shields.io/badge/version-v1.0-lightgrey.svg)](./README.md) [![python](https://img.shields.io/badge/python-3.5|3.6|3.7-blue.svg?style=?style=plastic&logo=python)](#)
[![pylint](https://img.shields.io/badge/lint%20score-9.97/10-yellowgreen.svg )](https://registry.hzdr.de/hub-terra/sms/backend/-/jobs?job=unittest-lint)
[![r_licenses](https://img.shields.io/badge/requirements_licenses-check-redyellow.svg?style=plastic&logo=open-source-initiative)](./docs/requirements_licenses.md)
[![openapi](https://img.shields.io/badge/OpenAPI-3.0-green.svg?style=?style=plastic&logo=openapi-initiative)](./app/openapi/openapi.yaml)
[![licences](https://img.shields.io/badge/licenses-MIT-green.svg?style=?style=plastic&logo=)](#)


RESTful API service in Python for managing sensor metadata using [flask](https://flask.palletsprojects.com/en/1.1.x/).

### Documentation

This Project uses OpenAPI to describe both the service model (the API in general, endpoints, request 
metadata like headers, authentication strategies, response metadata, etc.),
and it also covers the HTTP request/response body using a bunch of keywords
based on JSON Schema. 

[See the specs ](app/openapi/openapi.yaml)


### Technical Specs

- python 3.6+: Python Language supported and tested
- Flask: Micro Python Web Framework, good for microservice development and python WSGI apps.
- [OpenAPI](https://swagger.io/specification/) 3: specification to describe both the service model
- [Flask-REST-JSONAPI](https://flask-rest-jsonapi.readthedocs.io/en/latest/index.html): 
flask plugin for JSON Schema to describe an instance of JSON data, like the a HTTP request
 or response.
- [Docker](https://docs.docker.com/get-started/overview/): A containerization tool for better devops
- [Docker Compose](https://docs.docker.com/compose/): Tool for defining and running multi-container Docker applications


### Installation

You can choose between running the api with or without Docker.

[How to install](./docs/installation.md)


Note: For running elasticsearch it may be necessary to increase the maximal
map count for the virtual memory:

```
sudo sysctl vm.max_map_count=262144
```
### Usage

After having installed the dependencies, then just run the following commands to use it:

[Simple CRUD](docs/usage.md)

### Test

[How to run the tests](docs/test.md)

### Filter & Include & sort

[How to user filters](docs/filtering.md)



### Authors

- Martin Abbrent
- Kotyba Alhaj Taha
- Nils Brinckmann
- Marc Hanisch
- Dirk Pohle

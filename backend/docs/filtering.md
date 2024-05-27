<!--
SPDX-FileCopyrightText: 2020 - 2021
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Norman Ziegner <norman.ziegner@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

## Filtering
The filtering system is completely related to the data layer used by 
the ResourceList manager. In our case it will be the filtering interface for [SQLAlchemy](https://www.sqlalchemy.org/).


The filtering system of SQLAlchemy data layer has exactly the same interface as 
the filtering system of Flask-Restless. So this is a first example

````http
GET /platforms?filter=[{"name":"type","op":"eq","val":"test"}] HTTP/1.1
Accept: application/vnd.api+json

````

## Query format

`{"name": <fieldname>, "op": <operatorname>, "val": <argument>}`

or:

`{"name": <fieldname>, "op": <operatorname>, "field": <fieldname>}`

- name:	the name of the field you want to filter on
- op:	the operation you want to use (all sqlalchemy operations are available)
- val:	the value that you want to compare. You can replace this by 
“field” if you want to compare against the value of an other field

Common available operators:

- any: used to filter on to many relationships
- between: used to filter a field between two values
- endswith: check if field ends with a string
- eq: check if field is equal to something
- ge: check if field is greater than or equal to something
- gt: check if field is greater than to something
- has: used to filter on to one relationships
- ilike: check if field contains a string (case insensitive)
- in_: check if field is in a list of values
- is_: check if field is a value
- isnot: check if field is not a value
- like: check if field contains a string
- le: check if field is less than or equal to something
- lt: check if field is less than to something
- match: check if field match against a string or pattern
- ne: check if field is not equal to something
- notilike: check if field does not contains a string (case insensitive)
- notin_: check if field is not in a list of values
- notlike: check if field does not contains a string
- startswith: check if field starts with a string



You can also use boolean combination of operations:

`{"or": [<filterobject>, {"and": [<filterobject>, ...]}, ...]}`

__Example:__
```
/devices?filter=[{%22or%22:[{%22name%22:%22status_name%22,%22op%22:%22in_%22,%22val%22:[%22In%20Use%22]},{%22name%22:%22status_uri%22,%22op%22:%22in_%22,%22val%22:[%22/equipmentstatus/2/%22]}]}]
```
## Sparse fieldsets

You can restrict the fields returned by api with the querystring 
parameter called “`fields`”. It is very useful for performance purpose because 
fields not returned are not resolved by api. You can use “fields” parameter on 
any kind of route (classical CRUD route or 
relationships route) and any kind of http methods as long as method return data

Example:
````http
GET /devices?fields[device]=short_name HTTP/1.1
Accept: application/vnd.api+json
````
**Response**
````
{
  "data": [
    {
      "type": "device",
      "attributes": {
        "short_name": "test"
      },
      "id": "1",
      "links": {
        "self": "/rdm/svm-api/v1/devices/1"
      }
    }
  ],
  "links": {
    "self": "http://localhost:5000/rdm/svm-api/v1/devices?fields%5Bdevice%5D=short_name"
  },
  "meta": {
    "count": 1
  },
  "jsonapi": {
    "version": "1.0"
  }
}

````

## Sorting

You can sort results with querystring parameter named “sort”

__Example:__
```
GET /platforms?sort=short_name HTTP/1.1
Accept: application/vnd.api+json
```
### Multiple sort

````http
GET /persons?sort=short_name,type HTTP/1.1
Accept: application/vnd.api+json

````

### Descending sort

````http
GET /platforms?sort=-short_name HTTP/1.1
Accept: application/vnd.api+json
````
## Reference 
- [flask-rest-jsonapi filtering](https://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html)
- [query-format](https://flask-restless.readthedocs.io/en/stable/searchformat.html#query-format)
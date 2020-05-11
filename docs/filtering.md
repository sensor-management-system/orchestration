## Filtering
The filtering system is completely related to the data layer used by 
the ResourceList manager. In our case it will be the filtering interface for [SQLAlchemy]().


The filtering system of SQLAlchemy data layer has exactly the same interface as 
the filtering system of Flask-Restless. So this is a first example
````
GET /platforms?filter=[{"name":"type","op":"eq","val":"test"}] HTTP/1.1
Accept: application/vnd.api+json

````



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

## Include related objects

You can include related object(s) details to responses with the querystring 
parameter named “include”. You can use “include” parameter on
 any kind of route (classical CRUD route or relationships route) 
and any kind of http methods as long as method return data. 


```http request

POST http://localhost:5000/sis/v1/platforms?include=devices HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "platform",
    "attributes": {
        "description": "testParent",
        "shortName": "parent",
        "longName": "string",
        "manufacture": "parent_test",
        "type": "parenter"

    },
    "relationships": {
      "devices": {
        "data": [
          {
            "type": "device",
            "id": "1"
          }
        ]
      }
    }
  }
}
```
**Response**

````
HTTP/1.0 201 CREATED
Location: http://localhost:5000/sis/v1/platforms/1
Content-Type: application/vnd.api+json
Content-Length: 1745
Access-Control-Allow-Origin: https://git.ufz.de
Access-Control-Allow-Headers: Content-Type
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 08 May 2020 18:25:23 GMT

{
  "data": {
    "type": "platform",
    "attributes": {
      "description": "testParent",
      "longName": "string",
      "urn": "[PARENTER]_[PARENT]",
      "shortName": "parent",
      "platformType": null,
      "configurationDate": null,
      "manufacturer": null,
      "src": null,
      "type": "parenter",
      "inventoryNumber": null
    },
    "id": "1",
    "relationships": {
      "devices": {
        "links": {
          "self": "/sis/v1/platforms/1/relationships/devices",
          "related": "/sis/v1/platforms/1/devices"
        },
        "data": [
          {
            "type": "device",
            "id": "1"
          }
        ]
      }
    },
    "links": {
      "self": "/sis/v1/platforms/1"
    }
  },
  "links": {
    "self": "/sis/v1/platforms/1"
  },
  "included": [
    {
      "type": "device",
      "attributes": {
        "longName": "test_test",
        "urn": "[TEST]_[TEST]_[TEST]_[125436987]",
        "dualUse": "False",
        "persistentIdentifier": 54564654,
        "shortName": "test",
        "serialNumber": "125436987",
        "configurationDate": null,
        "inventoryNumber": 1122,
        "description": "test_test_test",
        "model": "test",
        "manufacture": "test",
        "label": "test",
        "type": "test"
      },
      "relationships": {
        "contacts": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/contacts",
            "related": "/sis/v1/devices/1/contacts"
          }
        },
        "platform": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/platform",
            "related": "/sis/v1/devices/1/platform"
          }
        },
        "events": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/events",
            "related": "/sis/v1/events?device_id=1"
          }
        },
        "properties": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/properties",
            "related": "/sis/v1/devices/1/contacts"
          }
        },
        "fields": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/fields",
            "related": "/sis/v1/devices/1/fields"
          }
        },
        "attachments": {
          "links": {
            "self": "/sis/v1/devices/1/relationships/attachments",
            "related": "/sis/v1/devices/1/attachments"
          }
        }
      },
      "id": "1",
      "links": {
        "self": "/sis/v1/devices/1"
      }
    }
  ],
  "jsonapi": {
    "version": "1.0"
  }
}


````
## Sparse fieldsets

You can restrict the fields returned by api with the querystring 
parameter called “`fields`”. It is very useful for performance purpose because 
fields not returned are not resolved by api. You can use “fields” parameter on 
any kind of route (classical CRUD route or 
relationships route) and any kind of http methods as long as method return data

Example:
````http request
GET http://localhost:5000/sis/v1/devices?fields[device]=urn HTTP/1.1
Accept: application/vnd.api+json
````
**Response**
````
{
  "data": [
    {
      "type": "device",
      "attributes": {
        "urn": "[TEST]_[TEST]_[TEST]_[125436987]"
      },
      "id": "1",
      "links": {
        "self": "/sis/v1/devices/1"
      }
    }
  ],
  "links": {
    "self": "http://localhost:5000/sis/v1/devices?fields%5Bdevice%5D=urn"
  },
  "meta": {
    "count": 1
  },
  "jsonapi": {
    "version": "1.0"
  }
}

````

# Sorting

You can sort results with querystring parameter named “sort”

**TBC**
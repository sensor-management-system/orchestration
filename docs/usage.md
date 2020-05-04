### Create object

Request:
```http request
POST http://localhost:5001/devices HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "device",
    "attributes": {
        "description": "test_test_test",
        "shortName": "short",
        "longName": "",
        "serialNumber": "0125436987",
        "manufacture": "manufacture",
        "model": "model",
        "inventoryNumber": "0001122",
        "persistentIdentifier": "54564654",
        "website": "###",
        "label": "LABEL",
        "type": "TYPE"
    }
  }
}
```
Response:

```

HTTP/1.1 201 Created
Content-Type: application/vnd.api+json
{
  "data": {
    "type": "device",
    "attributes": {
      "shortName": "short",
      "serialNumber": "125436987",
      "urn": "[MANUFACTURE]_[MODEL]_[TYPE]_[125436987]",
      "manufacture": "manufacture",
      "website": "###",
      "dualUse": "False",
      "configurationDate": null,
      "persistentIdentifier": 54564654,
      "inventoryNumber": 1122,
      "model": "model",
      "longName": "",
      "label": "LABEL",
      "description": "test_test_test",
      "type": "TYPE"
    },
    "relationships": {
      "platform": {
        "links": {
          "self": "/devices/4/relationships/platform",
          "related": "/devices/4/platform"
        }
      },
      "events": {
        "links": {
          "self": "/devices/4/relationships/events",
          "related": "/events?device_id=4"
        }
      },
      "contacts": {
        "links": {
          "self": "/devices/4/relationships/contacts",
          "related": "/contacts?device_id=4"
        }
      }
    },
    "id": "4",
    "links": {
      "self": "/devices/4"
    }
  },
  "links": {
    "self": "/devices/4"
  },
  "jsonapi": {
    "version": "1.0"
  }
}

```

### Update object and his relationships

Request:

```http request
PATCH http://localhost:5001/devices/1 HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "device",
    "id": "1",
    "attributes": {
      "shortName": "updated"
    }
  }
}

```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
  "data": {
    "type": "device",
    "attributes": {
      "shortName": "updated",
      "serialNumber": "125436987",
      "urn": "[MANUFACTURE]_[MODEL]_[TYPE]_[125436987]",
      "manufacture": "manufacture",
      "website": "###",
      "dualUse": "False",
      "configurationDate": null,
      "persistentIdentifier": 54564654,
      "inventoryNumber": 1122,
      "model": "model",
      "longName": "",
      "label": "LABEL",
      "description": "test_test_test",
      "type": "TYPE"
    },
    "relationships": {
      "platform": {
        "links": {
          "self": "/devices/1/relationships/platform",
          "related": "/devices/1/platform"
        }
      },
      "events": {
        "links": {
          "self": "/devices/1/relationships/events",
          "related": "/events?device_id=1"
        }
      },
      "contacts": {
        "links": {
          "self": "/devices/1/relationships/contacts",
          "related": "/contacts?device_id=1"
        }
      }
    },
    "id": "1",
    "links": {
      "self": "/devices/1"
    }
  },
  "links": {
    "self": "/devices/1"
  },
  "jsonapi": {
    "version": "1.0"
  }
}

```
### Create relationship

Request:
```http request
POST http://localhost:5001/platforms/1/relationships/devices HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": [
    {
      "type": "device",
      "id": "1"
    }
  ]
}
```
Response:

```
HTTP/1.0 200 OK
Content-Type: application/vnd.api+json

{
  "meta": {
    "message": "Relationship successfully created"
  },
  "jsonapi": {
    "version": "1.0"
  }
}
```
### Delete relationship

```http request
DELETE http://localhost:5001/platforms/1/relationships/devices HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": [
    {
      "type": "device",
      "id": "1"
    }
  ]
}
```
Response:

```
HTTP/1.0 200 OK
Content-Type: application/vnd.api+json

{
  "meta": {
    "message": "Relationship successfully updated"
  },
  "jsonapi": {
    "version": "1.0"
  }
}

```

### related and 

You add the querystring parameter “include” to the url to add or Update relationships 

```http request
POST http://localhost:5001/platforms?include= HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "platform",
    "attributes": {
        "description": "blah blah ",
        "shortName": "short",
        "longName": "long name",
        "manufacturer": "manufacturer",
        "inventoryNumber": "0001122",
        "persistentIdentifier": "54564654",
        "website": "###",
        "platformType": "testType",
        "type": "test"

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

### Multiple related resources

Multiple related resources can be requested in a comma-separated list

#### GET 

```http request
GET http://localhost:5001/devices/1?include=platform,events,contacts HTTP/1.1
Accept: application/vnd.api+json
``` 

#### POST

```http request
POST http://localhost:5001/devices?include=events,contacts HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "device",
    "attributes": {
        "serialNumber": "0125436987",
         "manufacture": "manufacture",
         "model": "model",
         "inventoryNumber": "0001122",
         "persistentIdentifier": "54564654",
         "type": "TYPE"

    },
    "relationships": {

      "contact": {
        "data": [
          {
            "type": "contact",
            "id": "1"
          }
        ]
      },
      "event": {
        "data": [
          {
            "type": "event",
            "id": "1"
          }
        ]
      }
    }
  }
}
```

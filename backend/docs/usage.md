<!--
SPDX-FileCopyrightText: 2020 - 2021
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: HEESIL-1.0
-->

# CRUD operations

To take a deeper look into the api-operations please visit the 
[Swagger 2.0](../app/project/static/swager.json)
sites.

## List objects

__Request:__

```http
GET /devices HTTP/1.1
Accept: application/vnd.api+json
```
__Response:__

```json
{
  "data": [
    {
      "attributes": {
        "created_at": "0001-00-00T00:00:00.000000",
        "updated_at": "0001-00-00T00:00:00.000000",
        "description": "",
        "short_name": "",
        "long_name": "",
        "serial_number": "",
        "manufacturer_uri": "",
        "manufacturer_name": "",
        "dual_use": false,
        "model": "",
        "inventory_number": "",
        "persistent_identifier": null,
        "website": "",
        "device_type_uri": "",
        "device_type_name": "",
        "status_uri": "",
        "status_name": ""
      },
      "type": "device",
      "id": "0",
      "relationships": {
        "customfields": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_properties": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "events": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_attachments": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_calibration_actions": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "configuration_device": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "contacts": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "generic_device_actions": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_mount_actions": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_software_update_actions": {
          "data": [],
          "links": {
            "self": null
          }
        },
        "device_unmount_actions": {
          "data": [],
          "links": {
            "self": null
          }
        }
      }
    }
  ]
}
```
## Create object

__Request:__
```http
POST /devices HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "attributes": {
      "description": "",
      "short_name": "TEST",
      "long_name": "",
      "serial_number": "",
      "manufacturer_uri": "",
      "manufacturer_name": "",
      "dual_use": false,
      "model": "",
      "inventory_number": "",
      "persistent_identifier": null,
      "website": "",
      "device_type_uri": "",
      "device_type_name": "",
      "status_uri": "",
      "status_name": ""
    },
    "relationships": {},
    "id": "0",
    "type": "device"
  }
}
```
__Response:__

```json

HTTP/1.1 201 Created
Content-Type: application/vnd.api+json
{
  "data": {
    "attributes": {
      "description": "",
      "short_name": "TEST",
      "long_name": "",
      "serial_number": "",
      "manufacturer_uri": "",
      "manufacturer_name": "",
      "dual_use": false,
      "model": "",
      "inventory_number": "",
      "persistent_identifier": null,
      "website": "",
      "device_type_uri": "",
      "device_type_name": "",
      "status_uri": "",
      "status_name": ""
    },
    "relationships": {},
    "id": "1",
    "type": "device"
  }
}


```

## Update object

__Request:__

```http
PATCH /devices/1 HTTP/1.1
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

__Response:__

```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
  "data": {
    "attributes": {
      "description": "",
      "short_name": "updated",
      "long_name": "",
      "serial_number": "",
      "manufacturer_uri": "",
      "manufacturer_name": "",
      "dual_use": false,
      "model": "",
      "inventory_number": "",
      "persistent_identifier": null,
      "website": "",
      "device_type_uri": "",
      "device_type_name": "",
      "status_uri": "",
      "status_name": ""
    },
    "relationships": {},
    "id": "1",
    "type": "device"
  }
}

```
## Delete object

__Request:__
```http
DELETE /devices/1 HTTP/1.1
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

__Response:__

```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json

{
  "meta": {
    "message": "Object successfully deleted"
  },
  "jsonapi": {
    "version": "1.0"
  }
}

```
## Relationships

### Create relationship

There are two ways to create a relationship in a JSON:API. The first one directly as we create the 
object, which we want to make the relation with. Or using the endpoint associated to this relationship.  
#### The First Methode 
We just add the querystring parameter `include` to the url and extend the payload as follows:

__Request:__

```http
POST /devices?include=contacts HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "device",
    "attributes": {
      "short_name": "test device",
    },
    "relationships": {
      "contacts": {
        "data": [
          {
            "type": "contact",
            "id": "1"
          }
        ]
      }
    }
  }
}
```

__Response:__

```json
HTTP/1.1 201 Created
Content-Type: application/vnd.api+json
{
  "data": {
    "type": "device",
    "attributes": {
     "description": "",
      "short_name": "test device",
      "long_name": "",
      "serial_number": "",
      "manufacturer_uri": "",
      "manufacturer_name": "",
      "dual_use": false,
      "model": "",
      "inventory_number": "",
      "persistent_identifier": null,
      "website": "",
      "device_type_uri": "",
      "device_type_name": "",
      "status_uri": "",
      "status_name": ""
    },
    "relationships": {
      "platform": {
        "links": {
          "self": "/devices/4/relationships/platform",
          "related": "/devices/4/platform"
        }
      },
      "contacts": {
        "links": {
          "self": "/devices/3/relationships/contacts",
          "related": "/contacts?device_id=3"
        }
      }
    }
    included": [
   {
      "type": "contact",
      "id": "1",
      "relationships": {
        "devices": {
          "links": {
            "related": "/rdm/svm-api/v1/contacts/1/relationships/devices"
          },
          "data": [
            {
              "type": "device",
              "id": "1"
            },
            {
              "type": "device",
              "id": "2"
            }
          ]
        },
        "user": {
          "links": {
            "self": "/rdm/svm-api/v1/contacts/1/relationships/user"
          },
          "data": {
            "type": "user",
            "id": "1"
          }
        },
        "platforms": {
          "links": {
            "related": "/rdm/svm-api/v1/contacts/1/relationships/platforms"
          },
          "data": [
            {
              "type": "platform",
              "id": "1"
            }
          ]
        },
        "configurations": {
          "links": {
            "related": "/rdm/svm-api/v1/contacts/1/relationships/configurations"
          },
          "data": [
            {
              "type": "configuration",
              "id": "1"
            }
          ]
        }
      },
      "attributes": {
        "family_name": "user",
        "website": null,
        "email": "user@ufz.de",
        "given_name": "user"
      },
      "links": {
        "self": "/rdm/svm-api/v1/contacts/1"
      }
    }
    ],
    "id": "3",
    "links": {
      "self": "/devices/3"
    }
  },
  "links": {
    "self": "/devices/3"
  },
  "jsonapi": {
    "version": "1.0"
  }
}

```
#### The second Methode

__Request:__

```http
POST /device/1/relationships/contacts HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": [
    {
      "type": "contact",
      "id": "2"
    }
  ]
}
```
__Response:__

```json
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

```http
DELETE /devices/1/relationships/contacts HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": [
    {
      "type": "contact",
      "id": "2"
    }
  ]
}
```
__Response:__

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

## References:

- [flask-rest-jsonapi](https://flask-rest-jsonapi.readthedocs.io/en/latest/quickstart.html)
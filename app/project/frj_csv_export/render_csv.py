"""Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi )"""
from csv import DictWriter
from io import StringIO

from flask import make_response


def flatten_json(y):
    """

      :param y: json_response
      :return: dict

    Returned values looks like that
      {
        'data.0.type': 'device',
        'data.0.attributes.short_name': 'device1',
        'data.0.attributes.device_type_uri': None,
        'data.0.attributes.long_name': None,
        'data.0.attributes.updated_at': None,
        'data.0.attributes.website': None,
        'data.0.attributes.dual_use': None,
        'data.0.attributes.manufacturer_name': None,
        'data.0.attributes.description': None,
        'data.0.attributes.serial_number': None,
        'data.0.attributes.model': None,
        'data.0.attributes.device_type_name': None,
        'data.0.attributes.inventory_number': None,
        'data.0.attributes.status_name': None,
        'data.0.attributes.persistent_identifier': None,
        'data.0.attributes.created_at': None,
        'data.0.attributes.properties.0.measuring_range_max': 1,
        'data.0.attributes.properties.0.resolution_unit_uri': None,
        'data.0.attributes.properties.0.unit_uri': None,
        'data.0.attributes.properties.0.compartment_name': None,
        'data.0.attributes.properties.0.sampling_media_name': None,
        'data.0.attributes.properties.0.measuring_range_min': 0,
        'data.0.attributes.properties.0.property_name': None,
        'data.0.attributes.properties.0.failure_value': 9999,
        'data.0.attributes.properties.0.compartment_uri': None,
        'data.0.attributes.properties.0.sampling_media_uri': None,
        'data.0.attributes.properties.0.label': None,
        'data.0.attributes.properties.0.resolution': None,
        'data.0.attributes.properties.0.resolution_unit_name': None,
        'data.0.attributes.properties.0.property_uri': None,
        'data.0.attributes.properties.0.id': '1',
        'data.0.attributes.properties.0.accuracy': None,
        'data.0.attributes.properties.0.unit_name': None,
        'data.0.attributes.manufacturer_uri': None,
        'data.0.attributes.status_uri': None,
        'data.0.relationships.created_by.links.self':
                    '/rdm/svm-api/v1/devices/1/relationships/createdUser',
        'data.0.relationships.updated_by.links.self':
                    '/rdm/svm-api/v1/devices/1/relationships/updatedUser',
        'data.0.relationships.events.links.self':
                    '/rdm/svm-api/v1/devices/1/relationships/events',
        'data.0.relationships.events.links.related':
                    '/rdm/svm-api/v1/events?device_id=1',
        'data.0.relationships.contacts.links.self':
                    '/rdm/svm-api/v1/devices/1/relationships/contacts',
        'data.0.relationships.contacts.links.related':
                    '/rdm/svm-api/v1/devices/1/contacts',
        'data.0.id': '1',
        'data.0.links.self': '/rdm/svm-api/v1/devices/1',
        'links.self': 'http://localhost:5000/rdm/svm-api/v1/devices',
        'meta.count': 3,
        'jsonapi.version': '1.0'
      }
    """
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for key, val in x.items():
                flatten(val, name + key + ".")
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + ".")
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def render_csv(response):
    data = response["data"]
    # Treat single values as a list of one element
    if not isinstance(data, list):
        data = [data]

    # Flatten the list of rows
    rows = []
    fields = set()
    for row in data:
        flattened = flatten_json(row)
        rows.append(flattened)
        fields.update(flattened.keys())

    # Write the rows to CSV
    with StringIO() as out:
        writer = DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        return make_response(out.getvalue(), 200, {"Content-Type": "text/csv"})

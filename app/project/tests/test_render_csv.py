import json
import csv
from collections import defaultdict

from project.frj_csv_export.render_csv import flatten_json

from project.tests.base import BaseTestCase

from project.urls import base_url

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema


class Test(BaseTestCase):
    device_url = base_url + '/devices'

    def test_flatten_json(self):
        """Ensure that the flatten_json gives the exact result as we want"""
        sensor = Device(id=22,
                        short_name='device_short_name test',
                        description="device_description test",
                        long_name='device_long_name test',
                        manufacturer_name='manufacturer_name test',
                        manufacturer_uri='http://cv/manufacturer_uri',
                        model='device_model test',
                        dual_use=True,
                        serial_number='device_serial_number test',
                        website='http://website/device',
                        inventory_number='inventory_number test',
                        persistent_identifier='persistent_identifier_test')
        DeviceSchema().dump(sensor)
        db.session.add(sensor)
        db.session.commit()
        response = self.client.get(self.device_url)
        data = json.loads(response.data.decode())
        fj = flatten_json(data)
        expected = {'data.type': 'device', 'data.attributes.website': 'http://website/device',
                    'data.attributes.device_type_name': None,
                    'data.attributes.device_type_uri': None,
                    'data.attributes.persistent_identifier': 'persistent_identifier_test',
                    'data.attributes.updated_at': '2020-12-18T10:11:59.432624',
                    'data.attributes.long_name': 'device_long_name test',
                    'data.attributes.short_name': 'device_short_name test',
                    'data.attributes.inventory_number': 'inventory_number test',
                    'data.attributes.manufacturer_name': 'manufacturer_name test',
                    'data.attributes.dual_use': True,
                    'data.attributes.created_at': '2020-12-18T10:11:59.432624',
                    'data.attributes.description': 'device_description test',
                    'data.attributes.manufacturer_uri': 'http://cv/manufacturer_uri',
                    'data.attributes.status_uri': None,
                    'data.attributes.model': 'device_model test',
                    'data.attributes.serial_number': 'device_serial_number test',
                    'data.attributes.status_name': None,
                    'data.relationships.contacts.links.self': '/rdm/svm-api/v1/devices/22/relationships/contacts',
                    'data.relationships.contacts.links.related': '/rdm/svm-api/v1/devices/22/contacts',
                    'data.relationships.updated_by.links.self': '/rdm/svm-api/v1/devices/22/relationships/updatedUser',
                    'data.relationships.events.links.self': '/rdm/svm-api/v1/devices/22/relationships/events',
                    'data.relationships.events.links.related': '/rdm/svm-api/v1/events?device_id=22',
                    'data.relationships.created_by.links.self': '/rdm/svm-api/v1/devices/22/relationships/createdUser',
                    'data.id': '22', 'data.links.self': '/rdm/svm-api/v1/devices/22',
                    'links.self': 'http://localhost/rdm/svm-api/v1/devices', 'meta.count': 1,
                    'jsonapi.version': '1.0'}
        self.assertEqual(fj['data.attributes.short_name'],
                         expected['data.attributes.short_name'])
        self.assertCountEqual(fj, expected)

    def test_csv_response(self):
        """Ensure csv Export works"""
        super(Test, self).tearDown()
        super(Test, self).setUp()
        sensor1 = Device(id=22,
                         short_name='device_short_name test',
                         description="device_description test",
                         long_name='device_long_name test',
                         manufacturer_name='manufacturer_name test',
                         manufacturer_uri='http://cv/manufacturer_uri',
                         model='device_model test',
                         dual_use=True,
                         serial_number='device_serial_number test',
                         website='http://website/device',
                         inventory_number='inventory_number test',
                         persistent_identifier='persistent_identifier_test')
        DeviceSchema().dump(sensor1)
        db.session.add(sensor1)
        db.session.commit()
        sensor2 = Device(id=33,
                         short_name='device_short_name test2',
                         description="device_description test2",
                         long_name='device_long_name test2',
                         manufacturer_name='manufacturer_name test2',
                         manufacturer_uri='http://cv/manufacturer_uri2',
                         model='device_model test2',
                         dual_use=False,
                         serial_number='device_serial_number test2',
                         website='http://website/device2',
                         inventory_number='inventory_number test2',
                         persistent_identifier='persistent_identifier_test2')
        DeviceSchema().dump(sensor2)
        db.session.add(sensor2)
        db.session.commit()
        response = self.client.get(self.device_url, headers={
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'text/csv'
        })
        # print(response.data.decode())
        # still need to be converted to dict WIP
        # rows = list(DictReader(response.data.decode().split()))
        # Since we used sensor1 and sensor2, there should be 2 rows
        # assert len(rows) == 2
        # The names should be in the dictionary
        # names = set([row['attributes.short_name'] for row in rows])
        # print(names)
        # assert 'device_short_name test' in names
        # assert 'device_short_name test2' in names

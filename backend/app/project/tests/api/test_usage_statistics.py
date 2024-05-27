# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the usage statistics."""

import datetime

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationAttachment,
    Contact,
    DatastreamLink,
    Device,
    DeviceAttachment,
    DeviceMountAction,
    DeviceProperty,
    Platform,
    PlatformAttachment,
    Site,
    SiteAttachment,
    TsmEndpoint,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestUsageStatistics(BaseTestCase):
    """Test class for the usage statistics."""

    url = base_url + "/usage-statistics"

    def test_get_empty(self):
        """Test with just the empty db."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_post_not_allowed(self):
        """Test that we can not post."""
        response = self.client.post(self.url, content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, 405)

    def test_get_one_device(self):
        """Test the counts with one device."""
        device = Device(short_name="first device")
        db.session.add(device)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 1,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_platform(self):
        """Test the count with one platform."""
        platform = Platform(short_name="first platform")
        db.session.add(platform)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 1,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_configuration(self):
        """Test the count with one configuration."""
        configuration = Configuration(label="first configuration")
        db.session.add(configuration)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 1,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_user(self):
        """Test the count with one user."""
        contact = Contact(given_name="N", family_name="B", email="nb@localhost")
        user = User(subject="nb", contact=contact)
        db.session.add_all([contact, user])
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 1,
                "sites": 0,
            },
        )

    def test_ensure_that_user_must_be_active(self):
        """Test that we don't list inactive users anymore."""
        contact = Contact(given_name="N", family_name="B", email="nb@localhost")
        user = User(subject="nb", contact=contact, active=False)
        db.session.add_all([contact, user])
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_site(self):
        """Test the count with one site."""
        site = Site(label="Site", is_internal=True, is_public=False)
        db.session.add(site)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 1,
            },
        )

    def test_get_mixed(self):
        """Test the counts with some data for various models."""
        device1 = Device(short_name="first device")
        device2 = Device(short_name="second device")
        device3 = Device(short_name="third device")
        device4 = Device(short_name="fourth device")
        platform1 = Platform(short_name="first platform")
        platform2 = Platform(short_name="second platform")
        platform3 = Platform(short_name="third platform")
        configuration1 = Configuration(label="first configuration")
        configuration2 = Configuration(label="second configuration")
        contact = Contact(given_name="N", family_name="B", email="nb@localhost")
        user = User(subject="nb", contact=contact)
        site1 = Site(label="Site1", is_internal=True, is_public=False)
        site2 = Site(label="Site2", is_internal=False, is_public=True)
        db.session.add_all(
            [
                device1,
                device2,
                device3,
                device4,
                platform1,
                platform2,
                platform3,
                configuration1,
                configuration2,
                contact,
                user,
                site1,
                site2,
            ]
        )
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 4,
                "platforms": 3,
                "configurations": 2,
                "users": 1,
                "sites": 2,
            },
        )

    def test_extended(self):
        """Ensure we can query for more data if we ask for."""
        response = self.client.get(self.url + "?extended=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
                "organizations": 0,
                "device_pids": 0,
                "platform_pids": 0,
                "configuration_pids": 0,
                "pids": 0,
                "uploads": 0,
                "orcids": 0,
                "datastreams": 0,
            },
        )

    def test_organization_count_is_bound_to_active_users(self):
        """Ensure we use organizations only if we have an active user."""
        contact1 = Contact(
            given_name="giv",
            family_name="fam",
            email="giv.gfam@abc.corp",
            organization="ABC Corp",
        )
        db.session.add(contact1)
        db.session.commit()

        response1 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json
        self.assertEqual(data1["counts"]["organizations"], 0)

        user1 = User(subject=contact1.email, contact=contact1)
        db.session.add(user1)
        db.session.commit()

        response2 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json
        self.assertEqual(data2["counts"]["organizations"], 1)

        user1.active = False
        db.session.add(user1)
        db.session.commit()

        response3 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response3.status_code, 200)
        data3 = response3.json
        self.assertEqual(data3["counts"]["organizations"], 0)

    def test_distinct_organizations(self):
        """Ensure that we count only how many distinct organizations there are."""
        contact1 = Contact(
            given_name="giv",
            family_name="fam",
            email="giv.gfam@abc.corp",
            organization="ABC Corp",
        )
        contact2 = Contact(
            given_name="giv",
            family_name="fam",
            email="giv.gfam@boo.corp",
            organization="Boo Corp",
        )
        contact3 = Contact(
            given_name="next",
            family_name="fam",
            email="next.gfam@boo.corp",
            organization="Boo Corp",
        )

        user1 = User(subject=contact1.email, contact=contact1)
        user2 = User(subject=contact2.email, contact=contact2)
        user3 = User(subject=contact3.email, contact=contact3)

        db.session.add_all([contact1, contact2, contact3, user1, user2, user3])
        db.session.commit()

        response = self.client.get(self.url + "?extended=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["counts"]["organizations"], 2)

    def test_pids_are_added(self):
        """Ensure we include devices, platforms and configs for the pid count."""
        device1 = Device(
            short_name="Dev1", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(device1)
        db.session.commit()

        response1 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json
        self.assertEqual(data1["counts"]["pids"], 0)
        self.assertEqual(data1["counts"]["device_pids"], 0)

        device2 = Device(
            short_name="Dev2",
            is_public=True,
            is_internal=False,
            is_private=False,
            persistent_identifier="11111/11111111111",
        )
        db.session.add(device2)
        db.session.commit()

        response2 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json
        self.assertEqual(data2["counts"]["pids"], 1)
        self.assertEqual(data2["counts"]["device_pids"], 1)

        platform1 = Platform(
            short_name="Pla1", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(platform1)
        db.session.commit()

        response3 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response3.status_code, 200)
        data3 = response3.json
        self.assertEqual(data3["counts"]["pids"], 1)
        self.assertEqual(data3["counts"]["platform_pids"], 0)

        platform2 = Platform(
            short_name="Pla2",
            is_public=True,
            is_internal=False,
            is_private=False,
            persistent_identifier="22222/222222222",
        )
        db.session.add(platform2)
        db.session.commit()

        response4 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response4.status_code, 200)
        data4 = response4.json
        self.assertEqual(data4["counts"]["pids"], 2)
        self.assertEqual(data4["counts"]["platform_pids"], 1)

        configuration1 = Configuration(label="Conf1", is_public=True)
        db.session.add(configuration1)
        db.session.commit()

        response5 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response5.status_code, 200)
        data5 = response5.json
        self.assertEqual(data5["counts"]["pids"], 2)
        self.assertEqual(data5["counts"]["configuration_pids"], 0)

        configuration2 = Configuration(
            label="Conf2", is_public=True, persistent_identifier="33333/33333333"
        )
        db.session.add(configuration2)
        db.session.commit()

        response6 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response6.status_code, 200)
        data6 = response6.json
        self.assertEqual(data6["counts"]["pids"], 3)
        self.assertEqual(data6["counts"]["configuration_pids"], 1)

    def test_uploads(self):
        """Ensure we sum up the uploaded attachments."""
        device1 = Device(
            short_name="Dev1", is_public=True, is_internal=False, is_private=False
        )
        platform1 = Platform(
            short_name="Pla1", is_public=True, is_internal=False, is_private=False
        )
        configuration1 = Configuration(label="Conf1", is_public=True)
        site1 = Site(label="Site1", is_public=True)
        db.session.add_all([device1, platform1, configuration1, site1])
        db.session.commit()

        response1 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json
        self.assertEqual(data1["counts"]["uploads"], 0)

        device_attachment1 = DeviceAttachment(
            device=device1,
            internal_url="http://internal.somewhere",
            url="https://somwhere",
            label="something",
        )
        db.session.add(device_attachment1)
        db.session.commit()

        response2 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json
        self.assertEqual(data2["counts"]["uploads"], 1)

        platform_attachment1 = PlatformAttachment(
            platform=platform1,
            internal_url="http://internal.somewhere",
            url="https://somwhere",
            label="something",
        )
        db.session.add(platform_attachment1)
        db.session.commit()

        response3 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response3.status_code, 200)
        data3 = response3.json
        self.assertEqual(data3["counts"]["uploads"], 2)

        configuration_attachment1 = ConfigurationAttachment(
            configuration=configuration1,
            internal_url="http://internal.somewhere",
            url="https://somwhere",
            label="something",
        )
        db.session.add(configuration_attachment1)
        db.session.commit()

        response4 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response4.status_code, 200)
        data4 = response4.json
        self.assertEqual(data4["counts"]["uploads"], 3)

        site_attachment1 = SiteAttachment(
            site=site1,
            internal_url="http://internal.somewhere",
            url="https://somwhere",
            label="something",
        )
        db.session.add(site_attachment1)
        db.session.commit()

        response5 = self.client.get(self.url + "?extended=true")
        self.assertEqual(response5.status_code, 200)
        data5 = response5.json
        self.assertEqual(data5["counts"]["uploads"], 4)

    def test_orcics(self):
        """Ensure we return the number of orcids."""
        contact = Contact(
            given_name="x", family_name="y", email="x@y.z", orcid="1234-5678-9012-3456"
        )
        db.session.add(contact)
        db.session.commit()

        response = self.client.get(self.url + "?extended=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["counts"]["orcids"], 1)

    def test_datastreams(self):
        """Ensure we count how many datastreams are linked."""
        tsm_endpoint = TsmEndpoint(url="http://somwhere", name="Somewhere")

        device1 = Device(
            short_name="Dev1", is_public=True, is_internal=False, is_private=False
        )
        device_property1 = DeviceProperty(device=device1, property_name="Temperature")
        configuration1 = Configuration(label="Conf1", is_public=True)
        contact1 = Contact(
            given_name="x", family_name="y", email="x@y.z", orcid="1234-5678-9012-3456"
        )
        mount1 = DeviceMountAction(
            device=device1,
            configuration=configuration1,
            begin_date=datetime.datetime(2023, 1, 1, 0, 0, 0),
            begin_contact=contact1,
        )

        datastream_link1 = DatastreamLink(
            device_property=device_property1,
            device_mount_action=mount1,
            tsm_endpoint=tsm_endpoint,
            datasource_id="d1",
            thing_id="t1",
            datastream_id="s1",
        )

        db.session.add_all(
            [
                tsm_endpoint,
                device1,
                configuration1,
                contact1,
                mount1,
                device_property1,
                datastream_link1,
            ]
        )
        db.session.commit()

        response = self.client.get(self.url + "?extended=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["counts"]["datastreams"], 1)

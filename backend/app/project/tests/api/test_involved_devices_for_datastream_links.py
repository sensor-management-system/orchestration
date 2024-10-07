#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


"""Tests for the involved devices for datastream links."""

import datetime
import json
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    DatastreamLink,
    Device,
    DeviceMountAction,
    DeviceProperty,
    InvolvedDeviceForDatastreamLink,
    TsmEndpoint,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, Fixtures

fixtures = Fixtures()


@fixtures.register("right_group")
def create_right_group():
    """Create a permission group for the devices and configurations."""
    return "1"


@fixtures.register("wrong_group")
def create_wrong_group():
    """Create another permission group for the devices and configurations."""
    return "2"


@fixtures.register("super_user_contact", scope=lambda: db.session)
def create_super_user_contact():
    """Create a contact that can be used to make a super user."""
    result = Contact(
        given_name="super", family_name="contact", email="super.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user", scope=lambda: db.session)
@fixtures.use(["super_user_contact"])
def create_super_user(super_user_contact):
    """Create super user to use it in the tests."""
    result = User(
        contact=super_user_contact, subject=super_user_contact.email, is_superuser=True
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_smt_100", scope=lambda: db.session)
@fixtures.use(["right_group"])
def create_public_smt_100(right_group):
    """Create a public device that is used for soil moisture measurements."""
    result = Device(
        short_name="SMT 100",
        is_public=True,
        is_internal=False,
        is_private=False,
        group_ids=[right_group],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("soil_moisture_of_public_smt_100", scope=lambda: db.session)
@fixtures.use(["public_smt_100"])
def create_soil_moisture_of_public_smt_100(public_smt_100):
    """Create the measured quantity for the soil moisture measurement."""
    result = DeviceProperty(device=public_smt_100, property_name="Soil moisture")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_cr_1000", scope=lambda: db.session)
@fixtures.use(["right_group"])
def create_public_cr_1000(right_group):
    """Create a public device that is used as a data logger."""
    result = Device(
        short_name="CR 1000",
        is_public=True,
        is_internal=False,
        is_private=False,
        group_ids=[right_group],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_configuration", scope=lambda: db.session)
@fixtures.use(["right_group"])
def create_public_configuration(right_group):
    """Create a public configuration."""
    result = Configuration(
        label="public configuration",
        is_public=True,
        is_internal=False,
        cfg_permission_group=right_group,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("smt_100_mount", scope=lambda: db.session)
@fixtures.use(["public_smt_100", "public_configuration", "contact1"])
def create_smt_100_mount(public_smt_100, public_configuration, contact1):
    """Create the mount for the smt 100 device."""
    result = DeviceMountAction(
        device=public_smt_100,
        configuration=public_configuration,
        begin_contact=contact1,
        begin_date=datetime.datetime(2010, 1, 1, 12, 0, 0),
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("cr_1000_mount", scope=lambda: db.session)
@fixtures.use(["public_cr_1000", "public_configuration", "contact1"])
def create_cr_1000_mount(public_cr_1000, public_configuration, contact1):
    """Create the mount for the cr 1000 device."""
    result = DeviceMountAction(
        device=public_cr_1000,
        configuration=public_configuration,
        begin_contact=contact1,
        begin_date=datetime.datetime(2010, 1, 1, 12, 0, 0),
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("tsm_endpoint", scope=lambda: db.session)
def create_tsm_endpoint():
    """Create a tsm endpoint."""
    result = TsmEndpoint(url="http://localhost", name="localhost")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("soil_moisture_datastream_link", scope=lambda: db.session)
@fixtures.use(["tsm_endpoint", "soil_moisture_of_public_smt_100", "smt_100_mount"])
def create_soil_moisture_datastream_link(
    tsm_endpoint, soil_moisture_of_public_smt_100, smt_100_mount
):
    """Create a datastream link for the soil moisture measurement."""
    result = DatastreamLink(
        device_property=soil_moisture_of_public_smt_100,
        device_mount_action=smt_100_mount,
        tsm_endpoint=tsm_endpoint,
        datasource_id=1,
        thing_id=2,
        datastream_id=3,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "cr_1000_involvement_for_soil_moisture_datastream_link", scope=lambda: db.session
)
@fixtures.use(["soil_moisture_datastream_link", "cr_1000_mount"])
def create_cr_1000_involvement_for_soil_moisture_datastream_link(
    soil_moisture_datastream_link, cr_1000_mount
):
    """Create the entry for the involvement of the cr 1000 in the soil moisture measurement."""
    result = InvolvedDeviceForDatastreamLink(
        datastream_link=soil_moisture_datastream_link,
        device=cr_1000_mount.device,
        order_index=123,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestInvolvedDeviecsForDatastreamLinks(BaseTestCase):
    """Test class for the involved devices for datastream links."""

    url = base_url + "/involved-devices-for-datastream-links"

    def test_get_list_empty(self):
        """Ensure we can get an empty list of there is no data."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_public_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can list public information even without a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        actual_data = resp.json["data"]

        self.assertEqual(
            actual_data[0]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )
        self.assertEqual(actual_data[0]["type"], "involved_device_for_datastream_link")
        self.assertEqual(
            actual_data[0]["attributes"]["order_index"],
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index,
        )
        self.assertEqual(
            actual_data[0]["relationships"]["datastream_link"]["data"]["id"],
            str(
                cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
            ),
        )
        self.assertEqual(
            actual_data[0]["relationships"]["datastream_link"]["data"]["type"],
            "datastream_link",
        )
        self.assertEqual(
            actual_data[0]["relationships"]["device"]["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.device_id),
        )
        self.assertEqual(
            actual_data[0]["relationships"]["device"]["data"]["type"], "device"
        )

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_internal_by_involved_device_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't list internal information without a user - caused by the involved device."""
        cr_1000 = cr_1000_involvement_for_soil_moisture_datastream_link.device
        cr_1000.is_public = False
        cr_1000.is_internal = True
        db.session.add(cr_1000)
        db.session.commit()

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_internal_by_datastream_device_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't list internal information without a user - caused by the main device."""
        smt_100 = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.device
        )
        smt_100.is_public = False
        smt_100.is_internal = True
        db.session.add(smt_100)
        db.session.commit()

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_internal_by_configuration_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't list internal information without a user - caused by the configuration."""
        configuration = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.configuration
        )
        configuration.is_public = False
        configuration.is_internal = True
        db.session.add(configuration)
        db.session.commit()

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_list_internal_by_involved_device_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure that we can list internal information if we have a user if the involved device is internal."""
        cr_1000 = cr_1000_involvement_for_soil_moisture_datastream_link.device
        cr_1000.is_public = False
        cr_1000.is_internal = True
        db.session.add(cr_1000)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 1)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_list_internal_by_datastream_device_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure that we can list internal information if we have a user if the main device is internal."""
        smt_100 = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.device
        )
        smt_100.is_public = False
        smt_100.is_internal = True
        db.session.add(smt_100)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 1)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_list_internal_by_configuration_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure that we can list internal information if we have a user if the configuration is internal."""
        configuration = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.configuration
        )
        configuration.is_public = False
        configuration.is_internal = True
        db.session.add(configuration)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 1)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_filter_by_device_id(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can filter by using the device id."""
        device_id_with_result = (
            cr_1000_involvement_for_soil_moisture_datastream_link.device_id
        )
        device_id_without_result = device_id_with_result + 10000

        resp_with_result = self.client.get(
            self.url + f"?filter[device_id]={device_id_with_result}"
        )
        self.assertEqual(resp_with_result.status_code, 200)
        self.assertEqual(len(resp_with_result.json["data"]), 1)

        resp_without_result = self.client.get(
            self.url + f"?filter[device_id]={device_id_without_result}"
        )
        self.assertEqual(resp_without_result.status_code, 200)
        self.assertEqual(len(resp_without_result.json["data"]), 0)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_list_filter_by_datastream_link_id(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can filter by using the datastream link id."""
        datastream_link_id_with_result = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
        )
        datastream_link_id_without_result = datastream_link_id_with_result + 10000

        resp_with_result = self.client.get(
            self.url + f"?filter[datastream_link_id]={datastream_link_id_with_result}"
        )
        self.assertEqual(resp_with_result.status_code, 200)
        self.assertEqual(len(resp_with_result.json["data"]), 1)

        resp_without_result = self.client.get(
            self.url
            + f"?filter[datastream_link_id]={datastream_link_id_without_result}"
        )
        self.assertEqual(resp_without_result.status_code, 200)
        self.assertEqual(len(resp_without_result.json["data"]), 0)

    def test_get_one_notfound(self):
        """Ensure we return 404 if we can't find the object."""
        resp = self.client.get(self.url + "/12345678900")
        self.assertEqual(resp.status_code, 404)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_one_public_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can get the details if the information is public."""
        resp = self.client.get(
            self.url + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
        )
        self.assertEqual(resp.status_code, 200)
        actual_data = resp.json["data"]

        self.assertEqual(
            actual_data["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )
        self.assertEqual(actual_data["type"], "involved_device_for_datastream_link")
        self.assertEqual(
            actual_data["attributes"]["order_index"],
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index,
        )
        self.assertEqual(
            actual_data["relationships"]["datastream_link"]["data"]["id"],
            str(
                cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
            ),
        )
        self.assertEqual(
            actual_data["relationships"]["datastream_link"]["data"]["type"],
            "datastream_link",
        )
        self.assertEqual(
            actual_data["relationships"]["device"]["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.device_id),
        )
        self.assertEqual(
            actual_data["relationships"]["device"]["data"]["type"], "device"
        )

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_one_internal_by_involved_device_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't get the details without user if the involved device is internal."""
        cr_1000 = cr_1000_involvement_for_soil_moisture_datastream_link.device
        cr_1000.is_public = False
        cr_1000.is_internal = True
        db.session.add(cr_1000)
        db.session.commit()

        resp = self.client.get(
            self.url + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
        )
        self.assertEqual(resp.status_code, 401)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_one_internal_by_datastream_device_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't get the details without user if the main device is internal."""
        smt_100 = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.device
        )
        smt_100.is_public = False
        smt_100.is_internal = True
        db.session.add(smt_100)
        db.session.commit()

        resp = self.client.get(
            self.url + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
        )
        self.assertEqual(resp.status_code, 401)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_get_one_internal_by_configuration_for_anoynmous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can't get the details without user if the configuration is internal."""
        configuration = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.configuration
        )
        configuration.is_public = False
        configuration.is_internal = True
        db.session.add(configuration)
        db.session.commit()

        resp = self.client.get(
            self.url + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
        )
        self.assertEqual(resp.status_code, 401)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_one_internal_by_involved_device_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure we can get the details with a user even if the involved device is internal."""
        cr_1000 = cr_1000_involvement_for_soil_moisture_datastream_link.device
        cr_1000.is_public = False
        cr_1000.is_internal = True
        db.session.add(cr_1000)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(
                self.url
                + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_one_internal_by_datastream_device_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure we can get the details with a user even if the main device is internal."""
        smt_100 = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.device
        )
        smt_100.is_public = False
        smt_100.is_internal = True
        db.session.add(smt_100)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(
                self.url
                + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link", "user1"])
    def test_get_one_internal_by_configuration_for_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1
    ):
        """Ensure we can get the details with a user even if the configuration is internal."""
        configuration = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link.device_mount_action.configuration
        )
        configuration.is_public = False
        configuration.is_internal = True
        db.session.add(configuration)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(
                self.url
                + f"/{cr_1000_involvement_for_soil_moisture_datastream_link.id}"
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )

    @fixtures.use(["soil_moisture_datastream_link", "public_cr_1000"])
    def test_post_anonymous(self, soil_moisture_datastream_link, public_cr_1000):
        """Ensure we enforce that there is a user."""
        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(public_cr_1000.id), "type": "device"}
                    },
                },
            }
        }

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )

        self.assertEqual(response.status_code, 401)

    @fixtures.use(
        ["soil_moisture_datastream_link", "cr_1000_mount", "user1", "wrong_group"]
    )
    def test_post_user_with_wrong_group(
        self, soil_moisture_datastream_link, cr_1000_mount, user1, wrong_group
    ):
        """Ensure we enforce that there is a user that needs to be member of the permission group."""
        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(cr_1000_mount.device_id), "type": "device"}
                    },
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[wrong_group],
                )
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )

        self.assertEqual(response.status_code, 403)

    @fixtures.use(
        ["soil_moisture_datastream_link", "cr_1000_mount", "user1", "right_group"]
    )
    def test_post_user_with_right_group(
        self, soil_moisture_datastream_link, cr_1000_mount, user1, right_group
    ):
        """Ensure we allow posting for a user that is be member of the permission group."""
        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(cr_1000_mount.device_id), "type": "device"}
                    },
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )

        self.assertEqual(response.status_code, 201)

    @fixtures.use(["soil_moisture_datastream_link", "cr_1000_mount", "super_user"])
    def test_post_super_user(
        self, soil_moisture_datastream_link, cr_1000_mount, super_user
    ):
        """Ensure we allow to post for a super user."""
        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(cr_1000_mount.device_id), "type": "device"}
                    },
                },
            }
        }

        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 201)

    @fixtures.use(
        [
            "soil_moisture_datastream_link",
            "cr_1000_mount",
            "user1",
            "wrong_group",
            "right_group",
        ]
    )
    def test_post_user_with_involved_device_in_wrong_group_only(
        self,
        soil_moisture_datastream_link,
        cr_1000_mount,
        user1,
        wrong_group,
        right_group,
    ):
        """Ensure we can add involved devices even we are not allowed to edit them."""
        public_cr_1000 = cr_1000_mount.device
        public_cr_1000.group_ids = [wrong_group]
        db.session.add(public_cr_1000)
        db.session.commit()

        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(public_cr_1000.id), "type": "device"}
                    },
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )

        self.assertEqual(response.status_code, 201)

    @fixtures.use(
        ["soil_moisture_datastream_link", "cr_1000_mount", "user1", "right_group"]
    )
    def test_post_user_with_involved_device_not_mounted(
        self, soil_moisture_datastream_link, cr_1000_mount, user1, right_group
    ):
        """Ensure we don't allow to create entries for involved devices if not mounted in right configuration."""
        other_configuration = Configuration(
            label="Other configuration",
            is_public=True,
            is_internal=False,
            cfg_permission_group=right_group,
        )
        public_cr_1000 = cr_1000_mount.device
        cr_1000_mount.configuration = other_configuration

        db.session.add_all([other_configuration, cr_1000_mount])
        db.session.commit()

        payload = {
            "data": {
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": 123,
                },
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(soil_moisture_datastream_link.id),
                            "type": "datastream_link",
                        },
                    },
                    "device": {
                        "data": {"id": str(public_cr_1000.id), "type": "device"}
                    },
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )

        self.assertEqual(response.status_code, 409)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_patch_anonymous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we are not allowed to patch if we don't have a user."""
        payload = {
            "data": {
                "id": str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": cr_1000_involvement_for_soil_moisture_datastream_link.order_index
                    + 1
                },
            }
        }
        response = self.client.patch(
            f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "user1",
            "wrong_group",
        ]
    )
    def test_patch_user_in_wrong_group(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1, wrong_group
    ):
        """Ensure we are not allowing to patch if our user is not part of the group."""
        payload = {
            "data": {
                "id": str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": cr_1000_involvement_for_soil_moisture_datastream_link.order_index
                    + 1
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[wrong_group],
                )
                response = self.client.patch(
                    f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "user1",
            "right_group",
        ]
    )
    def test_patch_user_in_right_group(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1, right_group
    ):
        """Ensure we allow to patch if our user is member of the group."""
        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        current_order_index = (
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index
        )
        new_order_index = current_order_index + 1

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": new_order_index,
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.patch(
                    f"{self.url}/{id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

        reloaded_involved_device = (
            db.session.query(InvolvedDeviceForDatastreamLink).filter_by(id=id).first()
        )
        self.assertEqual(
            reloaded_involved_device.order_index,
            new_order_index,
        )

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "super_user",
        ]
    )
    def test_patch_super_user(
        self,
        cr_1000_involvement_for_soil_moisture_datastream_link,
        super_user,
    ):
        """Ensure we allow to patch if our user super user."""
        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        current_order_index = (
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index
        )
        new_order_index = current_order_index + 1

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": new_order_index,
                },
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "super_user",
        ]
    )
    def test_patch_not_found(
        self,
        cr_1000_involvement_for_soil_moisture_datastream_link,
        super_user,
    ):
        """Ensure we return a 404 if we don't find the existing entry."""
        id = cr_1000_involvement_for_soil_moisture_datastream_link.id + 1234
        current_order_index = (
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index
        )
        new_order_index = current_order_index + 1

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {
                    "order_index": new_order_index,
                },
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    @fixtures.use(
        [
            "right_group",
            "public_configuration",
            "contact1",
            "tsm_endpoint",
            "user1",
            "cr_1000_involvement_for_soil_moisture_datastream_link",
        ]
    )
    def test_patch_to_datastream_with_same_permissions(
        self,
        right_group,
        public_configuration,
        contact1,
        tsm_endpoint,
        user1,
        cr_1000_involvement_for_soil_moisture_datastream_link,
    ):
        """Ensure we can change the datastream as long as we are allowed to edit it."""
        other_smt_100 = Device(
            short_name="Other SMT 100",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[right_group],
        )
        other_soil_moisture = DeviceProperty(
            property_name="Soil moisture",
            device=other_smt_100,
        )
        other_smt_100_mount = DeviceMountAction(
            device=other_smt_100,
            configuration=public_configuration,
            begin_contact=contact1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
        )
        other_datastream_link = DatastreamLink(
            device_mount_action=other_smt_100_mount,
            device_property=other_soil_moisture,
            tsm_endpoint=tsm_endpoint,
            datasource_id=6,
            thing_id=7,
            datastream_id=8,
        )
        db.session.add_all(
            [
                other_smt_100,
                other_soil_moisture,
                other_smt_100_mount,
                other_datastream_link,
            ]
        )
        db.session.commit()

        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        new_datastream_id = other_datastream_link.id

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {},
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(new_datastream_id),
                            "type": "datastream_link",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.patch(
                    f"{self.url}/{id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

        reloaded_involved_device = (
            db.session.query(InvolvedDeviceForDatastreamLink).filter_by(id=id).first()
        )
        self.assertEqual(
            reloaded_involved_device.datastream_link_id,
            new_datastream_id,
        )

    @fixtures.use(
        [
            "right_group",
            "wrong_group",
            "contact1",
            "tsm_endpoint",
            "user1",
            "cr_1000_involvement_for_soil_moisture_datastream_link",
        ]
    )
    def test_patch_to_datastream_with_other_permissions(
        self,
        right_group,
        wrong_group,
        contact1,
        tsm_endpoint,
        user1,
        cr_1000_involvement_for_soil_moisture_datastream_link,
    ):
        """Ensure we can't change to datastreams we are not allowed to edit."""
        other_smt_100 = Device(
            short_name="Other SMT 100",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[wrong_group],
        )
        other_soil_moisture = DeviceProperty(
            property_name="Soil moisture",
            device=other_smt_100,
        )
        other_configuration = Configuration(
            label="Other configuration",
            is_public=True,
            is_internal=False,
            cfg_permission_group=wrong_group,
        )
        other_smt_100_mount = DeviceMountAction(
            device=other_smt_100,
            configuration=other_configuration,
            begin_contact=contact1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
        )
        other_datastream_link = DatastreamLink(
            device_mount_action=other_smt_100_mount,
            device_property=other_soil_moisture,
            tsm_endpoint=tsm_endpoint,
            datasource_id=6,
            thing_id=7,
            datastream_id=8,
        )
        db.session.add_all(
            [
                other_smt_100,
                other_soil_moisture,
                other_configuration,
                other_smt_100_mount,
                other_datastream_link,
            ]
        )
        db.session.commit()

        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        new_datastream_id = other_datastream_link.id

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {},
                "relationships": {
                    "datastream_link": {
                        "data": {
                            "id": str(new_datastream_id),
                            "type": "datastream_link",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.patch(
                    f"{self.url}/{id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    @fixtures.use(
        [
            "right_group",
            "wrong_group",
            "public_configuration",
            "contact1",
            "tsm_endpoint",
            "user1",
            "cr_1000_involvement_for_soil_moisture_datastream_link",
        ]
    )
    def test_patch_to_device_with_other_permissions(
        self,
        right_group,
        wrong_group,
        public_configuration,
        contact1,
        tsm_endpoint,
        user1,
        cr_1000_involvement_for_soil_moisture_datastream_link,
    ):
        """Ensure we can change to a device we are allowed to edit."""
        other_smt_100 = Device(
            short_name="Other SMT 100",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[wrong_group],
        )
        other_soil_moisture = DeviceProperty(
            property_name="Soil moisture",
            device=other_smt_100,
        )
        other_smt_100_mount = DeviceMountAction(
            device=other_smt_100,
            configuration=public_configuration,
            begin_contact=contact1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
        )
        other_datastream_link = DatastreamLink(
            device_mount_action=other_smt_100_mount,
            device_property=other_soil_moisture,
            tsm_endpoint=tsm_endpoint,
            datasource_id=6,
            thing_id=7,
            datastream_id=8,
        )
        db.session.add_all(
            [
                other_smt_100,
                other_soil_moisture,
                other_smt_100_mount,
                other_datastream_link,
            ]
        )
        db.session.commit()

        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        new_device_id = other_smt_100.id

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {},
                "relationships": {
                    "device": {
                        "data": {
                            "id": str(new_device_id),
                            "type": "device",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.patch(
                    f"{self.url}/{id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

        reloaded_involved_device = (
            db.session.query(InvolvedDeviceForDatastreamLink).filter_by(id=id).first()
        )
        self.assertEqual(
            reloaded_involved_device.device_id,
            new_device_id,
        )

    @fixtures.use(
        [
            "right_group",
            "contact1",
            "user1",
            "cr_1000_involvement_for_soil_moisture_datastream_link",
        ]
    )
    def test_patch_to_device_in_other_configuration(
        self,
        right_group,
        contact1,
        user1,
        cr_1000_involvement_for_soil_moisture_datastream_link,
    ):
        """Ensure we can't change to a device in a another configuration."""
        other_cr_1000 = Device(
            short_name="Other CR 1000",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[right_group],
        )
        other_configuration = Configuration(
            label="Other configuration",
            is_public=True,
            is_internal=False,
            cfg_permission_group=right_group,
        )
        other_cr_1000_mount = DeviceMountAction(
            device=other_cr_1000,
            configuration=other_configuration,
            begin_contact=contact1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
        )
        db.session.add_all(
            [
                other_cr_1000,
                other_configuration,
                other_cr_1000_mount,
            ]
        )
        db.session.commit()

        id = cr_1000_involvement_for_soil_moisture_datastream_link.id
        new_device_id = other_cr_1000_mount.id

        payload = {
            "data": {
                "id": str(id),
                "type": "involved_device_for_datastream_link",
                "attributes": {},
                "relationships": {
                    "device": {
                        "data": {
                            "id": str(new_device_id),
                            "type": "device",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.patch(
                    f"{self.url}/{id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_delete_anonymous(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure that we need a user to delete the involved device."""
        response = self.client.delete(
            f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
        )
        self.assertEqual(response.status_code, 401)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "user1",
            "wrong_group",
        ]
    )
    def test_delete_user_wrong_group(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1, wrong_group
    ):
        """Ensure that we need a user in the group to delete the involved device."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[wrong_group],
                )
                response = self.client.delete(
                    f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
                )
        self.assertEqual(response.status_code, 403)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "user1",
            "right_group",
        ]
    )
    def test_delete_user_right_group(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1, right_group
    ):
        """Ensure that we need delete if the user is in the right group."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.delete(
                    f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
                )
        self.assertEqual(response.status_code, 200)

        reloaded = (
            db.session.query(InvolvedDeviceForDatastreamLink)
            .filter_by(id=cr_1000_involvement_for_soil_moisture_datastream_link.id)
            .first()
        )
        self.assertIsNone(reloaded)

    @fixtures.use(
        ["cr_1000_involvement_for_soil_moisture_datastream_link", "super_user"]
    )
    def test_delete_super_user(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, super_user
    ):
        """Ensure that we need delete if the user is super user."""
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}",
            )
        self.assertEqual(response.status_code, 200)

    @fixtures.use(
        ["cr_1000_involvement_for_soil_moisture_datastream_link", "super_user"]
    )
    def test_delete_not_found(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, super_user
    ):
        """Ensure that we return 404 if we can't find the entry."""
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{self.url}/{cr_1000_involvement_for_soil_moisture_datastream_link.id}12344",
            )
        self.assertEqual(response.status_code, 404)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "user1",
            "right_group",
        ]
    )
    def test_delete_datastream_link_with_existing_involved_devices(
        self, cr_1000_involvement_for_soil_moisture_datastream_link, user1, right_group
    ):
        """Ensure that we can delete the datastream link with existing involved devices."""
        datastream_id = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
        )
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[right_group],
                )
                response = self.client.delete(
                    f"{base_url}/datastream-links/{datastream_id}",
                )
        self.assertEqual(response.status_code, 200)

        count_of_remaining_involved_device_for_datastream_link = (
            db.session.query(InvolvedDeviceForDatastreamLink)
            .filter_by(datastream_link_id=datastream_id)
            .count()
        )
        self.assertEqual(count_of_remaining_involved_device_for_datastream_link, 0)

    @fixtures.use(
        [
            "cr_1000_involvement_for_soil_moisture_datastream_link",
            "super_user",
            "cr_1000_mount",
        ]
    )
    def test_delete_device_with_existing_involvment(
        self,
        cr_1000_involvement_for_soil_moisture_datastream_link,
        super_user,
        cr_1000_mount,
    ):
        """Ensure that we can't delete the device that is involved in a datastream."""
        device_id = cr_1000_involvement_for_soil_moisture_datastream_link.device_id
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{base_url}/devices/{device_id}",
            )
        self.assertEqual(response.status_code, 409)

        # The 409 was to be expected as we also have the mount.
        # We should get the 409 too, even if there is no mount anymore.
        db.session.query(DeviceMountAction).filter_by(id=cr_1000_mount.id).delete()
        db.session.commit()
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{base_url}/devices/{device_id}",
            )

        self.assertEqual(response.status_code, 409)

    @fixtures.use(["cr_1000_involvement_for_soil_moisture_datastream_link"])
    def test_included_involved_devices_for_datastream(
        self, cr_1000_involvement_for_soil_moisture_datastream_link
    ):
        """Ensure we can include the involved devices in the payload for the datastreams."""
        datastream_id = (
            cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
        )
        resp = self.client.get(
            f"{base_url}/datastream-links/{datastream_id}?include=involved_devices",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        included = resp.json["included"]

        self.assertEqual(len(data["relationships"]["involved_devices"]["data"]), 1)
        self.assertEqual(
            data["relationships"]["involved_devices"]["data"][0]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )
        self.assertEqual(
            data["relationships"]["involved_devices"]["data"][0]["type"],
            "involved_device_for_datastream_link",
        )

        self.assertEqual(len(included), 1)
        self.assertEqual(
            included[0]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.id),
        )
        self.assertEqual(included[0]["type"], "involved_device_for_datastream_link")
        self.assertEqual(
            included[0]["attributes"]["order_index"],
            cr_1000_involvement_for_soil_moisture_datastream_link.order_index,
        )

        self.assertEqual(
            included[0]["relationships"]["device"]["data"]["id"],
            str(cr_1000_involvement_for_soil_moisture_datastream_link.device_id),
        )
        self.assertEqual(
            included[0]["relationships"]["device"]["data"]["type"], "device"
        )
        self.assertEqual(
            included[0]["relationships"]["datastream_link"]["data"]["id"],
            str(
                cr_1000_involvement_for_soil_moisture_datastream_link.datastream_link_id
            ),
        )
        self.assertEqual(
            included[0]["relationships"]["datastream_link"]["data"]["type"],
            "datastream_link",
        )

    def test_openapi(self):
        """Ensure that provide some information about the endpoints."""
        resp = self.client.get(f"{base_url}/openapi.json")
        self.assertEqual(resp.status_code, 200)

        paths = resp.json["paths"]

        self.assertTrue("/involved-devices-for-datastream-links" in paths.keys())
        self.assertTrue(
            "/involved-devices-for-datastream-links/{involved_device_for_datastream_link_id}"
            in paths.keys()
        )

        list_methods = paths["/involved-devices-for-datastream-links"]
        self.assertTrue("get" in list_methods.keys())
        self.assertTrue("post" in list_methods.keys())

        detail_methods = paths[
            "/involved-devices-for-datastream-links/{involved_device_for_datastream_link_id}"
        ]
        self.assertTrue("get" in detail_methods.keys())
        self.assertTrue("patch" in detail_methods.keys())
        self.assertTrue("delete" in detail_methods.keys())

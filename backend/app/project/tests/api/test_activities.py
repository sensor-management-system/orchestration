# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the activity route endpoints."""

from flask import url_for

from project import base_url
from project.api.models import (
    ActivityLog,
    Configuration,
    ConfigurationContactRole,
    Contact,
    Device,
    DeviceContactRole,
    Platform,
    PlatformContactRole,
    Site,
    SiteContactRole,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, Fixtures

fixtures = Fixtures()


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


@fixtures.register("device", scope=lambda: db.session)
def create_device():
    """Create a device to use in the tests."""
    result = Device(
        short_name="test device", is_public=True, is_internal=False, is_private=False
    )
    db.session.add(result)
    return result


@fixtures.register("platform", scope=lambda: db.session)
def create_platform():
    """Create a platform to use in the tests."""
    result = Platform(
        short_name="test platform", is_public=True, is_internal=False, is_private=False
    )
    db.session.add(result)
    return result


@fixtures.register("configuration", scope=lambda: db.session)
def create_configuration():
    """Create a configuration to use in the tests."""
    result = Configuration(
        label="test configuration",
        is_public=True,
        is_internal=False,
        cfg_permission_group="1",
    )
    db.session.add(result)
    return result


@fixtures.register("site", scope=lambda: db.session)
def create_site():
    """Create a site to use in the tests."""
    result = Site(
        label="test site",
        is_public=True,
        is_internal=False,
    )
    db.session.add(result)
    return result


@fixtures.register("device_contact_role", scope=lambda: db.session)
@fixtures.use(["super_user_contact", "device"])
def create_device_contact_role(super_user_contact, device):
    """Create device contact role to use it in the tests."""
    result = DeviceContactRole(
        contact=super_user_contact, device=device, role_name="Manufacturer", role_uri=""
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("platform_contact_role", scope=lambda: db.session)
@fixtures.use(["super_user_contact", "platform"])
def create_platform_contact_role(super_user_contact, platform):
    """Create platform contact role to use it in the tests."""
    result = PlatformContactRole(
        contact=super_user_contact,
        platform=platform,
        role_name="Manufacturer",
        role_uri="",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("configuration_contact_role", scope=lambda: db.session)
@fixtures.use(["super_user_contact", "configuration"])
def create_configuration_contact_role(super_user_contact, configuration):
    """Create configuration contact role to use it in the tests."""
    result = ConfigurationContactRole(
        contact=super_user_contact,
        configuration=configuration,
        role_name="Manufacturer",
        role_uri="",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("site_contact_role", scope=lambda: db.session)
@fixtures.use(["super_user_contact", "site"])
def create_site_contact_role(super_user_contact, site):
    """Create site contact role to use it in the tests."""
    result = SiteContactRole(
        contact=super_user_contact, site=site, role_name="Manufacturer", role_uri=""
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestActivityLogIsFilled(BaseTestCase):
    """Tests to ensure that we will our activity log properly."""

    @fixtures.use(["super_user"])
    def test_creating_a_device(self, super_user):
        """Ensure we add an activity log with every device we create via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/devices",
                json={
                    "data": {
                        "type": "device",
                        "attributes": {
                            "short_name": "test device",
                            "is_public": True,
                            "is_internal": False,
                            "is_private": False,
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(str).of(activity_log.entity_id).to_equal(resp.json["data"]["id"])
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;basic data")

    @fixtures.use(["super_user", "device"])
    def test_changing_basic_data_of_a_device(self, super_user, device):
        """Ensure that we add an activity log with every device that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/devices/{device.id}",
                json={
                    "data": {
                        "type": "device",
                        "id": str(device.id),
                        "attributes": {
                            "short_name": "different",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;basic data")

    @fixtures.use(["super_user", "device"])
    def test_delete_device(self, super_user, device):
        """Ensure that we add an activity log with every device that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/devices/{device.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;basic data")
        self.expect(activity_log.data).to_equal({})

    @fixtures.use(["super_user", "device"])
    def test_adding_contact_role_to_a_device(self, super_user, device):
        """Ensure that we add an activity log with every contact that we add to the device via the api."""
        # The same logic happens for many more related entities.
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/device-contact-roles",
                json={
                    "data": {
                        "type": "device_contact_role",
                        "attributes": {
                            "role_name": "Manufacturer",
                            "role_uri": "",
                        },
                        "relationships": {
                            "device": {
                                "data": {
                                    "type": "device",
                                    "id": str(device.id),
                                },
                            },
                            "contact": {
                                "data": {
                                    "type": "contact",
                                    "id": str(super_user.contact_id),
                                }
                            },
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;contact")

    @fixtures.use(["super_user", "device_contact_role"])
    def test_changing_contact_role_of_a_device(self, super_user, device_contact_role):
        """Ensure that we add an activity log with every contact role that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/device-contact-roles/{device_contact_role.id}",
                json={
                    "data": {
                        "type": "device_contact_role",
                        "id": str(device_contact_role.id),
                        "attributes": {
                            "role_name": "PI",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device_contact_role.device_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;contact")

    @fixtures.use(["super_user", "device_contact_role"])
    def test_deleting_contact_role_from_a_device(self, super_user, device_contact_role):
        """Ensure that we add an activity log with every contact role that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/device-contact-roles/{device_contact_role.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device_contact_role.device_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;contact")

    @fixtures.use(["super_user"])
    def test_creating_a_platform(self, super_user):
        """Ensure we add an activity log with every platform we create via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/platforms",
                json={
                    "data": {
                        "type": "platform",
                        "attributes": {
                            "short_name": "test platform",
                            "is_public": True,
                            "is_internal": False,
                            "is_private": False,
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(str).of(activity_log.entity_id).to_equal(resp.json["data"]["id"])
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;basic data")

    @fixtures.use(["super_user", "platform"])
    def test_changing_basic_data_of_a_platform(self, super_user, platform):
        """Ensure that we add an activity log with every platform that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/platforms/{platform.id}",
                json={
                    "data": {
                        "type": "platform",
                        "id": str(platform.id),
                        "attributes": {
                            "short_name": "different",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;basic data")

    @fixtures.use(["super_user", "platform"])
    def test_delete_platform(self, super_user, platform):
        """Ensure that we add an activity log with every platform that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/platforms/{platform.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;basic data")
        self.expect(activity_log.data).to_equal({})

    @fixtures.use(["super_user", "platform"])
    def test_adding_contact_role_to_a_platform(self, super_user, platform):
        """Ensure that we add an activity log with every contact that we add to the platform via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/platform-contact-roles",
                json={
                    "data": {
                        "type": "platform_contact_role",
                        "attributes": {
                            "role_name": "Manufacturer",
                            "role_uri": "",
                        },
                        "relationships": {
                            "platform": {
                                "data": {
                                    "type": "platform",
                                    "id": str(platform.id),
                                },
                            },
                            "contact": {
                                "data": {
                                    "type": "contact",
                                    "id": str(super_user.contact_id),
                                }
                            },
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;contact")

    @fixtures.use(["super_user", "platform_contact_role"])
    def test_changing_contact_role_of_a_platform(
        self, super_user, platform_contact_role
    ):
        """Ensure that we add an activity log with every contact role that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/platform-contact-roles/{platform_contact_role.id}",
                json={
                    "data": {
                        "type": "platform_contact_role",
                        "id": str(platform_contact_role.id),
                        "attributes": {
                            "role_name": "PI",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform_contact_role.platform_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;contact")

    @fixtures.use(["super_user", "platform_contact_role"])
    def test_deleting_contact_role_from_a_platform(
        self, super_user, platform_contact_role
    ):
        """Ensure that we add an activity log with every contact role that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/platform-contact-roles/{platform_contact_role.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform_contact_role.platform_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;contact")

    @fixtures.use(["super_user"])
    def test_creating_a_configuration(self, super_user):
        """Ensure we add an activity log with every configuration we create via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/configurations",
                json={
                    "data": {
                        "type": "configuration",
                        "attributes": {
                            "label": "test configuration",
                            "is_public": True,
                            "is_internal": False,
                            "cfg_permission_group": "1",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(str).of(activity_log.entity_id).to_equal(resp.json["data"]["id"])
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;basic data")

    @fixtures.use(["super_user", "configuration"])
    def test_delete_configuration(self, super_user, configuration):
        """Ensure that we add an activity log with every configuration that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/configurations/{configuration.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(configuration.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;basic data")
        self.expect(activity_log.data).to_equal({})

    @fixtures.use(["super_user", "configuration"])
    def test_changing_basic_data_of_a_configuration(self, super_user, configuration):
        """Ensure that we add an activity log with every configuration that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/configurations/{configuration.id}",
                json={
                    "data": {
                        "type": "configuration",
                        "id": str(configuration.id),
                        "attributes": {
                            "label": "different",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(configuration.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;basic data")

    @fixtures.use(["super_user", "configuration"])
    def test_adding_contact_role_to_a_configuration(self, super_user, configuration):
        """Ensure that we add an activity log with every contact that we add to the configuration via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/configuration-contact-roles",
                json={
                    "data": {
                        "type": "configuration_contact_role",
                        "attributes": {
                            "role_name": "Manufacturer",
                            "role_uri": "",
                        },
                        "relationships": {
                            "configuration": {
                                "data": {
                                    "type": "configuration",
                                    "id": str(configuration.id),
                                },
                            },
                            "contact": {
                                "data": {
                                    "type": "contact",
                                    "id": str(super_user.contact_id),
                                }
                            },
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(configuration.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;contact")

    @fixtures.use(["super_user", "configuration_contact_role"])
    def test_changing_contact_role_of_a_configuration(
        self, super_user, configuration_contact_role
    ):
        """Ensure that we add an activity log with every contact role that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/configuration-contact-roles/{configuration_contact_role.id}",
                json={
                    "data": {
                        "type": "configuration_contact_role",
                        "id": str(configuration_contact_role.id),
                        "attributes": {
                            "role_name": "PI",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(
            configuration_contact_role.configuration_id
        )
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;contact")

    @fixtures.use(["super_user", "configuration_contact_role"])
    def test_deleting_contact_role_from_a_configuration(
        self, super_user, configuration_contact_role
    ):
        """Ensure that we add an activity log with every contact role that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/configuration-contact-roles/{configuration_contact_role.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(
            configuration_contact_role.configuration_id
        )
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;contact")

    @fixtures.use(["super_user"])
    def test_creating_a_site(self, super_user):
        """Ensure we add an activity log with every site we create via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/sites",
                json={
                    "data": {
                        "type": "site",
                        "attributes": {
                            "label": "test site",
                            "is_public": True,
                            "is_internal": False,
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(str).of(activity_log.entity_id).to_equal(resp.json["data"]["id"])
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;basic data")

    @fixtures.use(["super_user", "site"])
    def test_delete_site(self, super_user, site):
        """Ensure that we add an activity log with every site that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/sites/{site.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;basic data")
        self.expect(activity_log.data).to_equal({})

    @fixtures.use(["super_user", "site"])
    def test_changing_basic_data_of_a_site(self, super_user, site):
        """Ensure that we add an activity log with every site that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/sites/{site.id}",
                json={
                    "data": {
                        "type": "site",
                        "id": str(site.id),
                        "attributes": {
                            "label": "different",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;basic data")

    @fixtures.use(["super_user", "site"])
    def test_adding_contact_role_to_a_site(self, super_user, site):
        """Ensure that we add an activity log with every contact that we add to the site via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/site-contact-roles",
                json={
                    "data": {
                        "type": "site_contact_role",
                        "attributes": {
                            "role_name": "Manufacturer",
                            "role_uri": "",
                        },
                        "relationships": {
                            "site": {
                                "data": {
                                    "type": "site",
                                    "id": str(site.id),
                                },
                            },
                            "contact": {
                                "data": {
                                    "type": "contact",
                                    "id": str(super_user.contact_id),
                                }
                            },
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;contact")

    @fixtures.use(["super_user", "site_contact_role"])
    def test_changing_contact_role_of_a_site(self, super_user, site_contact_role):
        """Ensure that we add an activity log with every contact role that we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/site-contact-roles/{site_contact_role.id}",
                json={
                    "data": {
                        "type": "site_contact_role",
                        "id": str(site_contact_role.id),
                        "attributes": {
                            "role_name": "PI",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site_contact_role.site_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;contact")

    @fixtures.use(["super_user", "site_contact_role"])
    def test_deleting_contact_role_from_a_site(self, super_user, site_contact_role):
        """Ensure that we add an activity log with every contact role that we delete via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/site-contact-roles/{site_contact_role.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site_contact_role.site_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;contact")

    @fixtures.use(["super_user"])
    def test_creating_a_contact(self, super_user):
        """Ensure that we add an activity log with every contact we create via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/contacts",
                json={
                    "data": {
                        "type": "contact",
                        "attributes": {
                            "given_name": "New",
                            "family_name": "Contact",
                            "email": "new.contact@sms.edu",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(201)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Contact")
        self.expect(str).of(activity_log.entity_id).to_equal(resp.json["data"]["id"])
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("create;basic data")

    @fixtures.use(["super_user"])
    def test_changing_basic_data_of_a_contact(self, super_user):
        """Ensure that we add an activity log with every contact we update via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{base_url}/contacts/{super_user.contact_id}",
                json={
                    "data": {
                        "type": "contact",
                        "id": str(super_user.contact_id),
                        "attributes": {
                            "email": "new.mail@sms.edu",
                        },
                    }
                },
                headers={"Content-type": "application/vnd.api+json"},
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Contact")
        self.expect(activity_log.entity_id).to_equal(super_user.contact_id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("update;basic data")

    @fixtures.use(["super_user"])
    def test_delete_contact(self, super_user):
        """Ensure that we add an activity log with every contact we delete via the api."""
        contact = Contact(
            given_name="example", family_name="contact", email="example.contact@web.edu"
        )
        db.session.add(contact)
        db.session.commit()

        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{base_url}/contacts/{contact.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Contact")
        self.expect(activity_log.entity_id).to_equal(contact.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("delete;basic data")
        self.expect(activity_log.data).to_equal({})

    @fixtures.use(["super_user", "device"])
    def test_archiving_a_device(self, super_user, device):
        """Ensure that we add an activity log for every device we archive via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/devices/{device.id}/archive",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("archive;basic data")

    @fixtures.use(["super_user", "device"])
    def test_restoring_a_device(self, super_user, device):
        """Ensure that we add an activity log for every device we restore via the api."""
        device.archived = True
        db.session.add(device)
        db.session.commit()
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/devices/{device.id}/restore",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Device")
        self.expect(activity_log.entity_id).to_equal(device.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("restore;basic data")

    @fixtures.use(["super_user", "platform"])
    def test_archiving_a_platform(self, super_user, platform):
        """Ensure that we add an activity log for every platform we archive via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/platforms/{platform.id}/archive",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("archive;basic data")

    @fixtures.use(["super_user", "platform"])
    def test_restoring_a_platform(self, super_user, platform):
        """Ensure that we add an activity log for every platform we restore via the api."""
        platform.archived = True
        db.session.add(platform)
        db.session.commit()
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/platforms/{platform.id}/restore",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Platform")
        self.expect(activity_log.entity_id).to_equal(platform.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("restore;basic data")

    @fixtures.use(["super_user", "configuration"])
    def test_archiving_a_configuration(self, super_user, configuration):
        """Ensure that we add an activity log for every configuration we archive via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/configurations/{configuration.id}/archive",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(configuration.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("archive;basic data")

    @fixtures.use(["super_user", "configuration"])
    def test_restoring_a_configuration(self, super_user, configuration):
        """Ensure that we add an activity log for every configuration we restore via the api."""
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/configurations/{configuration.id}/restore",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Configuration")
        self.expect(activity_log.entity_id).to_equal(configuration.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("restore;basic data")

    @fixtures.use(["super_user", "site"])
    def test_archiving_a_site(self, super_user, site):
        """Ensure that we add an activity log for every site we archive via the api."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/sites/{site.id}/archive",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("archive;basic data")

    @fixtures.use(["super_user", "site"])
    def test_restoring_a_site(self, super_user, site):
        """Ensure that we add an activity log for every site we restore via the api."""
        site.archived = True
        db.session.add(site)
        db.session.commit()
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        with self.run_requests_as(super_user):
            resp = self.client.post(
                f"{base_url}/sites/{site.id}/restore",
            )
        self.expect(resp.status_code).to_equal(204)
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(1)
        activity_log = db.session.query(ActivityLog).first()
        self.expect(activity_log.entity).to_equal("Site")
        self.expect(activity_log.entity_id).to_equal(site.id)
        self.expect(activity_log.created_by).to_equal(super_user)
        self.expect(activity_log.description).to_equal("restore;basic data")


class TestGlobalActivityEndpoint(BaseTestCase):
    """Test the endpoint for the global activity."""

    url = f"{base_url}/controller/global-activities"

    def test_no_parameters(self):
        """Ensure we return 400 bad request if the parameters are missing."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(400)

    def test_no_parsable_parameter(self):
        """Ensure we return 400 bad request if the parameters can't be parsed."""
        resp = self.client.get(self.url, query_string={"earliest": "a", "latest": "b"})
        self.expect(resp.status_code).to_equal(400)

    def test_no_activity_logs(self):
        """Ensure that the result is empty if we don't have any activity."""
        self.expect(db.session.query(ActivityLog.id).count()).to_equal(0)
        resp = self.client.get(
            self.url,
            query_string={
                "earliest": "1970-01-01T00:00:00Z",
                "latest": "2999-12-31T23:59:59Z",
            },
        )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json).to_equal({"data": []})

    @fixtures.use(["super_user"])
    def test_earliest_after_latest(self, super_user):
        """Ensure that we don't include any entries if the earliest is after the latest."""
        activity_log = ActivityLog(
            entity="Device",
            entity_id="1",
            created_by=super_user,
            created_at="2020-01-01T12:00:00Z",
        )
        db.session.add(activity_log)
        db.session.commit()

        resp = self.client.get(
            self.url,
            query_string={
                "earliest": "2030-12-31T23:59:59Z",
                "latest": "1970-01-01T00:00:00Z",
            },
        )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json).to_equal({"data": []})

    @fixtures.use(["super_user"])
    def test_result_aggregated_per_days(self, super_user):
        """Ensure we aggregate the counts per day."""
        activity_log1 = ActivityLog(
            entity="Device",
            entity_id="1",
            created_by=super_user,
            created_at="2020-01-01T12:00:00Z",
        )
        activity_log2 = ActivityLog(
            entity="Device",
            entity_id="2",
            created_by=super_user,
            created_at="2020-01-01T13:00:00Z",
        )
        activity_log3 = ActivityLog(
            entity="Platform",
            entity_id="1",
            created_by=super_user,
            created_at="2020-01-02T13:00:00Z",
        )

        db.session.add_all([activity_log1, activity_log2, activity_log3])
        db.session.commit()

        resp = self.client.get(
            self.url,
            query_string={
                "earliest": "1970-01-01T00:00:00Z",
                "latest": "2030-12-31T23:59:59Z",
            },
        )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json).to_equal(
            {
                "data": [
                    {"date": "2020-01-01", "count": 2},
                    {"date": "2020-01-02", "count": 1},
                ]
            }
        )

    def test_is_documented_in_openapi_specs(self):
        """Ensure that we documented the endpoint in the openapi specs."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())

        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())

        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

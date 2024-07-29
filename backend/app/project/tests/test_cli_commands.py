# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test cases for the CLI commands."""

import json
import os
import sys
import tempfile
from contextlib import contextmanager
from unittest.mock import patch

from click.testing import CliRunner

from manage import (
    b2inst_update_all,
    b2inst_update_configuration,
    b2inst_update_device,
    b2inst_update_platform,
    deactivate_a_user,
    loaddata,
    reactivate_a_user,
)
from project import db
from project.api.models import (
    Configuration,
    ConfigurationContactRole,
    Contact,
    Device,
    DeviceContactRole,
    Platform,
    PlatformContactRole,
    Site,
    SiteContactRole,
    TsmEndpoint,
    User,
)
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase, fake

# import manage packages onto the path

sys.path.append(os.path.abspath(os.path.join("..", "manage")))


# Avoid DetachedInstanceError in Flask-SQLAlchemy
# https://stackoverflow.com/a/51452451
@contextmanager
def no_expire():
    """Allow us to use the share the session between test code & cli runner."""
    s = db.session()
    s.expire_on_commit = False
    try:
        yield
    finally:
        s.expire_on_commit = True


class TestCliCommands(BaseTestCase):
    """Test class for some of the CLI commands."""

    def test_deactivate_a_user_but_not_found(self):
        """Ensure we stop if we don't find a user that we should deactivate."""
        runner = CliRunner()
        result = runner.invoke(
            deactivate_a_user, ["testuser1@ufz.test"], env={"FLASK_APP": "manage"}
        )
        assert result.exit_code != 0
        assert result.exception is not None
        assert "Can't find" in result.stdout
        assert "testuser1@ufz.test" in result.stdout

    def test_deactivate_a_user_but_not_destination_user_found(self):
        """Ensure we stop if we don't find a user for substitution while we are asked for that."""
        with no_expire():
            contact = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
                organization="UFZ Test",
                website="https://ufz.de/test",
                orcid="0000-1111-2222-3333-4444",
            )
            user = User(subject="testuser1@ufz.test", contact=contact)
            db.session.add_all([contact, user])
            db.session.commit()

            runner = CliRunner()
            result = runner.invoke(
                deactivate_a_user,
                ["testuser1@ufz.test", "--dest-user-subject=testuser2@ufz.test"],
                env={"FLASK_APP": "manage"},
            )
            assert result.exit_code != 0
            assert result.exception is not None
            assert "Can't find" in result.stdout
            assert "testuser2@ufz.test" in result.stdout

    def test_deactivate_a_user_with_no_substituted_user(self):
        """Ensure that a user can be deactivated and all it data are changed to deactivation message."""
        with no_expire():
            contact = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
                organization="UFZ Test",
                website="https://ufz.de/test",
                orcid="0000-1111-2222-3333-4444",
            )
            user = User(subject="testuser1@ufz.test", contact=contact)

            device = Device(
                short_name="device_short_name test",
                created_by_id=user.id,
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )

            device_contact_role = DeviceContactRole(
                device=device,
                contact=contact,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            db.session.add_all([contact, user, device, device_contact_role])
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst, "has_external_metadata"
            ) as has_external_metadata:
                has_external_metadata.return_value = True
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    result = runner.invoke(
                        deactivate_a_user,
                        ["testuser1@ufz.test"],
                        env={"FLASK_APP": "manage"},
                    )
                    update_external_metadata.assert_called_once()
                has_external_metadata.assert_called_once()

            assert not result.exception
            assert result.exit_code == 0
            assert user.active is False
            msg = f"User {user.id} is deactivated"
            assert contact.email == msg
            assert contact.given_name == msg
            assert contact.family_name == msg
            assert contact.website == ""
            assert contact.organization == ""
            assert contact.orcid is None

    def test_deactivate_a_user_with_substituted_user(self):
        """Ensure that a user can be deactivated and provide a substituted user."""
        with no_expire():
            contact1 = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
            )
            contact2 = Contact(
                given_name="Test",
                family_name="User2",
                email="test.user2@ufz.test",
            )
            user1 = User(subject="testuser1@ufz.test", contact=contact1)
            user2 = User(subject="testuser2@ufz.test", contact=contact2)
            device = Device(
                short_name="device_short_name test",
                created_by_id=user1.id,
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )

            device_contact_role = DeviceContactRole(
                device=device,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            platform = Platform(
                short_name="dummy platform",
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            platform_contact_role = PlatformContactRole(
                platform=platform,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            configuration = Configuration(
                label="dummy configuration",
                is_internal=True,
                is_public=False,
            )

            configuration_contact_role = ConfigurationContactRole(
                configuration=configuration,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            site = Site(
                label="dummy site",
                is_internal=True,
                is_public=False,
            )

            site_contact_role = SiteContactRole(
                site=site,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            db.session.add_all(
                [
                    contact1,
                    contact2,
                    user1,
                    user2,
                    device,
                    device_contact_role,
                    platform,
                    platform_contact_role,
                    configuration,
                    configuration_contact_role,
                    site,
                    site_contact_role,
                ]
            )
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst, "has_external_metadata"
            ) as has_external_metadata:
                has_external_metadata.return_value = True
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    result = runner.invoke(
                        deactivate_a_user,
                        [
                            "testuser1@ufz.test",
                            "--dest-user-subject=testuser2@ufz.test",
                        ],
                        env={"FLASK_APP": "manage"},
                    )
                    update_called = set(
                        [
                            (x[0][0].id, type(x[0][0]))
                            for x in update_external_metadata.call_args_list
                        ]
                    )
                has_external_called = set(
                    [
                        (x[0][0].id, type(x[0][0]))
                        for x in has_external_metadata.call_args_list
                    ]
                )

            assert not result.exception
            assert result.exit_code == 0
            assert user1.active is False
            assert user2.active is True

            device_contact_roles = (
                db.session.query(DeviceContactRole).filter_by(device_id=device.id).all()
            )
            assert len(device_contact_roles) == 1
            assert device_contact_roles[0].contact.id == contact2.id

            platform_contact_roles = (
                db.session.query(PlatformContactRole)
                .filter_by(platform_id=platform.id)
                .all()
            )
            assert len(platform_contact_roles) == 1
            assert platform_contact_roles[0].contact.id == contact2.id

            configuration_contact_roles = (
                db.session.query(ConfigurationContactRole)
                .filter_by(configuration_id=configuration.id)
                .all()
            )
            assert len(configuration_contact_roles) == 1
            assert configuration_contact_roles[0].contact.id == contact2.id

            site_contact_roles = (
                db.session.query(SiteContactRole).filter_by(site_id=site.id).all()
            )
            assert len(site_contact_roles) == 1
            assert site_contact_roles[0].contact.id == contact2.id

            assert (site.id, Site) in update_called
            assert (device.id, Device) in update_called
            assert (platform.id, Platform) in update_called
            assert (configuration.id, Configuration) in update_called
            assert update_called == has_external_called

    def test_deactivate_a_user_with_substituted_user_and_existing_roles(self):
        """Ensure that we don't overwrite contacts if the target contact is already there with the very same role."""
        with no_expire():
            contact1 = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
            )
            contact2 = Contact(
                given_name="Test",
                family_name="User2",
                email="test.user2@ufz.test",
            )
            user1 = User(subject="testuser1@ufz.test", contact=contact1)
            user2 = User(subject="testuser2@ufz.test", contact=contact2)
            device = Device(
                short_name="device_short_name test",
                created_by_id=user1.id,
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )

            device_contact_role1 = DeviceContactRole(
                device=device,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )
            device_contact_role2 = DeviceContactRole(
                device=device,
                contact=contact2,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            platform = Platform(
                short_name="dummy platform",
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            platform_contact_role1 = PlatformContactRole(
                platform=platform,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )
            platform_contact_role2 = PlatformContactRole(
                platform=platform,
                contact=contact2,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            configuration = Configuration(
                label="dummy configuration",
                is_internal=True,
                is_public=False,
            )

            configuration_contact_role1 = ConfigurationContactRole(
                configuration=configuration,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )
            configuration_contact_role2 = ConfigurationContactRole(
                configuration=configuration,
                contact=contact2,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            site = Site(
                label="dummy site",
                is_internal=True,
                is_public=False,
            )

            site_contact_role1 = SiteContactRole(
                site=site,
                contact=contact1,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )
            site_contact_role2 = SiteContactRole(
                site=site,
                contact=contact2,
                role_name="Owner",
                role_uri="https://cv/roles/4",
            )

            db.session.add_all(
                [
                    contact1,
                    contact2,
                    user1,
                    user2,
                    device,
                    device_contact_role1,
                    device_contact_role2,
                    platform,
                    platform_contact_role1,
                    platform_contact_role2,
                    configuration,
                    configuration_contact_role1,
                    configuration_contact_role2,
                    site,
                    site_contact_role1,
                    site_contact_role2,
                ]
            )
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst, "has_external_metadata"
            ) as has_external_metadata:
                has_external_metadata.return_value = True
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    result = runner.invoke(
                        deactivate_a_user,
                        [
                            "testuser1@ufz.test",
                            "--dest-user-subject=testuser2@ufz.test",
                        ],
                        env={"FLASK_APP": "manage"},
                    )
                    update_called = set(
                        [
                            (x[0][0].id, type(x[0][0]))
                            for x in update_external_metadata.call_args_list
                        ]
                    )
                has_external_called = set(
                    [
                        (x[0][0].id, type(x[0][0]))
                        for x in has_external_metadata.call_args_list
                    ]
                )

            assert not result.exception
            assert result.exit_code == 0
            assert user1.active is False
            assert user2.active is True

            device_contact_roles = (
                db.session.query(DeviceContactRole).filter_by(device_id=device.id).all()
            )
            assert len(device_contact_roles) == 1
            assert device_contact_roles[0].contact.id == contact2.id

            platform_contact_roles = (
                db.session.query(PlatformContactRole)
                .filter_by(platform_id=platform.id)
                .all()
            )
            assert len(platform_contact_roles) == 1
            assert platform_contact_roles[0].contact.id == contact2.id

            configuration_contact_roles = (
                db.session.query(ConfigurationContactRole)
                .filter_by(configuration_id=configuration.id)
                .all()
            )
            assert len(configuration_contact_roles) == 1
            assert configuration_contact_roles[0].contact.id == contact2.id

            site_contact_roles = (
                db.session.query(SiteContactRole).filter_by(site_id=site.id).all()
            )
            assert len(site_contact_roles) == 1
            assert site_contact_roles[0].contact.id == contact2.id

            assert (site.id, Site) in update_called
            assert (device.id, Device) in update_called
            assert (platform.id, Platform) in update_called
            assert (configuration.id, Configuration) in update_called
            assert update_called == has_external_called

    def test_reactivate_a_user(self):
        """Ensure that a user can be reactivated."""
        with no_expire():
            contact = Contact(
                given_name="User is deactivated",
                family_name="User is deactivated",
                email="User is deactivated",
                active=False,
            )
            user = User(subject="testuser@ufz.test", contact=contact, active=False)
            db.session.expire_on_commit = False
            db.session.add_all([contact, user])
            db.session.commit()

            runner = CliRunner()

            reactivate = runner.invoke(
                reactivate_a_user,
                ["testuser@ufz.test"],
                env={"FLASK_APP": "manage"},
                input="Test\nUser\ntest.user@ufz.test\n",
            )
            assert user.active is True
            assert contact.active is True
            assert contact.email == "test.user@ufz.test"
            assert reactivate.exit_code == 0

    def test_load_data_completely_new(self):
        """Ensure we can insert completly new data."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            data = [
                {
                    "fields": {
                        "name": "FOO",
                        "url": "https://foo",
                    },
                    "model": "TsmEndpoint",
                    "pk": 1,
                },
                {
                    "fields": {
                        "name": "BAR",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "pk": 2,
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(2, db.session.query(TsmEndpoint).count())
            tsm_endpoint1 = db.session.get(TsmEndpoint, 1)
            tsm_endpoint2 = db.session.get(TsmEndpoint, 2)
            self.assertEqual(tsm_endpoint1.name, "FOO")
            self.assertEqual(tsm_endpoint1.url, "https://foo")
            self.assertEqual(tsm_endpoint2.name, "BAR")
            self.assertEqual(tsm_endpoint2.url, "https://bar")

    def test_load_data_update_existing(self):
        """Ensure we can update existing data."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            tsm_endpoint = TsmEndpoint(id=1, name="foo", url="https://foo")
            db.session.add(tsm_endpoint)
            db.session.commit()
            data = [
                {
                    "fields": {
                        "name": "BAR",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "pk": 1,
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(1, db.session.query(TsmEndpoint).count())
            reloaded_tsm_endpoint = db.session.get(TsmEndpoint, 1)
            self.assertEqual(reloaded_tsm_endpoint.name, "BAR")
            self.assertEqual(reloaded_tsm_endpoint.url, "https://bar")

    def test_load_data_update_existing_by_unique_criteria(self):
        """Ensure we can update existing data without knowing the primary key."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            tsm_endpoint = TsmEndpoint(name="foo", url="https://foo")
            db.session.add(tsm_endpoint)
            db.session.commit()
            data = [
                {
                    "fields": {
                        "name": "foo",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "unique": ["name"],
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(1, db.session.query(TsmEndpoint).count())
            reloaded_tsm_endpoint = (
                db.session.query(TsmEndpoint).filter_by(name="foo").first()
            )
            self.assertEqual(reloaded_tsm_endpoint.url, "https://bar")

    def test_load_data_insert_new_by_unique_criteria(self):
        """Ensure we can insert new data without having a pk."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            tsm_endpoint = TsmEndpoint(name="foo", url="https://foo")
            db.session.add(tsm_endpoint)
            db.session.commit()
            data = [
                {
                    "fields": {
                        "name": "bar",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "unique": ["name"],
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(2, db.session.query(TsmEndpoint).count())
            reloaded_tsm_endpoint = (
                db.session.query(TsmEndpoint).filter_by(name="bar").first()
            )
            self.assertEqual(reloaded_tsm_endpoint.url, "https://bar")

    def test_load_data_error_if_unique_criteria_is_not_unique(self):
        """Ensure don't change anything but raise an error if the unique criteria is not unique."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            tsm_endpoint1 = TsmEndpoint(id=1, name="foo", url="https://foo1")
            db.session.add(tsm_endpoint1)
            tsm_endpoint2 = TsmEndpoint(id=2, name="foo", url="https://foo2")
            db.session.add(tsm_endpoint2)
            db.session.commit()
            data = [
                {
                    "fields": {
                        "name": "new",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "unique": ["name"],
                },
                {
                    "fields": {
                        "name": "foo",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "unique": ["name"],
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertNotEqual(result.exit_code, 0)

            # Nothing has changed.
            self.assertEqual(2, db.session.query(TsmEndpoint).count())
            reloaded_tsm_endpoint1 = db.session.get(TsmEndpoint, 1)
            reloaded_tsm_endpoint2 = db.session.get(TsmEndpoint, 2)
            self.assertEqual(reloaded_tsm_endpoint1.url, "https://foo1")
            self.assertEqual(reloaded_tsm_endpoint2.url, "https://foo2")

    def test_load_data_empty_data(self):
        """Ensure we can run it without any data in it."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            data = []
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(0, db.session.query(TsmEndpoint).count())

    def test_load_data_empty_file_error(self):
        """Ensure we raise an error if we try to load a completly empty file."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
                self.assertTrue(isinstance(result.exception, json.JSONDecodeError))

    def test_load_data_missing_file_error(self):
        """Ensure we raise an error if there is no such file."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                different_path = path + "123432432432423543543.json"
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [different_path],
                    env={"FLASK_APP": "manage"},
                )
                self.assertTrue(isinstance(result.exception, FileNotFoundError))

    def test_load_data_empty_file_ignore(self):
        """Ensure we can ignore it if the file is completely empty."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path, "--skip-empty-file"],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(result.exit_code, 0)

    def test_load_data_missing_file_ignore(self):
        """Ensure we can ignore it if the file doesn't exists."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                different_path = path + "123432432432423543543.json"
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [different_path, "--skip-missing-file"],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(result.exit_code, 0)

    def test_b2inst_update_device(self):
        """Ensure we call the b2inst.update_external_metadata function for the selected device."""
        with no_expire():
            device = Device(
                short_name="device_short_name test",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            db.session.add(device)
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                result = runner.invoke(
                    b2inst_update_device,
                    [str(device.id)],
                    env={"FLASK_APP": "manage"},
                )
                update_external_metadata.assert_called_once()
                args, kwargs = update_external_metadata.call_args
                called_device = args[0]
                run_async = kwargs["run_async"]
                self.assertEqual(called_device, device)
                self.assertFalse(run_async)

            assert not result.exception
            assert result.exit_code == 0

    def test_b2inst_update_platform(self):
        """Ensure we call the b2inst.update_external_metadata function for the selected platform."""
        with no_expire():
            platform = Platform(
                short_name="platform_short_name test",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            db.session.add(platform)
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                result = runner.invoke(
                    b2inst_update_platform,
                    [str(platform.id)],
                    env={"FLASK_APP": "manage"},
                )
                update_external_metadata.assert_called_once()
                args, kwargs = update_external_metadata.call_args
                called_platform = args[0]
                run_async = kwargs["run_async"]
                self.assertEqual(called_platform, platform)
                self.assertFalse(run_async)

            assert not result.exception
            assert result.exit_code == 0

    def test_b2inst_update_configuration(self):
        """Ensure we call the b2inst.update_external_metadata function for the selected configuration."""
        with no_expire():
            configuration = Configuration(
                label="configuration_short_name test",
                is_public=False,
                is_internal=True,
            )
            db.session.add(configuration)
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                result = runner.invoke(
                    b2inst_update_configuration,
                    [str(configuration.id)],
                    env={"FLASK_APP": "manage"},
                )
                update_external_metadata.assert_called_once()
                args, kwargs = update_external_metadata.call_args
                called_configuration = args[0]
                run_async = kwargs["run_async"]
                self.assertEqual(called_configuration, configuration)
                self.assertFalse(run_async)

            assert not result.exception
            assert result.exit_code == 0

    def test_b2inst_update_all(self):
        """Ensure we can run the update for all the elements with b2inst record id."""
        with no_expire():
            device_without_b2inst = Device(
                short_name="device_short_name test",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            device_with_b2inst = Device(
                short_name="device_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="125",
            )
            platform_without_b2inst = Platform(
                short_name="platform_short_name test",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )
            platform_with_b2inst = Platform(
                short_name="platform_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="124",
            )
            configuration_without_b2inst = Configuration(
                label="configuration_short_name test",
                is_public=False,
                is_internal=True,
            )
            configuration_with_b2inst = Configuration(
                label="configuration_short_name test with b2inst",
                is_public=False,
                is_internal=True,
                b2inst_record_id="123",
            )
            db.session.add_all(
                [
                    device_without_b2inst,
                    device_with_b2inst,
                    platform_without_b2inst,
                    platform_with_b2inst,
                    configuration_without_b2inst,
                    configuration_with_b2inst,
                ]
            )
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                result = runner.invoke(
                    b2inst_update_all,
                    [],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(
                    update_external_metadata.call_count,
                    3,
                )

            assert not result.exception
            assert result.exit_code == 0

    def test_b2inst_update_all_with_errors(self):
        """Ensure we stop with updating if we have an error."""
        with no_expire():
            device_with_b2inst = Device(
                short_name="device_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="125",
            )
            platform_with_b2inst = Platform(
                short_name="platform_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="124",
            )
            configuration_with_b2inst = Configuration(
                label="configuration_short_name test with b2inst",
                is_public=False,
                is_internal=True,
                b2inst_record_id="123",
            )
            db.session.add_all(
                [
                    device_with_b2inst,
                    platform_with_b2inst,
                    configuration_with_b2inst,
                ]
            )
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.side_effect = Exception("Some problem")
                result = runner.invoke(
                    b2inst_update_all,
                    [],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(
                    update_external_metadata.call_count,
                    1,
                )

            assert result.exception == update_external_metadata.side_effect
            assert result.exit_code == 1

    def test_b2inst_update_all_skip_errors(self):
        """Ensure we can skip the errors."""
        with no_expire():
            device_with_b2inst = Device(
                short_name="device_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="125",
            )
            platform_with_b2inst = Platform(
                short_name="platform_short_name test with b2inst",
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
                b2inst_record_id="124",
            )
            configuration_with_b2inst = Configuration(
                label="configuration_short_name test with b2inst",
                is_public=False,
                is_internal=True,
                b2inst_record_id="123",
            )
            db.session.add_all(
                [
                    device_with_b2inst,
                    platform_with_b2inst,
                    configuration_with_b2inst,
                ]
            )
            db.session.commit()

            runner = CliRunner()
            with patch.object(
                pidinst.b2inst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.side_effect = Exception("Some problem")
                result = runner.invoke(
                    b2inst_update_all,
                    ["--skip-problematic"],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(
                    update_external_metadata.call_count,
                    3,
                )

            # We only log the errors, but the overall command goes fine.
            assert result.exception is None
            assert result.exit_code == 0

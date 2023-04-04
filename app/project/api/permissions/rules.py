"""Set of rules what action is allowed on the entities."""
import itertools

from flask import g
from sqlalchemy import and_, or_

from ...extensions.instances import idl
from ..datalayers.esalchemy import AndFilter, OrFilter, TermEqualsExactStringFilter
from ..helpers.custom_dispatch import custom_dispatch
from ..models import (
    Configuration,
    ConfigurationAttachment,
    ConfigurationContactRole,
    ConfigurationCustomField,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
    Contact,
    CustomField,
    DatastreamLink,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
    DeviceCalibrationAttachment,
    DeviceContactRole,
    DeviceMountAction,
    DeviceProperty,
    DevicePropertyCalibration,
    DeviceSoftwareUpdateAction,
    DeviceSoftwareUpdateActionAttachment,
    GenericConfigurationAction,
    GenericConfigurationActionAttachment,
    GenericDeviceAction,
    GenericDeviceActionAttachment,
    GenericPlatformAction,
    GenericPlatformActionAttachment,
    Platform,
    PlatformAttachment,
    PlatformContactRole,
    PlatformMountAction,
    PlatformSoftwareUpdateAction,
    PlatformSoftwareUpdateActionAttachment,
    Site,
    SiteContactRole,
    User,
)
from ..models.base_model import db


# Create some generic functions.
@custom_dispatch
def can_see(entity):
    """Return if the entity can be seen."""
    return type(entity)


@custom_dispatch
def can_create(type_, data):
    """Return if the type with the data can be created."""
    return type_


@custom_dispatch
def can_edit(entity):
    """Return if the entity can be edited."""
    return type(entity)


@custom_dispatch
def can_change(entity, data):
    """Return if the entity can be changed with the data."""
    # Reason to have it seperate to can_edit is that the overall
    # edit option is used very often without as delegated function,
    # without actually changing the entity that is tested then.
    #
    # This function here is really for the updates on the given
    # entity.
    return type(entity)


@custom_dispatch
def can_delete(entity):
    """Return if the entity can be deleted."""
    return type(entity)


@custom_dispatch
def can_archive(entity):
    """Return if the entity can be archived."""
    return type(entity)


@custom_dispatch
def can_restore(entity):
    """Return if the entity can be restored."""
    return type(entity)


@custom_dispatch
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    # Take the model class of db.session.query(model)
    return query.column_descriptions[0]["type"]


@custom_dispatch
def filter_visible_es(model_class):
    """
    Create the elasticsearch query based on the visibility settings.

    This function must only provided for those entities that can
    use the elsticsearch.

    Should be consistent to the filter_visible function.
    """
    return model_class


# Set the default for some of those functions.
@can_see.default
def can_see_default(entity):
    """Don't allow to see for unspecified types."""
    return False


@can_create.default
def can_create_default(type_, data):
    """Don't allow to create for unspecified types."""
    return False


@can_edit.default
def can_edit_default(entity):
    """Don't allow to edit for unspecified types."""
    return False


@can_change.default
def can_change_default(entity, data):
    """Allow the update."""
    # Reason here is that can_edit should run before.
    # If that works, then we should be able to do changes,
    # except for those that we specify specifically.
    return True


@can_delete.default
def can_delete_default(entity):
    """Don't allow to delete for unspecified types."""
    return False


@can_archive.default
def can_archive_default(entity):
    """Don't allow to archive unspecified types."""
    return False


@can_restore.default
def can_restore_default(entity):
    """Don't allow to restore unspecified types."""
    return False


@filter_visible.default
def filter_visible_default(query):
    """Use the default filtering for the visibility (take everything)."""
    return query


@filter_visible_es.default
def filter_visible_es_default(model_class):
    """Don't create a filter so that everything is visible."""
    return None


# Configuration
@can_see.register(Configuration)
def can_see(entity):
    """Return if the entity can be seen."""
    # For the Configurations we only differ if it is
    # public (visible for everyone) or internal (so that you need to
    # be logged in to see it.)
    return entity.is_public or g.user


@can_create.register(Configuration)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    # Without user => no creation at all.
    if not g.user:
        return False
    # Super user is allowed to do it anyhow.
    if g.user.is_superuser:
        return True
    # Otherwise we use the permission groups.
    permission_group = data.get("cfg_permission_group")
    # We really want the user to set one on creation.
    if not permission_group or permission_group == "{}":
        return False
    # Any kind of membership is sufficient.
    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    if permission_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        return True
    return False


@can_edit.register(Configuration)
def can_edit(entity):
    """Return if the entity can be edited."""
    if not g.user:
        return False
    # No change for archived configurations is allowed.
    if entity.archived:
        return False
    if g.user.is_superuser:
        return True
    # Difference here to the creation: If the permission group is not set,
    # then we allow it (to change older entries).
    if not entity.cfg_permission_group or entity.cfg_permission_group == "{}":
        return True
    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    if entity.cfg_permission_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        return True
    return False


@can_change.register(Configuration)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # If we have an update in the permission group, we want that the user
    # is still at least a member in it.
    if data.get("cfg_permission_group"):
        cfg_permission_group = data["cfg_permission_group"]
        idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
        if not idl_user:
            return False

        if cfg_permission_group in itertools.chain(
            idl_user.administrated_permission_groups,
            idl_user.membered_permission_groups,
        ):
            return True
        return False
    return True


@can_delete.register(Configuration)
def can_delete(entity):
    """Return if the entity can be deleted."""
    if entity.archived:
        return False
    # Only super users can delete.
    return g.user and g.user.is_superuser


@can_archive.register(Configuration)
def can_archive(entity):
    """Return if the entity can be archived."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # For archiving we need admin role.
    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    if entity.cfg_permission_group in idl_user.administrated_permission_groups:
        return True

    return False


@can_restore.register(Configuration)
def can_restore(entity):
    """Return if the entity can be restored."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # For restoring we need the admin role.
    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    if entity.cfg_permission_group in idl_user.administrated_permission_groups:
        return True

    return False


@filter_visible.register(Configuration)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    if not g.user:
        query = query.filter(Configuration.is_public.is_(True))
    return query


@filter_visible_es.register(Configuration)
def filter_visible_es(model_class):
    """Create the filter for the visibility for Configurations."""
    if not g.user:
        return TermEqualsExactStringFilter("is_public", True)
    return None


# ConfigurationAttachment
# Here we delegate a lot.
@can_see.register(ConfigurationAttachment)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.configuration)


@can_create.register(ConfigurationAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    configuration_id = data.get("configuration")
    # adding an attachment to the configuration is like editing
    # configuration itself.
    return can_edit(
        db.session.query(Configuration)
        .filter(Configuration.id == configuration_id)
        .first()
    )


@can_edit.register(ConfigurationAttachment)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.configuration)


@can_change.register(ConfigurationAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    # If we have an update in the configuration, then we want to make
    # sure that we still have edit rights for the configuration.
    if data.get("configuration"):
        if not can_edit(
            db.session.query(Configuration)
            .filter(Configuration.id == data["configuration"])
            .first()
        ):
            return False
    return True


@can_delete.register(ConfigurationAttachment)
def can_delete(entity):
    """Return if the entity can be deleted."""
    # Removing an attachment on a configuration is like editing
    # the configuration itself.
    return can_edit(entity.configuration)


@filter_visible.register(ConfigurationAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(Configuration, query.join(Configuration))


# ConfigurationContactRole
# ConfigurationCustomField
# ConfigurationDynamicLocationBeginAction
# ConfigurationStaticLocationBeginAction
# GenericConfigurationAction
for model in [
    ConfigurationContactRole,
    ConfigurationCustomField,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
    GenericConfigurationAction,
]:
    can_see.register_same(model, handler=ConfigurationAttachment)
    can_create.register_same(model, handler=ConfigurationAttachment)
    can_edit.register_same(model, handler=ConfigurationAttachment)
    can_change.register_same(model, handler=ConfigurationAttachment)
    can_delete.register_same(model, handler=ConfigurationAttachment)
    filter_visible.register_same(model, handler=ConfigurationAttachment)

# DeviceMountAction
@can_see.register(DeviceMountAction)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.configuration) and can_see(entity.device)


@can_create.register(DeviceMountAction)
def can_create(type_, data):
    """Return true if we can create the entity."""
    configuration_id = data.get("configuration")
    device_id = data.get("device")

    # We need to have edit rights on both the configuration and the device.
    return can_edit(
        db.session.query(Configuration)
        .filter(Configuration.id == configuration_id)
        .first()
    ) and can_edit(db.session.query(Device).filter(Device.id == device_id).first())


@can_edit.register(DeviceMountAction)
def can_edit(entity):
    """Return true if we can edit the entity."""
    return can_edit(entity.configuration) and can_edit(entity.device)


@can_change.register(DeviceMountAction)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("configuration"):
        if not can_edit(
            db.session.query(Configuration)
            .filter(Configuration.id == data["configuration"])
            .first()
        ):
            return False
    if data.get("device"):
        if not can_edit(
            db.session.query(Device).filter(Device.id == data["device"]).first()
        ):
            return False
    return True


@can_delete.register(DeviceMountAction)
def can_delete(entity):
    """Return true if we can delete the entity."""
    return can_edit(entity.configuration) and can_edit(entity.device)


@filter_visible.register(DeviceMountAction)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    query = filter_visible.delegate(Configuration, query.join(Configuration))
    query = filter_visible.delegate(Device, query.join(Device))
    return query


# PlatformMountAction
@can_see.register(PlatformMountAction)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.configuration) and can_see(entity.platform)


@can_create.register(PlatformMountAction)
def can_create(type_, data):
    """Return true if we can create the entity."""
    configuration_id = data.get("configuration")
    platform_id = data.get("platform")

    return can_edit(
        db.session.query(Configuration)
        .filter(Configuration.id == configuration_id)
        .first()
    ) and can_edit(
        db.session.query(Platform).filter(Platform.id == platform_id).first()
    )


@can_edit.register(PlatformMountAction)
def can_edit(entity):
    """Return true if we can edit the entity."""
    return can_edit(entity.configuration) and can_edit(entity.platform)


@can_change.register(PlatformMountAction)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("configuration"):
        if not can_edit(
            db.session.query(Configuration)
            .filter(Configuration.id == data["configuration"])
            .first()
        ):
            return False
    if data.get("platform"):
        if not can_edit(
            db.session.query(Platform).filter(Platform.id == data["platform"]).first()
        ):
            return False
    return True


@can_delete.register(PlatformMountAction)
def can_delete(entity):
    """Return true if we can delete the entity."""
    return can_edit(entity.configuration) and can_edit(entity.platform)


@filter_visible.register(PlatformMountAction)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    query = filter_visible.delegate(Configuration, query.join(Configuration))
    query = filter_visible.delegate(Platform, query.join(PlatformMountAction.platform))
    return query


# Contact
@can_see.register(Contact)
def can_see(entity):
    """Return if the entity can be seen."""
    return True


@can_create.register(Contact)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    return g.user


@can_edit.register(Contact)
def can_edit(entity):
    """Return if the entity can be edited."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # Normal user should be able to edit its own contact information.
    if g.user.contact == entity:
        return True
    if entity.created_by == g.user:
        # If we have a different user for the contact, we don't allow to edit.
        if db.session.query(User).filter(User.contact == entity).first():
            return False
        return True
    return False


@can_change.register(Contact)
def can_change(entity, data):
    """Return if we can change the entity with the data."""
    # There is no change possible with the api that we need to restrict.
    return True


@can_delete.register(Contact)
def can_delete(entity):
    """Return if the entity can be deleted."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    if g.user.contact == entity:
        # Don't allow to delete his own contact.
        return False
    if entity.created_by == g.user:
        # if we have a user for that contact, we don't want to allow to delete it.
        if db.session.query(User).filter(User.contact == entity).first():
            return False
        return True
    return False


# CustomField
@can_see.register(CustomField)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.device)


@can_create.register(CustomField)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    device_id = data.get("device")
    return can_edit(db.session.query(Device).filter(Device.id == device_id).first())


@can_edit.register(CustomField)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.device)


@can_change.register(CustomField)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("device"):
        if not can_edit(
            db.session.query(Device).filter(Device.id == data["device"]).first()
        ):
            return False
    return True


@can_delete.register(CustomField)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.device)


@filter_visible.register(CustomField)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(Device, query.join(Device))


# DeviceAttachment
# DeviceCalibrationAction
# DeviceContactRole
# DeviceProperty
# DeviceSoftwareUpdateAction
# GenericDeviceAction
for model in [
    DeviceAttachment,
    DeviceCalibrationAction,
    DeviceContactRole,
    DeviceProperty,
    DeviceSoftwareUpdateAction,
    GenericDeviceAction,
]:
    can_see.register_same(model, handler=CustomField)
    can_create.register_same(model, handler=CustomField)
    can_edit.register_same(model, handler=CustomField)
    can_change.register_same(model, handler=CustomField)
    can_delete.register_same(model, handler=CustomField)
    filter_visible.register_same(model, handler=CustomField)


# DatastreamLink
@can_see.register(DatastreamLink)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.device_mount_action)


@can_create.register(DatastreamLink)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    device_mount_action_id = data.get("device_mount_action")
    return can_edit(
        db.session.query(DeviceMountAction)
        .filter(DeviceMountAction.id == device_mount_action_id)
        .first()
    )


@can_edit.register(DatastreamLink)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.device_mount_action)


@can_change.register(DatastreamLink)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("device_mount_action"):
        if not can_edit(
            db.session.query(DeviceMountAction)
            .filter(DeviceMountAction.id == data["device_mount_action"])
            .first()
        ):
            return False
    return True


@can_delete.register(DatastreamLink)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.device_mount_action)


@filter_visible.register(DatastreamLink)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        DeviceMountAction, query.join(DatastreamLink.device_mount_action)
    )


# Device
@can_see.register(Device)
def can_see(entity):
    """Return if the entity can be seen."""
    if entity.is_public:
        return True
    if g.user:
        if g.user.is_superuser:
            return True
        if entity.is_internal:
            return True
        # For devices we also have private settings.
        # So the user can see it, but other normal users can't.
        if entity.is_private and g.user == entity.created_by:
            return True
    return False


@can_create.register(Device)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    if data.get("is_private"):
        return True
    # We want to enforce groups for new devices.
    if not data.get("group_ids"):
        return False
    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        for group in data.get("group_ids", []):
            if idl_group == group:
                return True
    return False


@can_edit.register(Device)
def can_edit(entity):
    """Return if the entity can be edited."""
    if not g.user:
        return False
    if entity.archived:
        return False
    if g.user.is_superuser:
        return True
    if entity.is_private:
        # If private then the creator should be the
        # only way to decide if that should be editable.
        if entity.created_by == g.user:
            return True
        return False

    if not entity.group_ids:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False
    for idl_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@can_change.register(Device)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # We don't allow to switch back to private if it was internal
    # or public before.
    if data.get("is_private") and not entity.is_private:
        return False
    # If we have an update in the permission groups, we want that the user
    # is still at least a member in it.
    if data.get("group_ids"):
        group_ids = data["group_ids"]
        idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
        if not idl_user:
            return False
        is_at_least_member = False
        for idl_group in itertools.chain(
            idl_user.administrated_permission_groups,
            idl_user.membered_permission_groups,
        ):
            for group in group_ids:
                if idl_group == group:
                    is_at_least_member = True
                    break
        if not is_at_least_member:
            return False
        # And we want to check that those that are removed are removed
        # because we are admin in it.
        removed_group_without_being_admin = False
        # entity.group_ids could be None initially.
        old_group_ids = entity.group_ids or []
        removed_groups = set(old_group_ids) - set(group_ids)
        for removed_group in removed_groups:
            if removed_group not in idl_user.administrated_permission_groups:
                removed_group_without_being_admin = True
                break
        if removed_group_without_being_admin:
            return False
    return True


@can_delete.register(Device)
def can_delete(entity):
    """Return if the entity can be deleted."""
    if entity.archived:
        return False
    if entity.persistent_identifier:
        return False
    if g.user and g.user.is_superuser:
        return True
    if entity.is_private and entity.created_by == g.user:
        return True
    return False


@can_archive.register(Device)
def can_archive(entity):
    """Return if the entity can be archived."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    if entity.is_private and entity.created_by == g.user:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in idl_user.administrated_permission_groups:
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@can_restore.register(Device)
def can_restore(entity):
    """Return if the entity can be restored."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    if entity.is_private and entity.created_by == g.user:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in idl_user.administrated_permission_groups:
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@filter_visible.register(Device)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    if g.user and g.user.is_superuser:
        return query
    if not g.user:
        return query.filter_by(is_public=True)
    model = Device
    return query.filter(
        or_(
            and_(
                model.is_private,
                model.created_by_id == g.user.id,
            ),
            or_(
                model.is_public,
                model.is_internal,
            ),
        )
    )


@filter_visible_es.register(Device)
def filter_visible_es(model_class):
    """Create the elasticsearch filter for the device visibility."""
    if not g.user:
        return TermEqualsExactStringFilter("is_public", True)
    if g.user.is_superuser:
        return None
    return OrFilter(
        [
            AndFilter(
                [
                    TermEqualsExactStringFilter("is_private", True),
                    TermEqualsExactStringFilter("created_by_id", g.user.id),
                ]
            ),
            TermEqualsExactStringFilter("is_public", True),
            TermEqualsExactStringFilter("is_internal", True),
        ]
    )


# DeviceCalibrationAttachment
@can_see.register(DeviceCalibrationAttachment)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.action)


@can_create.register(DeviceCalibrationAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(DeviceCalibrationAction)
        .filter(DeviceCalibrationAction.id == action_id)
        .first()
    )


@can_edit.register(DeviceCalibrationAttachment)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.action)


@can_change.register(DeviceCalibrationAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(DeviceCalibrationAction)
            .filter(DeviceCalibrationAction.id == data["action"])
            .first()
        ):
            return False
    return True


@can_delete.register(DeviceCalibrationAttachment)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.action)


@filter_visible.register(DeviceCalibrationAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        DeviceCalibrationAction, query.join(DeviceCalibrationAction)
    )


# DevicePropertyCalibration
@can_see.register(DevicePropertyCalibration)
def can_see(entity):
    """Return true if we are allowed to see the entity."""
    return can_see(entity.calibration_action)


@can_create.register(DevicePropertyCalibration)
def can_create(type_, data):
    """Return true if we are allowed to create the entity."""
    action_id = data.get("calibration_action")
    return can_edit(
        db.session.query(DeviceCalibrationAction)
        .filter(DeviceCalibrationAction.id == action_id)
        .first()
    )


@can_edit.register(DevicePropertyCalibration)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.calibration_action)


@can_change.register(DevicePropertyCalibration)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("calibration_action"):
        if not can_edit(
            db.session.query(DeviceCalibrationAction)
            .filter(DeviceCalibrationAction.id == data["calibration_action"])
            .first()
        ):
            return False
    return True


@can_delete.register(DevicePropertyCalibration)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.calibration_action)


filter_visible.register_same(
    DevicePropertyCalibration, handler=DeviceCalibrationAttachment
)

# DeviceSoftwareUpdateActionAttachment
can_see.register_same(
    DeviceSoftwareUpdateActionAttachment, handler=DeviceCalibrationAttachment
)


@can_create.register(DeviceSoftwareUpdateActionAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(DeviceSoftwareUpdateAction)
        .filter(DeviceSoftwareUpdateAction.id == action_id)
        .first()
    )


can_edit.register_same(
    DeviceSoftwareUpdateActionAttachment, handler=DeviceCalibrationAttachment
)


@can_change.register(DeviceSoftwareUpdateActionAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(DeviceSoftwareUpdateAction)
            .filter(DeviceSoftwareUpdateAction.id == data["action"])
            .first()
        ):
            return False
    return True


can_delete.register_same(
    DeviceSoftwareUpdateActionAttachment, handler=DeviceCalibrationAttachment
)


@filter_visible.register(DeviceSoftwareUpdateActionAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        DeviceSoftwareUpdateAction, query.join(DeviceSoftwareUpdateAction)
    )


# GenericConfigurationActionAttachment
@can_see.register(GenericConfigurationActionAttachment)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.action)


@can_create.register(GenericConfigurationActionAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(GenericConfigurationAction)
        .filter(GenericConfigurationAction.id == action_id)
        .first()
    )


@can_edit.register(GenericConfigurationActionAttachment)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.action)


@can_change.register(GenericConfigurationActionAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(GenericConfigurationAction)
            .filter(GenericConfigurationAction.id == data["action"])
            .first()
        ):
            return False
    return True


@can_delete.register(GenericConfigurationActionAttachment)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.action)


@filter_visible.register(GenericConfigurationActionAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        GenericConfigurationAction, query.join(GenericConfigurationAction)
    )


# GenericDeviceActionAttachment
can_see.register_same(
    GenericDeviceActionAttachment, handler=DeviceCalibrationAttachment
)


@can_create.register(GenericDeviceActionAttachment)
def can_create(type_, data):
    """Return true if we are allowed to create the entity."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(GenericDeviceAction)
        .filter(GenericDeviceAction.id == action_id)
        .first()
    )


can_edit.register_same(
    GenericDeviceActionAttachment, handler=DeviceCalibrationAttachment
)


@can_change.register(GenericDeviceActionAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(GenericDeviceAction)
            .filter(GenericDeviceAction.id == data["action"])
            .first()
        ):
            return False
    return True


can_delete.register_same(
    GenericDeviceActionAttachment, handler=DeviceCalibrationAttachment
)


@filter_visible.register(GenericDeviceActionAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(GenericDeviceAction, query.join(GenericDeviceAction))


# GenericPlatformAction
@can_see.register(GenericPlatformAction)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.platform)


@can_create.register(GenericPlatformAction)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    platform_id = data.get("platform")
    return can_edit(
        db.session.query(Platform).filter(Platform.id == platform_id).first()
    )


@can_edit.register(GenericPlatformAction)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.platform)


@can_change.register(GenericPlatformAction)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("platform"):
        if not can_edit(
            db.session.query(Platform).filter(Platform.id == data["platform"]).first()
        ):
            return False
    return True


@can_delete.register(GenericPlatformAction)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.platform)


@filter_visible.register(GenericPlatformAction)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(Platform, query.join(Platform))


# PlatformAttachment
# PlatformContactRole
# PlatformSoftwareUpdateAction
for model in [PlatformAttachment, PlatformContactRole, PlatformSoftwareUpdateAction]:
    can_see.register_same(model, handler=GenericPlatformAction)
    can_create.register_same(model, handler=GenericPlatformAction)
    can_edit.register_same(model, handler=GenericPlatformAction)
    can_change.register_same(model, handler=GenericPlatformAction)
    can_delete.register_same(model, handler=GenericPlatformAction)
    filter_visible.register_same(model, handler=GenericPlatformAction)

# GenericPlatformActionAttachment
@can_see.register(GenericPlatformActionAttachment)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.action)


@can_create.register(GenericPlatformActionAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(GenericPlatformAction)
        .filter(GenericPlatformAction.id == action_id)
        .first()
    )


@can_change.register(GenericPlatformActionAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(GenericPlatformAction)
            .filter(GenericPlatformAction.id == data["action"])
            .first()
        ):
            return False
    return True


@can_edit.register(GenericPlatformActionAttachment)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.action)


@can_delete.register(GenericPlatformActionAttachment)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.action)


@filter_visible.register(GenericPlatformActionAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        GenericPlatformAction, query.join(GenericPlatformAction)
    )


# Platform
can_see.register_same(Platform, handler=Device)
can_create.register_same(Platform, handler=Device)
can_edit.register_same(Platform, handler=Device)
can_change.register_same(Platform, handler=Device)
can_delete.register_same(Platform, handler=Device)
can_archive.register_same(Platform, handler=Device)
can_restore.register_same(Platform, handler=Device)


@filter_visible.register(Platform)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    if g.user and g.user.is_superuser:
        return query
    if not g.user:
        return query.filter_by(is_public=True)
    model = Platform
    return query.filter(
        or_(
            and_(
                model.is_private,
                model.created_by_id == g.user.id,
            ),
            or_(
                model.is_public,
                model.is_internal,
            ),
        )
    )


filter_visible_es.register_same(Platform, handler=Device)

# PlatformSoftwareUpdateActionAttachment
can_see.register_same(
    PlatformSoftwareUpdateActionAttachment, handler=GenericPlatformActionAttachment
)


@can_create.register(PlatformSoftwareUpdateActionAttachment)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    action_id = data.get("action")
    return can_edit(
        db.session.query(PlatformSoftwareUpdateAction)
        .filter(PlatformSoftwareUpdateAction.id == action_id)
        .first()
    )


can_edit.register_same(
    PlatformSoftwareUpdateActionAttachment, handler=GenericPlatformActionAttachment
)


@can_change.register(PlatformSoftwareUpdateActionAttachment)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("action"):
        if not can_edit(
            db.session.query(PlatformSoftwareUpdateAction)
            .filter(PlatformSoftwareUpdateAction.id == data["action"])
            .first()
        ):
            return False
    return True


can_delete.register_same(
    PlatformSoftwareUpdateActionAttachment, handler=GenericPlatformActionAttachment
)


@filter_visible.register(PlatformSoftwareUpdateActionAttachment)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(
        PlatformSoftwareUpdateAction, query.join(PlatformSoftwareUpdateAction)
    )


# Site
@can_see.register(Site)
def can_see(entity):
    """Return if the entity can be seen."""
    if entity.is_public:
        return True
    if g.user:
        if g.user.is_superuser:
            return True
        if entity.is_internal:
            return True
    return False


@can_create.register(Site)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    group_ids = data.get("group_ids")
    if not group_ids:
        return False

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        for group in data.get("group_ids"):
            if idl_group == group:
                return True
    return False


@can_edit.register(Site)
def can_edit(entity):
    """Return if the entity can be edited."""
    if not g.user:
        return False
    if entity.archived:
        return False
    if g.user.is_superuser:
        return True

    if not entity.group_ids:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in itertools.chain(
        idl_user.administrated_permission_groups, idl_user.membered_permission_groups
    ):
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@can_change.register(Site)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True
    # If we have an update in the permission groups, we want that the user
    # is still at least a member in it.
    if data.get("group_ids"):
        group_ids = data["group_ids"]
        idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
        if not idl_user:
            return False
        is_at_least_member = False
        for idl_group in itertools.chain(
            idl_user.administrated_permission_groups,
            idl_user.membered_permission_groups,
        ):
            for group in group_ids:
                if idl_group == group:
                    is_at_least_member = True
                    break
        if not is_at_least_member:
            return False
        # And we want to check that those that are removed are removed
        # because we are admin in it.
        removed_group_without_being_admin = False
        # entity.group_ids could be None initially.
        old_group_ids = entity.group_ids or []
        removed_groups = set(old_group_ids) - set(group_ids)
        for removed_group in removed_groups:
            if removed_group not in idl_user.administrated_permission_groups:
                removed_group_without_being_admin = True
                break
        if removed_group_without_being_admin:
            return False
    return True


@can_delete.register(Site)
def can_delete(entity):
    """Return if the entity can be deleted."""
    if entity.archived:
        return False
    if g.user and g.user.is_superuser:
        return True
    return False


@can_archive.register(Site)
def can_archive(entity):
    """Return if the entity can be archived."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in idl_user.administrated_permission_groups:
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@can_restore.register(Site)
def can_restore(entity):
    """Return if the entity can be restored."""
    if not g.user:
        return False
    if g.user.is_superuser:
        return True

    idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_user:
        return False

    for idl_group in idl_user.administrated_permission_groups:
        for group in entity.group_ids:
            if idl_group == group:
                return True

    return False


@filter_visible.register(Site)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    if not g.user:
        return query.filter_by(is_public=True)
    return query


filter_visible_es.register_same(Site, handler=Configuration)

# SiteContactRole
@can_see.register(SiteContactRole)
def can_see(entity):
    """Return if the entity can be seen."""
    return can_see(entity.site)


@can_create.register(SiteContactRole)
def can_create(type_, data):
    """Return if the type with the data can be created."""
    site_id = data.get("site")
    return can_edit(db.session.query(Site).filter(Site.id == site_id).first())


@can_edit.register(SiteContactRole)
def can_edit(entity):
    """Return if the entity can be edited."""
    return can_edit(entity.site)


@can_change.register(SiteContactRole)
def can_change(entity, data):
    """Return if we can change the entity accordingly."""
    if data.get("site"):
        if not can_edit(db.session.query(Site).filter(Site.id == data["site"]).first()):
            return False
    return True


@can_delete.register(SiteContactRole)
def can_delete(entity):
    """Return if the entity can be deleted."""
    return can_edit(entity.site)


@filter_visible.register(SiteContactRole)
def filter_visible(query):
    """Filter the query based on the visibility settings."""
    return filter_visible.delegate(Site, query.join(Site))

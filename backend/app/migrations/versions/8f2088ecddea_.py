# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""
This migration fixes some issues with the ce029fd02198 migration.

The ce029fd02198 migration was used to introduce the model classes for
actions in the SMS backend.
As things often don't work perfectly the very first try, here are some improvements:

* enforce some foreign keys by not allowing them to be null
* fix some constraints regarding to the _name & _uri handling for references to the CV


Revision ID: 8f2088ecddea
Revises: ce029fd02198
Create Date: 2021-02-25 15:02:51.100736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f2088ecddea"
down_revision = "ce029fd02198"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "fk_ConfigurationDynamicLocationBeginAction_updated_by_id",
        "configuration_dynamic_location_begin_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationDynamicLocationBeginAction_created_by_id",
        "configuration_dynamic_location_begin_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationDynamicLocationEndAction_updated_by_id",
        "configuration_dynamic_location_end_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationDynamicLocationEndAction_created_by_id",
        "configuration_dynamic_location_end_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationStaticLocationBeginAction_updated_by_id",
        "configuration_static_location_begin_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationStaticLocationBeginAction_created_by_id",
        "configuration_static_location_begin_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationStaticLocationEndAction_created_by_id",
        "configuration_static_location_end_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_ConfigurationStaticLocationEndAction_updated_by_id",
        "configuration_static_location_end_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.alter_column(
        "device_calibration_action",
        "device_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.create_foreign_key(
        "fk_DeviceCalibrationAction_created_by_id",
        "device_calibration_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceCalibrationAction_updated_by_id",
        "device_calibration_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceMountAction_created_by_id",
        "device_mount_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceMountAction_updated_by_id",
        "device_mount_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.alter_column(
        "device_property_calibration",
        "device_property_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_constraint(
        "device_property_calibration_calibration_action_id_fkey",
        "device_property_calibration",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "device_property_calibration",
        "device_calibration_action",
        ["calibration_action_id"],
        ["id"],
    )
    op.alter_column(
        "device_software_update_action",
        "software_type_uri",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.create_foreign_key(
        "fk_DeviceSoftwareUpdateAction_created_by_id",
        "device_software_update_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceSoftwareUpdateAction_updated_by_id",
        "device_software_update_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceUnmountAction_created_by_id",
        "device_unmount_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DeviceUnmountAction_updated_by_id",
        "device_unmount_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericConfigurationAction_updated_by_id",
        "generic_configuration_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericConfigurationAction_created_by_id",
        "generic_configuration_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericDeviceAction_updated_by_id",
        "generic_device_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericDeviceAction_created_by_id",
        "generic_device_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericPlatformAction_created_by_id",
        "generic_platform_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_GenericPlatformAction_updated_by_id",
        "generic_platform_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_PlatformMountAction_created_by_id",
        "platform_mount_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_PlatformMountAction_updated_by_id",
        "platform_mount_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.alter_column(
        "platform_software_update_action",
        "software_type_uri",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.create_foreign_key(
        "fk_PlatformSoftwareUpdateAction_created_by_id",
        "platform_software_update_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_PlatformSoftwareUpdateAction_updated_by_id",
        "platform_software_update_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_PlatformUnmountAction_updated_by_id",
        "platform_unmount_action",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_PlatformUnmountAction_created_by_id",
        "platform_unmount_action",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_PlatformUnmountAction_created_by_id",
        "platform_unmount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_PlatformUnmountAction_updated_by_id",
        "platform_unmount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_PlatformSoftwareUpdateAction_updated_by_id",
        "platform_software_update_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_PlatformSoftwareUpdateAction_created_by_id",
        "platform_software_update_action",
        type_="foreignkey",
    )
    op.alter_column(
        "platform_software_update_action",
        "software_type_uri",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.drop_constraint(
        "fk_PlatformMountAction_updated_by_id",
        "platform_mount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_PlatformMountAction_created_by_id",
        "platform_mount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericPlatformAction_updated_by_id",
        "generic_platform_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericPlatformAction_created_by_id",
        "generic_platform_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericDeviceAction_created_by_id",
        "generic_device_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericDeviceAction_updated_by_id",
        "generic_device_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericConfigurationAction_created_by_id",
        "generic_configuration_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_GenericConfigurationAction_updated_by_id",
        "generic_configuration_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DeviceUnmountAction_updated_by_id",
        "device_unmount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DeviceUnmountAction_created_by_id",
        "device_unmount_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DeviceSoftwareUpdateAction_updated_by_id",
        "device_software_update_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DeviceSoftwareUpdateAction_created_by_id",
        "device_software_update_action",
        type_="foreignkey",
    )
    op.alter_column(
        "device_software_update_action",
        "software_type_uri",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.drop_constraint(None, "device_property_calibration", type_="foreignkey")
    op.create_foreign_key(
        "device_property_calibration_calibration_action_id_fkey",
        "device_property_calibration",
        "device_property",
        ["calibration_action_id"],
        ["id"],
    )
    op.alter_column(
        "device_property_calibration",
        "device_property_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_constraint(
        "fk_DeviceMountAction_updated_by_id", "device_mount_action", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_DeviceMountAction_created_by_id", "device_mount_action", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_DeviceCalibrationAction_updated_by_id",
        "device_calibration_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DeviceCalibrationAction_created_by_id",
        "device_calibration_action",
        type_="foreignkey",
    )
    op.alter_column(
        "device_calibration_action",
        "device_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_constraint(
        "fk_ConfigurationStaticLocationEndAction_updated_by_id",
        "configuration_static_location_end_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationStaticLocationEndAction_created_by_id",
        "configuration_static_location_end_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationStaticLocationBeginAction_created_by_id",
        "configuration_static_location_begin_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationStaticLocationBeginAction_updated_by_id",
        "configuration_static_location_begin_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationDynamicLocationEndAction_created_by_id",
        "configuration_dynamic_location_end_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationDynamicLocationEndAction_updated_by_id",
        "configuration_dynamic_location_end_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationDynamicLocationBeginAction_created_by_id",
        "configuration_dynamic_location_begin_action",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_ConfigurationDynamicLocationBeginAction_updated_by_id",
        "configuration_dynamic_location_begin_action",
        type_="foreignkey",
    )
    # ### end Alembic commands ###

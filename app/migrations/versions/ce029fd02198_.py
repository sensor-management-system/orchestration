"""empty message

Revision ID: ce029fd02198
Revises: eac266534186
Create Date: 2021-02-25 08:37:58.707512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce029fd02198'
down_revision = 'eac266534186'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_calibration_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('current_calibration_date', sa.DateTime(), nullable=False),
    sa.Column('next_calibration_date', sa.DateTime(), nullable=True),
    sa.Column('formula', sa.String(length=256), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_DeviceCalibrationAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_DeviceCalibrationAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_software_update_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('software_type_name', sa.String(length=256), nullable=False),
    sa.Column('software_type_uri', sa.String(length=256), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=True),
    sa.Column('repository_url', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_DeviceSoftwareUpdateAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_DeviceSoftwareUpdateAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_device_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('action_type_name', sa.String(length=256), nullable=False),
    sa.Column('action_type_uri', sa.String(length=256), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_GenericDeviceAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_GenericDeviceAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_platform_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('action_type_name', sa.String(length=256), nullable=False),
    sa.Column('action_type_uri', sa.String(length=256), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_GenericPlatformAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_GenericPlatformAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform_software_update_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('software_type_name', sa.String(length=256), nullable=False),
    sa.Column('software_type_uri', sa.String(length=256), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=True),
    sa.Column('repository_url', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_PlatformSoftwareUpdateAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_PlatformSoftwareUpdateAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_calibration_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['device_calibration_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['device_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_property_calibration',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('calibration_action_id', sa.Integer(), nullable=False),
    sa.Column('device_property_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['calibration_action_id'], ['device_property.id'], ),
    sa.ForeignKeyConstraint(['device_property_id'], ['device_property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_software_update_action_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['device_software_update_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['device_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_device_action_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['generic_device_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['device_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_platform_action_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['generic_platform_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['platform_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform_software_update_action_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['platform_software_update_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['platform_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=256), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_dynamic_location_begin_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('x_property_id', sa.Integer(), nullable=True),
    sa.Column('y_property_id', sa.Integer(), nullable=True),
    sa.Column('z_property_id', sa.Integer(), nullable=True),
    sa.Column('epsg_code', sa.String(length=256), nullable=True),
    sa.Column('elevation_datum_name', sa.String(length=256), nullable=True),
    sa.Column('elevation_datum_uri', sa.String(length=256), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_ConfigurationDynamicLocationBeginAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_ConfigurationDynamicLocationBeginAction_updated_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['x_property_id'], ['device_property.id'], ),
    sa.ForeignKeyConstraint(['y_property_id'], ['device_property.id'], ),
    sa.ForeignKeyConstraint(['z_property_id'], ['device_property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_dynamic_location_end_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_ConfigurationDynamicLocationEndAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_ConfigurationDynamicLocationEndAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_static_location_begin_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Float(), nullable=True),
    sa.Column('y', sa.Float(), nullable=True),
    sa.Column('z', sa.Float(), nullable=True),
    sa.Column('epsg_code', sa.String(length=256), nullable=True),
    sa.Column('elevation_datum_name', sa.String(length=256), nullable=True),
    sa.Column('elevation_datum_uri', sa.String(length=256), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_ConfigurationStaticLocationBeginAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_ConfigurationStaticLocationBeginAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuration_static_location_end_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_ConfigurationStaticLocationEndAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_ConfigurationStaticLocationEndAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_mount_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('parent_platform_id', sa.Integer(), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('offset_x', sa.Float(), nullable=True),
    sa.Column('offset_y', sa.Float(), nullable=True),
    sa.Column('offset_z', sa.Float(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_DeviceMountAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['parent_platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_DeviceMountAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_unmount_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_DeviceUnmountAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_DeviceUnmountAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_configuration_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('action_type_name', sa.String(length=256), nullable=False),
    sa.Column('action_type_uri', sa.String(length=256), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_GenericConfigurationAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_GenericConfigurationAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform_mount_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('parent_platform_id', sa.Integer(), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('offset_x', sa.Float(), nullable=True),
    sa.Column('offset_y', sa.Float(), nullable=True),
    sa.Column('offset_z', sa.Float(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_PlatformMountAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['parent_platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_PlatformMountAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform_unmount_action',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('configuration_id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['configuration_id'], ['configuration.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_PlatformUnmountAction_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_PlatformUnmountAction_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generic_configuration_action_attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['generic_configuration_action.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['configuration_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('generic_configuration_action_attachment')
    op.drop_table('platform_unmount_action')
    op.drop_table('platform_mount_action')
    op.drop_table('generic_configuration_action')
    op.drop_table('device_unmount_action')
    op.drop_table('device_mount_action')
    op.drop_table('configuration_static_location_end_action')
    op.drop_table('configuration_static_location_begin_action')
    op.drop_table('configuration_dynamic_location_end_action')
    op.drop_table('configuration_dynamic_location_begin_action')
    op.drop_table('configuration_attachment')
    op.drop_table('platform_software_update_action_attachment')
    op.drop_table('generic_platform_action_attachment')
    op.drop_table('generic_device_action_attachment')
    op.drop_table('device_software_update_action_attachment')
    op.drop_table('device_property_calibration')
    op.drop_table('device_calibration_attachment')
    op.drop_table('platform_software_update_action')
    op.drop_table('generic_platform_action')
    op.drop_table('generic_device_action')
    op.drop_table('device_software_update_action')
    op.drop_table('device_calibration_action')
    # ### end Alembic commands ###

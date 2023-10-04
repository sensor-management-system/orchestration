# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Update the uri entries so that it points to the central cv.

This script is only for the institute for that we take the complete
data of the CV to the central instance.

There is no mapping in this migration that would be required if
we enter entries later (with different ids).

Revision ID: 426aab825deb
Revises: 393a55ad59db
Create Date: 2023-06-27 05:36:07.802916

"""
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "426aab825deb"
down_revision = "ad264dbfbff0"
branch_labels = None
depends_on = None


def upgrade():
    """Switch the uri entries to the central cv."""
    tables = {
        # configuration has no uri field
        # configuration_attachment has no uri field
        "configuration_contact_role": [
            "role_uri",
        ],
        # configuration_custom_field has no uri field
        "configuration_dynamic_location_begin_action": [
            "elevation_datum_uri",
        ],
        "configuration_parameter": [
            "unit_uri",
        ],
        "configuration_static_location_begin_action": [
            "elevation_datum_uri",
        ],
        # contact has no uri field
        # custom_field has no uri field
        "datastream_link": [
            "license_uri",
        ],
        "device": [
            "manufacturer_uri",
            "device_type_uri",
            "status_uri",
        ],
        # device_attachment has no uri field
        # device_calibration_action has no uri field
        # device_calibration_attachment has no uri field
        "device_contact_role": [
            "role_uri",
        ],
        # device_mount_action has no uri field
        "device_parameter": ["unit_uri"],
        # + same for configuration_parameter & platform_parameter
        "device_property": [
            "unit_uri",
            "compartment_uri",
            "property_uri",
            "sampling_media_uri",
            "resolution_unit_uri",
            "aggregation_type_uri",
        ],
        # device_property_calibration has no uri field
        "device_software_update_action": [
            "software_type_uri",
        ],
        # device_software_update_action_attachment has no uri field
        "generic_configuration_action": [
            "action_type_uri",
        ],
        # generic_configuration_action_attachment has no uri field
        "generic_device_action": [
            "action_type_uri",
        ],
        # generic_device_action_attachment has no uri field
        "generic_platform_action": [
            "action_type_uri",
        ],
        # generic_platform_action_attachment has no uri field
        "platform": [
            "manufacturer_uri",
            "platform_type_uri",
            "status_uri",
        ],
        # platform_attachment has no uri field
        "platform_contact_role": [
            "role_uri",
        ],
        "platform_parameter": [
            "unit_uri",
        ],
        # platform_mount_action has no uri field
        "platform_software_update_action": [
            "software_type_uri",
        ],
        # platform_software_update_action_attachment has no uri field
        "site": [
            "elevation_datum_uri",
            "site_type_uri",
            "site_usage_uri",
        ],
        "site_contact_role": [
            "role_uri",
        ],
        # tsm_endpint has no uri field
        # user has no uri field
    }
    server_paths_to_replace = [
        "https://webapp.ufz.de/sms/cv",
        "https://webapp-stage.intranet.de/sms/cv",
        "https://sensors.gfz-potsdam.de/cv",
        "https://rz-vm64.gfz-potsdam.de/cv",
        "https://sms.atmohub.kit.edu/cv",
        "https://ibg3sms.ibg.kfa-juelich.de/cv",
        # And for the GFZ staging-develop
        "http://rz-vm64.gfz-potsdam.de/cv",
        "https://rz-vm64.gfz-potsdam.de:3000/cv",
        # And in case the ufz paths are http only
        "http://webapp.ufz.de/sms/cv",
        "http://webapp-stage.intranet.de/sms/cv",
    ]
    target = "https://sms-cv.helmholtz.cloud/sms/cv"

    conn = op.get_bind()
    for table, columns in tables.items():
        for column in columns:
            for server in server_paths_to_replace:
                update = f"update {table} set {column} = replace({column}, '{server}', '{target}')"
                conn.execute(text(update))


def downgrade():
    """Don't do anything."""
    pass

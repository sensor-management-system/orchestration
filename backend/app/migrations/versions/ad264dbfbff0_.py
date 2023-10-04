# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Map some of the KIT ids to some other ones that are used for UFZ CV.

The UFZ CV is used as the base for the central CV, so we map the entries
to accoding ids that they will have at the end of the central CV migration.

Revision ID: ad264dbfbff0
Revises: 426aab825deb
Create Date: 2023-09-29 07:07:43.391882

"""
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "ad264dbfbff0"
down_revision = "516b983a7213"
branch_labels = None
depends_on = None


def upgrade():
    """
    Map ids of the KIT CV to the accoding one on the UFZ CV.

    We still use the KIT URL at the end, as we switch to the central
    CV in the next step anyway.
    """
    conn = op.get_bind()

    kit_cv_base_url = "https://sms.atmohub.kit.edu/cv/api/v1/"

    manufacturer_mapping = {
        # from: to,
        "69": "167",  # Styx Neutronica
        "70": "168",  # HT Hydrotechnik
    }

    for table in ["device", "platform"]:
        for from_id, to_id in manufacturer_mapping.items():
            update_query = f"""
            update {table}
            set manufacturer_uri = '{kit_cv_base_url}/manufacturers/{to_id}/'
            where manufacturer_uri = '{kit_cv_base_url}/manufacturers/{from_id}/'
            """
            conn.execute(text(update_query))

    # And we need to map the entry for the sampling medium 'air'.
    # The KIT has a completely new entry, while the UFZ renamed
    # weather to air.
    from_id_air = 21
    to_id_air = 9

    update_query_samping_medium_air = f"""
    update device_property
    set samping_media_uri = '{kit_cv_base_url}/samplingmedia/{from_id_air}/'
    where samping_media_uri = '{kit_cv_base_url}/samplingmedia/{to_id_air}/'
    """

    conn.execute(text(update_query_samping_medium_air))


def downgrade():
    """Don't do anything."""
    pass

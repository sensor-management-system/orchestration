# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Update two columns that were set to wrong uri values, due to a bug in the cv update manage.py call.

Revision ID: 3583b07a3c98
Revises: c5f2c6fc971e
Create Date: 2026-04-28 05:40:24.787505

"""
import os

import requests
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3583b07a3c98"
down_revision = "c5f2c6fc971e"
branch_labels = None
depends_on = None


def upgrade():
    """Update the db for wrongly set uri values (that equal the name entry)."""
    cv_url = os.environ.get("CV_URL")
    if not cv_url:
        return
    # The cv_url_prod is a helper, so that we have all the time
    # an url that can be reached also from within the SMS backend container.
    cv_url_prod = cv_url
    if cv_url.startswith("http://localhost"):
        cv_url_prod = "https://sms-cv.helmholtz.cloud/sms/cv/api/v1"

    cv_status_url = f"{cv_url_prod}/equipmentstatus/"
    cv_status_response = requests.get(
        cv_status_url,
        {
            "page[size]": 10_000,
        },
    )
    cv_status_response.raise_for_status()
    status_uri_index = {
        e["attributes"]["term"]: e["links"]["self"]
        for e in cv_status_response.json()["data"]
    }

    cv_site_usage_url = f"{cv_url_prod}/siteusages/"
    cv_site_usage_response = requests.get(
        cv_site_usage_url,
        {
            "page[size]": 10_000,
        },
    )
    cv_site_usage_response.raise_for_status()
    site_usage_uri_index = {
        e["attributes"]["term"]: e["links"]["self"]
        for e in cv_site_usage_response.json()["data"]
    }

    connection = op.get_bind()

    # 1. Fetch the CV
    # 2. Extract the ids for the wrongly set entries
    device_status_select = """
    select id, status_uri
    from device
    where status_uri is not null
    and status_uri <> ''
    and status_uri = status_name
    """
    device_id_and_status_entries = []
    for res in connection.execute(sa.text(device_status_select)).fetchall():
        device_id = res["id"]
        status_uri = res["status_uri"]
        device_id_and_status_entries.append((device_id, status_uri))

    for device_id, status_uri in device_id_and_status_entries:
        fixed_status_uri = status_uri_index.get(status_uri, None)
        if fixed_status_uri:
            device_status_update_command = """
            update device
            set status_uri = :status_uri
            where id = :id
            """
            connection.execute(
                sa.text(device_status_update_command),
                {"status_uri": fixed_status_uri, "id": device_id},
            )

    site_usage_select = """
    select id, site_usage_uri
    from site
    where site_usage_uri is not null
    and site_usage_uri <> ''
    and site_usage_uri = site_usage_name
    """
    site_id_and_usage_entries = []
    for res in connection.execute(sa.text(site_usage_select)).fetchall():
        site_id = res["id"]
        site_usage_uri = res["site_usage_uri"]
        site_id_and_usage_entries.append((site_id, site_usage_uri))

    for site_id, site_usage_uri in site_id_and_usage_entries:
        fixed_site_uri = site_usage_uri_index.get(site_usage_uri, None)
        if fixed_site_uri:
            site_usage_update_command = """
            update site
            set site_usage_uri = :site_usage_uri
            where id = :id
            """
            connection.execute(
                sa.text(site_usage_update_command),
                {"site_usage_uri": fixed_site_uri, "id": site_id},
            )


def downgrade():
    """There is nothing to do here."""
    pass

# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add the aggregation types from the measured quantities (second try).

Revision ID: 37fe18314572
Revises: 3ba235b20231
Create Date: 2023-07-12 13:29:18.886822

"""
import dataclasses
import logging
import os
import time
import typing

import requests
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "37fe18314572"
down_revision = "3ba235b20231"
branch_labels = None
depends_on = None


@dataclasses.dataclass
class DeviceProperty:
    """Class to handle a subset of the device property data."""

    id: int
    property_uri: typing.Optional[str]
    property_name: typing.Optional[str]
    aggregation_type_uri: typing.Optional[str]
    aggregation_type_name: typing.Optional[str]


def wait_for(url, max_try_count=10, sleep_seconds=10):
    """Wait for an endpoint to be reachable."""
    accessible = False
    try_count = 0

    while not accessible:
        try:
            result = requests.get(url)
            result.raise_for_status()
            accessible = True
        except Exception as e:
            try_count += 1
            time.sleep(sleep_seconds)
            if try_count > max_try_count:
                raise e


def without_protocol(url):
    """
    Remove the protocol from the url.

    Transforms https://gfz-potsdam.de to gfz-potsdam.de
    """
    return url.split("://", 1)[-1]


def upgrade():
    """Do the database changes."""
    cv_url = os.environ.get("CV_URL")
    # The cv_url_prod is a helper, so that we have all the time
    # an url that can be reached also from within the SMS backend container.
    cv_url_prod = cv_url
    if cv_url.startswith("https://localhost"):
        cv_url_prod = "https://sensors.gfz-potsdam.de/cv/api/v1"

    conn = op.get_bind()

    # Extract the properties.
    device_properties = []
    res = conn.execute(
        "SELECT id, property_name, property_uri, aggregation_type_uri, aggregation_type_name from device_property"
    )
    for row in res:
        device_properties.append(
            DeviceProperty(
                id=row["id"],
                property_uri=row["property_uri"],
                property_name=row["property_name"],
                aggregation_type_uri=row["aggregation_type_uri"],
                aggregation_type_name=row["aggregation_type_name"],
            )
        )

    for dp in device_properties:
        # We want to run the update only if there are some conditions:
        # 1) We have a property uri from our own CV.
        # 2) we don't have an aggregtion type yet.
        if (
            dp.property_uri
            and not dp.aggregation_type_name
            and without_protocol(dp.property_uri).startswith(without_protocol(cv_url))
        ):

            aggregation_type_uri = dp.aggregation_type_uri
            aggregation_type_name = dp.aggregation_type_name

            # Ensure we can reach the CV already.
            # For the first time it may take some minutes, but this is ok
            # as long as we can reach the CV then.
            wait_for(cv_url_prod, max_try_count=20, sleep_seconds=20)

            try:
                # First we ask about the data of the measured quantity.
                # We can extract the id of the aggregation type.
                response = requests.get(dp.property_uri.replace(cv_url, cv_url_prod))
                response.raise_for_status()
                property_data = response.json()
                aggregation_type_id = property_data["data"]["relationships"][
                    "aggregation_type"
                ]["data"]["id"]

                # Then we can construct the uri for the aggregation type.
                # And we can query the CV for its data.
                aggregation_type_uri = (
                    f"{cv_url}/aggregationtypes/{aggregation_type_id}"
                )

                response = requests.get(
                    aggregation_type_uri.replace(cv_url, cv_url_prod)
                )
                response.raise_for_status()
                aggregation_type_data = response.json()

                # We use the term as name.
                aggregation_type_name = aggregation_type_data["data"]["attributes"][
                    "term"
                ]
            except Exception as e:
                # In case anything goes wrong here, we just want to inform.
                # There is no way to extract the aggregation types if we
                # can't access the CV for the entries.
                # However, it should not block other device properties that
                # we may can update. So we just skip it & try the next one.
                logging.info(e)
                logging.info(
                    f"Error on fetching for device property id={dp.id} - skipping"
                )

            if (
                aggregation_type_uri != dp.aggregation_type_uri
                or aggregation_type_name != dp.aggregation_type_name
            ):
                # Run the update query only in case we have extracted
                # something new.
                conn.execute(
                    sa.text(
                        """
                        update device_property
                        set aggregation_type_uri = :aggregation_type_uri,
                        aggregation_type_name = :aggregation_type_name
                        where id=:id
                        """
                    ),
                    id=dp.id,
                    aggregation_type_uri=aggregation_type_uri,
                    aggregation_type_name=aggregation_type_name,
                )


def downgrade():
    """Undo the database structure changes."""
    # There are no structure changes, so we pass...
    pass

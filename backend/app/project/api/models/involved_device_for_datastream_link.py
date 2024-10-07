# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Class to model an additionally involved device for a datastream link."""

import datetime
import math

from .base_model import db


class InvolvedDeviceForDatastreamLink(db.Model):
    """Involved device for a datastream link."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        foreign_keys=[device_id],
        backref=db.backref(
            "involved_in_datastreams",
            cascade="save-update, merge",
        ),
    )
    datastream_link_id = db.Column(
        db.Integer, db.ForeignKey("datastream_link.id"), nullable=False
    )
    datastream_link = db.relationship(
        "DatastreamLink",
        foreign_keys=[datastream_link_id],
        backref=db.backref(
            "involved_devices",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    order_index = db.Column(
        db.BigInteger,
        nullable=False,
        default=lambda _: math.floor(datetime.datetime.now().timestamp() * 1000),
    )

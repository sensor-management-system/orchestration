# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Class for a device image."""

import datetime
import math

from .base_model import db
from .mixin import AuditMixin


class DeviceImage(db.Model, AuditMixin):
    """Device image class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        foreign_keys=[device_id],
        backref=db.backref(
            "device_images", cascade="save-update, merge, delete, delete-orphan"
        ),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("device_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "DeviceAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("device_images"),
    )
    order_index = db.Column(
        db.BigInteger,
        nullable=False,
        # The primary idea was to use the id value and multiply it with 10
        # to have a default order id.
        # Howevr, the id is set **after** we set the default values (as
        # it comes from the database).
        # So we use the timestamp instead.
        default=lambda _: math.floor(datetime.datetime.now().timestamp() * 1000),
    )

    def get_parent(self):
        """Get the device (as it belongs to it)."""
        return self.device

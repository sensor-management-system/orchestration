# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Class for the export control attachment."""
from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import db
from .mixin import AuditMixin


class ExportControlAttachment(db.Model, AuditMixin):
    """Export control attachment class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    internal_url = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_export_control_only = db.Column(db.Boolean, default=True)

    manufacturer_model_id = db.Column(
        db.Integer, db.ForeignKey("manufacturer_model.id"), nullable=False
    )
    manufacturer_model = db.relationship(
        "ManufacturerModel",
        backref=db.backref(
            "export_control_attachments",
        ),
    )

    @hybrid_property
    def is_upload(self):
        """Return True if the internal url is set."""
        return bool(self.internal_url)

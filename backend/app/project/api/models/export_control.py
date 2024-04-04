# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model for the export control."""

from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class ExportControl(db.Model, AuditMixin, IndirectSearchableMixin):
    """Entity to store export control information."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dual_use = db.Column(db.Boolean, nullable=True)
    export_control_classification_number = db.Column(db.String(256), nullable=True)
    customs_tariff_number = db.Column(db.String(256), nullable=True)
    additional_information = db.Column(db.Text, nullable=True)
    internal_note = db.Column(db.Text, nullable=True)

    manufacturer_model_id = db.Column(
        db.Integer, db.ForeignKey("manufacturer_model.id"), nullable=False
    )
    manufacturer_model = db.relationship(
        "ManufacturerModel",
        backref=db.backref(
            "export_control",
            uselist=False,
        ),
    )

    def get_parent_search_entities(self):
        """Return the device as parent search entity."""
        return [self.manufacturer_model]

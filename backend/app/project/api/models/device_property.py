# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model for device properties."""


from ..models.device import Device
from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class DeviceProperty(db.Model, IndirectSearchableMixin, AuditMixin):
    """DeviceProperty class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    measuring_range_min = db.Column(db.Float(), nullable=True)
    measuring_range_max = db.Column(db.Float(), nullable=True)
    failure_value = db.Column(db.Float(), nullable=True)
    accuracy = db.Column(db.Float(), nullable=True)
    accuracy_unit_uri = db.Column(db.String(256), nullable=True)
    accuracy_unit_name = db.Column(db.String(256), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    unit_uri = db.Column(db.String(256), nullable=True)  # CV
    unit_name = db.Column(db.String(256), nullable=True)  # CV
    compartment_uri = db.Column(db.String(256), nullable=True)
    compartment_name = db.Column(db.String(256), nullable=True)
    property_uri = db.Column(db.String(256), nullable=True)
    property_name = db.Column(db.String(256), nullable=False)
    sampling_media_uri = db.Column(db.String(256), nullable=True)
    sampling_media_name = db.Column(db.String(256), nullable=True)
    resolution = db.Column(db.Float(), nullable=True)
    resolution_unit_uri = db.Column(db.String(256), nullable=True)
    resolution_unit_name = db.Column(db.String(256), nullable=True)
    aggregation_type_uri = db.Column(db.String(256), nullable=True)
    aggregation_type_name = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        Device,
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref(
            "device_properties", cascade="save-update, merge, delete, delete-orphan"
        ),
    )

    def to_search_entry(self):
        """Convert the model to a dict to store it in the full text search."""
        # to be included in devices
        return {
            "label": self.label,
            "unit_name": self.unit_name,
            "unit_uri": self.unit_uri,
            "compartment_name": self.compartment_name,
            "compartment_uri": self.compartment_uri,
            "property_name": self.property_name,
            "property_uri": self.property_uri,
            "sample_medium_name": self.sampling_media_name,
            "sample_medium_uri": self.sampling_media_uri,
            "accuracy_unit_name": self.accuracy_unit_name,
            "accuracy_unit_uri": self.accuracy_unit_uri,
            "resolution_unit_name": self.resolution_unit_name,
            "resolution_unit_uri": self.resolution_unit_uri,
            "aggregation_type_name": self.aggregation_type_name,
            "aggregation_type_uri": self.aggregation_type_uri,
            "description": self.description,
        }

    def get_parent_search_entities(self):
        """Return the device as parent search entity."""
        return [self.device]

    def get_parent(self):
        """Return parent object."""
        return self.device

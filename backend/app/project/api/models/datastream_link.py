# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for the datastream links."""

from .base_model import db
from .mixin import AuditMixin


class DatastreamLink(db.Model, AuditMixin):
    """
    Link of a device property to a datastream of a tsm system.

    The idea here is to create a link between a device property for a device
    that is used in a configuration with really measured data.
    Those data are hosted in external systems (we call them "Time Series
    Management Systems").
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # We link the device property of a specific mount (in a configuration)
    device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=False
    )
    device_property = db.relationship(
        "DeviceProperty", backref=db.backref("datastream_links")
    )
    device_mount_action_id = db.Column(
        db.Integer, db.ForeignKey("device_mount_action.id"), nullable=False
    )
    device_mount_action = db.relationship(
        "DeviceMountAction", backref=db.backref("datastream_links")
    )
    # And we link the datastream id of a specific instance of a
    # time series management system.
    #
    # We follow a hierarchy here:
    # - a datasource gives a list of things (like stations)
    # - a thing gives a list of datastreams (like airtemperature on a specific station)
    # For thing & datastream we follow the naming as it is done in
    # the sensor things api (STA).
    #
    # Datasources allow us to handle different databases.
    # And in case we want to support linking to different tsm systems overall
    # We also store a tsm endpoint entry (to support multiple centres).
    # And we save the names of the datasources, things & datastreams
    # to display them in the sms easily.
    tsm_endpoint_id = db.Column(
        db.Integer, db.ForeignKey("tsm_endpoint.id"), nullable=True
    )
    tsm_endpoint = db.relationship(
        "TsmEndpoint", backref=db.backref("datastream_links")
    )
    datasource_id = db.Column(db.String(256), nullable=False)
    datasource_name = db.Column(db.String(256), nullable=True)
    thing_id = db.Column(db.String(256), nullable=False)
    thing_name = db.Column(db.String(256), nullable=True)
    datastream_id = db.Column(db.String(256), nullable=False)
    datastream_name = db.Column(db.String(256), nullable=True)
    # In rare cases it is possible that the very same datastream could
    # be uses to measure different quantities on different stations.
    # So we need to allow further restrictions for the time in that such
    # a datastream link is valid.
    # If no other values are given, then we can use the dates from the
    # mount itself (so those fields here are completely optional).
    begin_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    # And we add some fields that may become interesting when
    # bringing it in the direction of STA.
    license_uri = db.Column(db.String(256), nullable=True)
    license_name = db.Column(db.String(256), nullable=True)
    # Aggregation period in seconds.
    aggregation_period = db.Column(db.Float(), nullable=True)

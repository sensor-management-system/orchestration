# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Controller class to extract parameter values."""

import dateutil.parser
from flask import g, request
from flask_rest_jsonapi import ResourceList

from ..helpers.date_time_range import DateTimeRange
from ..helpers.errors import (
    BadRequestError,
    ForbiddenError,
    MethodNotAllowed,
    NotFoundError,
    UnauthorizedError,
)
from ..models import Configuration
from ..models.base_model import db
from ..permissions.rules import can_see


class ControllerConfigurationParameterValues(ResourceList):
    """Controller class for the extraction of configuration parameter values."""

    def get(self, *args, **kwargs):
        """Return the list of parameters & their values at timepoint."""
        if "configuration_id" not in kwargs.keys():
            raise NotFoundError("No id.")
        configuration_id = kwargs["configuration_id"]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).one_or_none()
        )
        if not configuration:
            raise NotFoundError("No configuration with the given id.")
        if not can_see(configuration):
            if not g.user:
                raise UnauthorizedError("Authentication required.")
            raise ForbiddenError("Authentication required.")
        if "timepoint" not in request.args.keys():
            raise BadRequestError("timepoint parameter required")
        try:
            timepoint = dateutil.parser.parse(request.args["timepoint"])
        except dateutil.parser.ParserError:
            raise BadRequestError("timepoint must be ISO 8601")

        result = []
        for parameter in configuration.configuration_parameters:
            latest_action = None
            for value_change in parameter.configuration_parameter_value_change_actions:
                if value_change.date <= timepoint:
                    if latest_action is None or latest_action.date < value_change.date:
                        latest_action = value_change
            value = None
            if latest_action is not None:
                value = latest_action.value

            result.append(
                {
                    "id": str(parameter.id),
                    "type": "configuration_parameter",
                    "attributes": {
                        "label": parameter.label,
                        "value": value,
                        "unit_uri": parameter.unit_uri,
                        "unit_name": parameter.unit_name,
                    },
                }
            )
        for mount_action in configuration.device_mount_actions:
            mount_range = DateTimeRange(mount_action.begin_date, mount_action.end_date)
            if mount_range.overlaps_with(DateTimeRange(timepoint, timepoint)):
                device = mount_action.device
                for parameter in device.device_parameters:
                    latest_action = None
                    for value_change in parameter.device_parameter_value_change_actions:
                        if value_change.date <= timepoint:
                            if (
                                latest_action is None
                                or latest_action.date < value_change.date
                            ):
                                latest_action = value_change
                    value = None
                    if latest_action is not None:
                        value = latest_action.value

                    result.append(
                        {
                            "id": str(parameter.id),
                            "type": "device_parameter",
                            "attributes": {
                                "label": parameter.label,
                                "value": value,
                                "unit_uri": parameter.unit_uri,
                                "unit_name": parameter.unit_name,
                            },
                        }
                    )
        for mount_action in configuration.platform_mount_actions:
            mount_range = DateTimeRange(mount_action.begin_date, mount_action.end_date)
            if mount_range.overlaps_with(DateTimeRange(timepoint, timepoint)):
                platform = mount_action.platform
                for parameter in platform.platform_parameters:
                    latest_action = None
                    for (
                        value_change
                    ) in parameter.platform_parameter_value_change_actions:
                        if value_change.date <= timepoint:
                            if (
                                latest_action is None
                                or latest_action.date < value_change.date
                            ):
                                latest_action = value_change
                    value = None
                    if latest_action is not None:
                        value = latest_action.value

                    result.append(
                        {
                            "id": str(parameter.id),
                            "type": "platform_parameter",
                            "attributes": {
                                "label": parameter.label,
                                "value": value,
                                "unit_uri": parameter.unit_uri,
                                "unit_name": parameter.unit_name,
                            },
                        }
                    )

        return {
            "data": result,
        }

    def post(self, *args, **kwargs):
        """Don't allow the post request."""
        raise MethodNotAllowed("endpoint is readonly")

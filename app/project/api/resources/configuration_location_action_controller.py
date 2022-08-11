from flask import g, request

from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import (
    NotFoundError,
    UnauthorizedError,
)
from ..models import Configuration, ConfigurationStaticLocationBeginAction, ConfigurationDynamicLocationBeginAction
from ..models.base_model import db

from ..schemas.configuration_static_location_actions_schema import ConfigurationStaticLocationBeginActionSchema
from ..schemas.configuration_dynamic_location_actions_schema import ConfigurationDynamicLocationBeginActionSchema


class ControllerConfigurationLocationActionTimepoints(ResourceList):
    """Controller that returns a list of timepoints for the location actions."""

    def get(self, *args, **kwargs):
        if "configuration_id" not in kwargs.keys():
            raise NotFoundError("No id.")
        configuration_id = kwargs["configuration_id"]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).one_or_none()
        )
        if not configuration:
            raise NotFoundError("No configuration with the given id.")
        if configuration.is_internal:
            if not g.user:
                raise UnauthorizedError("Authentication required.")

        include_ends = request.args.get("include_ends", 'false') in ['true', "TRUE", "True"]
        static_location_schema = ConfigurationStaticLocationBeginActionSchema()
        dynamic_location_schema = ConfigurationDynamicLocationBeginActionSchema()

        static_locations = db.session.query(ConfigurationStaticLocationBeginAction).filter(
            ConfigurationStaticLocationBeginAction.configuration_id == configuration_id,
        )
        dynamic_locations = db.session.query(ConfigurationDynamicLocationBeginAction).filter(
            ConfigurationDynamicLocationBeginAction.configuration_id == configuration_id,
        )

        dates_with_labels = list()
        for static_location in static_locations:
            dates_with_labels.append(
                {
                    "timepoint": static_location.begin_date,
                    "type": "configuration_static_location_begin",
                    "attributes": static_location_schema.dump(static_location)["data"]["attributes"]
                }
            )
            if include_ends and static_location.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": static_location.end_date,
                        "type": "configuration_static_location_end",
                        "attributes": static_location_schema.dump(static_location)["data"]["attributes"]
                    }
                )

        for dynamic_location in dynamic_locations:
            dates_with_labels.append(
                {
                    "timepoint": dynamic_location.begin_date,
                    "type": "configuration_dynamic_location_begin",
                    "attributes": dynamic_location_schema.dump(dynamic_location)["data"]["attributes"]
                }
            )
            if include_ends and dynamic_location.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": dynamic_location.end_date,
                        "type": "configuration_dynamic_location_end",
                        "attributes": dynamic_location_schema.dump(dynamic_location)["data"]["attributes"]
                    }
                )
        dates_with_labels.sort(key=lambda x: x["timepoint"])

        return dates_with_labels

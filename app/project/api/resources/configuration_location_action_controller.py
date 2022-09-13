"""Custom controller classes to work with location actions for configurations."""

from flask import g

from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import NotFoundError, UnauthorizedError
from ..models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
)
from ..models.base_model import db


class ControllerConfigurationLocationActionTimepoints(ResourceList):
    """Controller that returns a list of timepoints for the location actions."""

    def get(self, *args, **kwargs):
        """Return the response for the GET request."""
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

        static_locations = db.session.query(
            ConfigurationStaticLocationBeginAction
        ).filter(
            ConfigurationStaticLocationBeginAction.configuration_id == configuration_id,
        )
        dynamic_locations = db.session.query(
            ConfigurationDynamicLocationBeginAction
        ).filter(
            ConfigurationDynamicLocationBeginAction.configuration_id
            == configuration_id,
        )

        dates_with_labels = list()
        for static_location in static_locations:
            dates_with_labels.append(
                {
                    "timepoint": static_location.begin_date,
                    "id": str(static_location.id),
                    "type": "configuration_static_location_begin",
                }
            )
            if static_location.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": static_location.end_date,
                        "id": str(static_location.id),
                        "type": "configuration_static_location_end",
                    }
                )

        for dynamic_location in dynamic_locations:
            dates_with_labels.append(
                {
                    "timepoint": dynamic_location.begin_date,
                    "id": str(dynamic_location.id),
                    "type": "configuration_dynamic_location_begin",
                }
            )
            if dynamic_location.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": dynamic_location.end_date,
                        "id": str(dynamic_location.id),
                        "type": "configuration_dynamic_location_end",
                    }
                )
        dates_with_labels.sort(key=lambda x: x["timepoint"])

        return dates_with_labels

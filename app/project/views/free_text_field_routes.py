"""
Endpoints to query for text fields only.

Idea is to provide endpoints that can be used to help users
in the frontend with entries that they already wrote - and that
are not part of a controlled vocabulary.
"""

from abc import ABC

from flask import Blueprint, g

from ..api.helpers.errors import ErrorResponse, UnauthorizedError
from ..api.models import (
    Configuration,
    ConfigurationCustomField,
    CustomField,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DeviceSoftwareUpdateAction,
    GenericConfigurationAction,
    GenericDeviceAction,
    GenericPlatformAction,
    Platform,
    PlatformSoftwareUpdateAction,
    Site,
)
from ..api.models.base_model import db
from ..config import env
from ..restframework.views.classbased import class_based_view

free_text_field_routes = Blueprint(
    "free_text_field_routes",
    __name__,
    url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1"),
)


class AbstractFreeTextFieldEndpoint(ABC):
    """
    Abstract base class to share the query logic for all the endpoints here.

    The main idea is always the same: Make a distinct query for one field
    without further filters & return the list of them.
    """

    def __call__(self):
        """
        Run the query & return the list on a data entry.

        Structure is always the same:

        {
            "data": ["entry1", "entry2", ...]
        }

        The query relies on the implementing class to provive a field entry
        that points to the exact column that we want to query.
        """
        try:
            if not g.user:
                raise UnauthorizedError("Login required.")
            result_list = [
                x[0]
                for x in db.session.query(self.__class__.field)
                .distinct()
                .order_by(self.__class__.field)
                if x[0]
            ]
            result = {"data": result_list}
            return result
        except ErrorResponse as e:
            return e.respond()


@free_text_field_routes.route("/controller/configuration-labels", methods=["GET"])
@class_based_view
class ConfigurationLabelEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct configuration labels."""

    field = Configuration.label


@free_text_field_routes.route(
    "/controller/configuration-custom-field-keys", methods=["GET"]
)
@class_based_view
class ConfigurationCustomFieldKeyEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct configuration custom field keys."""

    field = ConfigurationCustomField.key


@free_text_field_routes.route(
    "/controller/configuration-custom-field-values", methods=["GET"]
)
@class_based_view
class ConfigurationCustomFieldValueEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct configuration custom field values."""

    field = ConfigurationCustomField.value


@free_text_field_routes.route(
    "/controller/device-calibration-action-descriptions", methods=["GET"]
)
@class_based_view
class DeviceCalibrationActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device calibration action descriptions."""

    field = DeviceCalibrationAction.description


@free_text_field_routes.route(
    "/controller/device-calibration-action-formulas", methods=["GET"]
)
@class_based_view
class DeviceCalibrationActionFormulaEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device calibration action formulas."""

    field = DeviceCalibrationAction.formula


@free_text_field_routes.route("/controller/device-custom-field-keys", methods=["GET"])
@class_based_view
class CustomFieldKeyEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct custom field keys."""

    field = CustomField.key


@free_text_field_routes.route("/controller/device-custom-field-values", methods=["GET"])
@class_based_view
class CustomFieldValueEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct custom field values."""

    field = CustomField.value


@free_text_field_routes.route("/controller/device-long-names", methods=["GET"])
@class_based_view
class DeviceLongNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device long names."""

    field = Device.long_name


@free_text_field_routes.route("/controller/device-manufacturer-names", methods=["GET"])
@class_based_view
class DeviceManufacturerNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device manufacturer names."""

    field = Device.manufacturer_name


@free_text_field_routes.route("/controller/device-property-labels", methods=["GET"])
@class_based_view
class DevicePropertyLabelEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device property labels."""

    field = DeviceProperty.label


@free_text_field_routes.route("/controller/device-short-names", methods=["GET"])
@class_based_view
class DeviceShortNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device short names."""

    field = Device.short_name


@free_text_field_routes.route(
    "/controller/device-software-update-action-descriptions", methods=["GET"]
)
@class_based_view
class DeviceSoftwareUpdateActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device software update action descriptions."""

    field = DeviceSoftwareUpdateAction.description


@free_text_field_routes.route(
    "/controller/device-software-update-action-repository-urls", methods=["GET"]
)
@class_based_view
class DeviceSoftwareUpdateActionRepositoryUrlEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device software update action repository urls."""

    field = DeviceSoftwareUpdateAction.repository_url


@free_text_field_routes.route(
    "/controller/generic-configuration-action-descriptions", methods=["GET"]
)
@class_based_view
class GenericConfigurationActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct configuration action descriptions."""

    field = GenericConfigurationAction.description


@free_text_field_routes.route(
    "/controller/generic-device-action-descriptions", methods=["GET"]
)
@class_based_view
class GenericDeviceActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device action descriptions."""

    field = GenericDeviceAction.description


@free_text_field_routes.route(
    "/controller/generic-platform-action-descriptions", methods=["GET"]
)
@class_based_view
class GenericPlatformActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform action descriptions."""

    field = GenericPlatformAction.description


@free_text_field_routes.route("/controller/platform-long-names", methods=["GET"])
@class_based_view
class PlatformLongNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform long names."""

    field = Platform.long_name


@free_text_field_routes.route(
    "/controller/platform-manufacturer-names", methods=["GET"]
)
@class_based_view
class PlatformManufacturerNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform manufacturer names."""

    field = Platform.manufacturer_name


@free_text_field_routes.route("/controller/platform-short-names", methods=["GET"])
@class_based_view
class PlatformShortNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform short names."""

    field = Platform.short_name


@free_text_field_routes.route(
    "/controller/platform-software-update-action-descriptions", methods=["GET"]
)
@class_based_view
class PlatformSoftwareUpdateActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform software update action descriptions."""

    field = PlatformSoftwareUpdateAction.description


@free_text_field_routes.route(
    "/controller/platform-software-update-action-repository-urls", methods=["GET"]
)
@class_based_view
class PlatformSoftwareUpdateActionRepositoryUrlEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform software update action repository urls."""

    field = PlatformSoftwareUpdateAction.repository_url


@free_text_field_routes.route("/controller/site-buildings", methods=["GET"])
@class_based_view
class SiteBuildingEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site buildings."""

    field = Site.building


@free_text_field_routes.route("/controller/site-cities", methods=["GET"])
@class_based_view
class SiteCityEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site cities."""

    field = Site.city


@free_text_field_routes.route("/controller/site-countries", methods=["GET"])
@class_based_view
class SiteCountryEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site countries."""

    field = Site.country


@free_text_field_routes.route("/controller/site-labels", methods=["GET"])
@class_based_view
class SiteLabelEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site labels."""

    field = Site.label


@free_text_field_routes.route("/controller/site-rooms", methods=["GET"])
@class_based_view
class SiteRoomEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site rooms."""

    field = Site.room


@free_text_field_routes.route("/controller/site-streets", methods=["GET"])
@class_based_view
class SiteStreetEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site streets."""

    field = Site.street


@free_text_field_routes.route("/controller/site-street-numbers", methods=["GET"])
@class_based_view
class SiteStreetNumberEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site street numbers."""

    field = Site.street_number


@free_text_field_routes.route("/controller/site-zip-codes", methods=["GET"])
@class_based_view
class SiteZipCodeEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct site zip codes."""

    field = Site.zip_code

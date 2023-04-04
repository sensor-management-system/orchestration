"""
Endpoints to query for text fields only.

Idea is to provide endpoints that can be used to help users
in the frontend with entries that they already wrote - and that
are not part of a controlled vocabulary.
"""

from abc import ABC

from flask import Blueprint, g, request
from sqlalchemy import or_

from ..api.helpers.errors import ErrorResponse, UnauthorizedError
from ..api.models import (
    Configuration,
    ConfigurationCustomField,
    Contact,
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

    The configuration of the class is done with up to 4 fields on the
    class itself:

    field: This is the field that we want to extract.
    join_field: The field that we use to join to another table (if needed).
    is_private_field: The field that specifies if the entry is private or not.
                      This can be part of the joined table.
    created_by_id_field: The field that points to the user id that created that entry.
                         This points to the only user that can edit a private device/platform.
                         The field can be on the joined table.
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
                raise UnauthorizedError("Authentication required.")
            base_query = db.session.query(self.__class__.field)

            if getattr(self.__class__, "ignore_field", None):
                ignore_str = request.values.get("ignore", "")
                if ignore_str:
                    ignore_values = request.values.get("ignore", "").split(",")
                    base_query = base_query.filter(
                        self.__class__.ignore_field.not_in(ignore_values)
                    )

            if getattr(self.__class__, "filter_fields", None):
                filter_fields = self.__class__.filter_fields
                for query_param, field in filter_fields.items():
                    if request.values.get(query_param):
                        param_value = request.values[query_param]
                        base_query = base_query.filter(field == param_value)

            if getattr(self.__class__, "is_private_field", None) and getattr(
                self.__class__, "created_by_id_field", None
            ):
                # Maybe we must join to extract the right fields.
                if getattr(self.__class__, "join_field", None):
                    base_query = base_query.join(self.__class__.join_field)
                # Either it is not private or we have the owner.
                base_query = base_query.filter(
                    or_(
                        self.__class__.is_private_field.isnot(True),
                        self.__class__.created_by_id_field == g.user.id,
                    )
                )
            result_list = [
                x[0]
                for x in base_query.distinct().order_by(self.__class__.field)
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
    join_field = DeviceCalibrationAction.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route(
    "/controller/device-calibration-action-formulas", methods=["GET"]
)
@class_based_view
class DeviceCalibrationActionFormulaEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device calibration action formulas."""

    field = DeviceCalibrationAction.formula
    join_field = DeviceCalibrationAction.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-custom-field-keys", methods=["GET"])
@class_based_view
class CustomFieldKeyEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct custom field keys."""

    field = CustomField.key
    join_field = CustomField.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-custom-field-values", methods=["GET"])
@class_based_view
class CustomFieldValueEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct custom field values."""

    field = CustomField.value
    join_field = CustomField.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-long-names", methods=["GET"])
@class_based_view
class DeviceLongNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device long names."""

    field = Device.long_name
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-manufacturer-names", methods=["GET"])
@class_based_view
class DeviceManufacturerNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device manufacturer names."""

    field = Device.manufacturer_name
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-serial-numbers", methods=["GET"])
@class_based_view
class DeviceSerialNumberEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device serial numbers."""

    field = Device.serial_number
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id
    ignore_field = Device.id

    filter_fields = {
        "short_name": Device.short_name,
        "manufacturer_name": Device.manufacturer_name,
        "manufacturer_uri": Device.manufacturer_uri,
        "model": Device.model,
    }


@free_text_field_routes.route("/controller/device-property-labels", methods=["GET"])
@class_based_view
class DevicePropertyLabelEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device property labels."""

    field = DeviceProperty.label
    join_field = DeviceProperty.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route("/controller/device-short-names", methods=["GET"])
@class_based_view
class DeviceShortNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device short names."""

    field = Device.short_name
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route(
    "/controller/device-software-update-action-descriptions", methods=["GET"]
)
@class_based_view
class DeviceSoftwareUpdateActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device software update action descriptions."""

    field = DeviceSoftwareUpdateAction.description
    join_field = DeviceSoftwareUpdateAction.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route(
    "/controller/device-software-update-action-repository-urls", methods=["GET"]
)
@class_based_view
class DeviceSoftwareUpdateActionRepositoryUrlEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct device software update action repository urls."""

    field = DeviceSoftwareUpdateAction.repository_url
    join_field = DeviceSoftwareUpdateAction.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


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
    join_field = GenericDeviceAction.device
    is_private_field = Device.is_private
    created_by_id_field = Device.created_by_id


@free_text_field_routes.route(
    "/controller/generic-platform-action-descriptions", methods=["GET"]
)
@class_based_view
class GenericPlatformActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform action descriptions."""

    field = GenericPlatformAction.description
    join_field = GenericPlatformAction.platform
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


@free_text_field_routes.route("/controller/platform-long-names", methods=["GET"])
@class_based_view
class PlatformLongNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform long names."""

    field = Platform.long_name
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


@free_text_field_routes.route(
    "/controller/platform-manufacturer-names", methods=["GET"]
)
@class_based_view
class PlatformManufacturerNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform manufacturer names."""

    field = Platform.manufacturer_name
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


@free_text_field_routes.route("/controller/platform-serial-numbers", methods=["GET"])
@class_based_view
class PlatformSerialNumberEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform serial numbers."""

    field = Platform.serial_number
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id
    ignore_field = Platform.id

    filter_fields = {
        "short_name": Platform.short_name,
        "manufacturer_name": Platform.manufacturer_name,
        "manufacturer_uri": Platform.manufacturer_uri,
        "model": Platform.model,
    }


@free_text_field_routes.route("/controller/platform-short-names", methods=["GET"])
@class_based_view
class PlatformShortNameEndpoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform short names."""

    field = Platform.short_name
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


@free_text_field_routes.route(
    "/controller/platform-software-update-action-descriptions", methods=["GET"]
)
@class_based_view
class PlatformSoftwareUpdateActionDescriptionEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform software update action descriptions."""

    field = PlatformSoftwareUpdateAction.description
    join_field = PlatformSoftwareUpdateAction.platform
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


@free_text_field_routes.route(
    "/controller/platform-software-update-action-repository-urls", methods=["GET"]
)
@class_based_view
class PlatformSoftwareUpdateActionRepositoryUrlEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct platform software update action repository urls."""

    field = PlatformSoftwareUpdateAction.repository_url
    join_field = PlatformSoftwareUpdateAction.platform
    is_private_field = Platform.is_private
    created_by_id_field = Platform.created_by_id


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


@free_text_field_routes.route("/controller/contact-organizations", methods=["GET"])
@class_based_view
class ContactOrganizationEndPoint(AbstractFreeTextFieldEndpoint):
    """Endpoint for distinct contact organizations."""

    field = Contact.organization

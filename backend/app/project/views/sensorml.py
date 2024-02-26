# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Dirk Ecker <d.ecker@fz-juelich.de>
# - Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Routes for sensorML."""

import re
from xml.etree import ElementTree as ET

from flask import Blueprint, current_app, g, make_response, url_for
from flask_rest_jsonapi.exceptions import JsonApiException

from ..api.helpers.errors import (
    ErrorResponse,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from ..api.models import Configuration, Device, Platform, Site
from ..api.models.base_model import db
from ..api.permissions.rules import can_see
from ..config import env
from ..sensorml.converters import (
    ConfigurationConverter,
    DeviceConverter,
    PlatformConverter,
    SiteConverter,
)
from ..sensorml.models import gco, gmd, gml, sml, swe, xlink, xsi

sensor_ml_routes = Blueprint(
    "sensorml", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@sensor_ml_routes.route("/devices/<int:device_id>/sensorml", methods=["GET"])
def device_to_sensor_ml(device_id):
    """
    Export a device as sensorML.

    :param device_id: id
    :return: xml file
    """
    try:
        device = db.session.query(Device).filter_by(id=device_id).first()
        if device is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        if not can_see(device):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Device not accessable")
        cv_url = current_app.config["CV_URL"]
        physical_system = DeviceConverter(device, cv_url).sml_physical_system()
        xml_object = physical_system.to_xml()
        ET.register_namespace("gml", gml.namespace)
        ET.register_namespace("gco", gco.namespace)
        ET.register_namespace("gmd", gmd.namespace)
        ET.register_namespace("sml", sml.namespace)
        ET.register_namespace("swe", swe.namespace)
        ET.register_namespace("xlink", xlink.namespace)
        ET.register_namespace("xsi", xsi.namespace)
        schema_locations = {}
        for ns_element in [gml, gco, gmd, sml, swe, xlink, xsi]:
            if ns_element.schema_location:
                schema_locations[ns_element.namespace] = ns_element.schema_location

        xml_object.attrib[xsi.attrib("schemaLocation")] = " ".join(
            f"{k} {v}" for k, v in schema_locations.items()
        )
        header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
        text = header + ET.tostring(xml_object)
        response = make_response(text)
        response.headers["Content-Type"] = "application/xml"
        return response
    except ErrorResponse as e:
        return e.respond()
    except JsonApiException as e:
        return e.to_dict(), e.status


@sensor_ml_routes.route("/platforms/<int:platform_id>/sensorml", methods=["GET"])
def platform_to_sensor_ml(platform_id):
    """
    Export a platform as sensorML.

    :param platform_id: id
    :return: xml file
    """
    try:
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        if platform is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        if not can_see(platform):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Platform not accessable")
        cv_url = current_app.config["CV_URL"]
        physical_system = PlatformConverter(platform, cv_url).sml_physical_system()
        xml_object = physical_system.to_xml()
        ET.register_namespace("gml", gml.namespace)
        ET.register_namespace("gco", gco.namespace)
        ET.register_namespace("gmd", gmd.namespace)
        ET.register_namespace("sml", sml.namespace)
        ET.register_namespace("swe", swe.namespace)
        ET.register_namespace("xlink", xlink.namespace)
        ET.register_namespace("xsi", xsi.namespace)
        schema_locations = {}
        for ns_element in [gml, gco, gmd, sml, swe, xlink, xsi]:
            if ns_element.schema_location:
                schema_locations[ns_element.namespace] = ns_element.schema_location

        xml_object.attrib[xsi.attrib("schemaLocation")] = " ".join(
            f"{k} {v}" for k, v in schema_locations.items()
        )
        header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
        text = header + ET.tostring(xml_object)
        response = make_response(text)
        response.headers["Content-Type"] = "application/xml"
        return response
    except ErrorResponse as e:
        return e.respond()
    except JsonApiException as e:
        return e.to_dict(), e.status


@sensor_ml_routes.route(
    "/configurations/<int:configuration_id>/sensorml", methods=["GET"]
)
def configuration_to_sensor_ml(configuration_id):
    """
    Export a configuration as sensorML.

    :param configuration_id: id
    :return: xml file
    """
    try:
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        if configuration is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        if not can_see(configuration):
            if not g.user:
                raise UnauthorizedError("Authentication required.")
            raise ForbiddenError("Configuration not accessable")
        cv_url = current_app.config["CV_URL"]

        def url_lookup(element):

            if isinstance(element, Platform):
                return url_for(
                    "sensorml.platform_to_sensor_ml",
                    platform_id=element.id,
                    _external=True,
                )
            return url_for(
                "sensorml.device_to_sensor_ml", device_id=element.id, _external=True
            )

        physical_system = ConfigurationConverter(
            configuration,
            cv_url,
            url_lookup,
        ).sml_physical_system()
        xml_object = physical_system.to_xml()
        ET.register_namespace("gml", gml.namespace)
        ET.register_namespace("gco", gco.namespace)
        ET.register_namespace("gmd", gmd.namespace)
        ET.register_namespace("sml", sml.namespace)
        ET.register_namespace("swe", swe.namespace)
        ET.register_namespace("xlink", xlink.namespace)
        ET.register_namespace("xsi", xsi.namespace)
        schema_locations = {}
        for ns_element in [gml, gco, gmd, sml, swe, xlink, xsi]:
            if ns_element.schema_location:
                schema_locations[ns_element.namespace] = ns_element.schema_location

        xml_object.attrib[xsi.attrib("schemaLocation")] = " ".join(
            f"{k} {v}" for k, v in schema_locations.items()
        )
        header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
        text = header + ET.tostring(xml_object)

        # We need to make sure that our gml:ids are unique in the
        # overall document.
        # The strategy here to give different names - with `_dup_{n}`
        # suffix.
        dup_count = {}

        def gml_id_replacement(match):
            original_gml_id = match.group(1)
            if original_gml_id not in dup_count.keys():
                dup_count[original_gml_id] = 0
                return match.group()
            dup_count[original_gml_id] += 1
            result = f'gml:id="{original_gml_id}_dup_{dup_count[original_gml_id]}"'
            return result

        text = re.sub(r'gml:id="([^"]+)"', gml_id_replacement, text.decode())
        response = make_response(text)
        response.headers["Content-Type"] = "application/xml"
        return response
    except ErrorResponse as e:
        return e.respond()
    except JsonApiException as e:
        return e.to_dict(), e.status


@sensor_ml_routes.route("/sites/<int:site_id>/sensorml", methods=["GET"])
def site_to_sensor_ml(site_id):
    """
    Export a site as sensorML.

    :param site_id: id
    :return: xml file
    """
    try:
        site = db.session.query(Site).filter_by(id=site_id).first()
        if site is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        if not can_see(site):
            if not g.user:
                raise UnauthorizedError("Authentication required.")
            raise ForbiddenError("Configuration not accessable")
        cv_url = current_app.config["CV_URL"]

        def url_lookup(element):
            if isinstance(element, Platform):
                return url_for(
                    "sensorml.platform_to_sensor_ml",
                    platform_id=element.id,
                    _external=True,
                )
            if isinstance(element, Device):
                return url_for(
                    "sensorml.device_to_sensor_ml", device_id=element.id, _external=True
                )
            return url_for(
                "sensorml.configuration_to_sensor_ml",
                configuration_id=element.id,
                _external=True,
            )

        physical_system = SiteConverter(
            site,
            cv_url,
            url_lookup,
        ).sml_physical_system()
        xml_object = physical_system.to_xml()
        ET.register_namespace("gml", gml.namespace)
        ET.register_namespace("gco", gco.namespace)
        ET.register_namespace("gmd", gmd.namespace)
        ET.register_namespace("sml", sml.namespace)
        ET.register_namespace("swe", swe.namespace)
        ET.register_namespace("xlink", xlink.namespace)
        ET.register_namespace("xsi", xsi.namespace)
        schema_locations = {}
        for ns_element in [gml, gco, gmd, sml, swe, xlink, xsi]:
            if ns_element.schema_location:
                schema_locations[ns_element.namespace] = ns_element.schema_location

        xml_object.attrib[xsi.attrib("schemaLocation")] = " ".join(
            f"{k} {v}" for k, v in schema_locations.items()
        )

        header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
        text = header + ET.tostring(xml_object)
        # We need to make sure that our gml:ids are unique in the
        # overall document.
        # The strategy here to give different names - with `_dup_{n}`
        # suffix.
        dup_count = {}

        def gml_id_replacement(match):
            original_gml_id = match.group(1)
            if original_gml_id not in dup_count.keys():
                dup_count[original_gml_id] = 0
                return match.group()
            dup_count[original_gml_id] += 1
            result = f'gml:id="{original_gml_id}_dup_{dup_count[original_gml_id]}"'
            return result

        text = re.sub(r'gml:id="([^"]+)"', gml_id_replacement, text.decode())
        response = make_response(text)
        response.headers["Content-Type"] = "application/xml"
        return response
    except ErrorResponse as e:
        return e.respond()
    except JsonApiException as e:
        return e.to_dict(), e.status


# @sensor_ml_routes.route("/device-from-sensorml", methods=["GET", "POST"])
# def digest_sensor_ml():
#
#     if request.method == "POST":
#         content_types = ["application/xml", "text/xml", "application/octet-stream"]
#         if "url" in request.form:
#             url = request.form["url"]
#             response = requests.get(url, timeout=5)
#             response.raise_for_status()
#             root = PhysicalSystem(response.text)
#             raise NotFoundError(repr(root.get_identifiers_by_name("Short Name")))
#
#         elif "file" in request.files:
#             file = request.files["file"]
#             content_type = file.content_type
#             if file and content_type in content_types:
#                 try:
#                     xml = file.stream.read()
#                     root = PhysicalSystem(xml)
#
#                     d = Device(
#                         description=root.get_identifiers_by_name("description"),
#                         short_name=root.get_identifiers_by_name("Short Name"),
#                         long_name=root.get_identifiers_by_name("long name"),
#                         serial_number=root.get_identifiers_by_name("Serial Number"),
#                         manufacturer_uri=root.get_identifiers_by_name(
#                             "Manufacturer Definition"
#                         ),
#                         manufacturer_name=root.get_identifiers_by_name("Manufacturer"),
#                         model=root.get_identifiers_by_name("model Number"),
#                         persistent_identifier=root.get_identifiers_by_name("uniqueID"),
#                         status_uri=root.get_identifiers_by_name(
#                             "System Status Definition"
#                         ),
#                         status_name=root.get_identifiers_by_name("System Status"),
#                         device_type_uri=root.get_classifiers_by_name(
#                             "Sensor Type Definition"
#                         ),
#                         device_type_name=root.get_classifiers_by_name("Sensor Type"),
#                         # dual_use=root.dual_use or None,
#                         # inventory_number=root.inventory_number or None,
#                         # website=root.website or None,
#                     )
#                     if save_to_db(d):
#                         for contact in root.contacts:
#                             c = Contact(
#                                 given_name=contact["name"].split(" ")[0],
#                                 family_name=contact["name"],
#                                 website=contact["url"],
#                                 email=contact["email"],
#                                 active=False,
#                                 devices=[d],
#                             )
#                             save_to_db(c)
#                         # for field in root.c
#                         # return redirect(url_for(f"/devices/{d.id}"), code=302)
#                         return redirect(url_for("api.device_list"), code=302)
#                     else:
#                         raise ConflictError("Could not save to db.")
#
#                 except NotFoundError as e:
#                     raise NotFoundError(str(e))
#             else:
#                 raise UnsupportedMediaTypeError(
#                     "{} is Not Permitted".format(file.content_type)
#                 )
#
#         else:
#             raise BadRequestError("No File or url in request Body was Found")
#     return """
#         <!doctype html>
#         <title>Digest a SensorMl File</title>
#         <h1>Digest a SensorMl File</h1>
#         <form method=post enctype=multipart/form-data>
#           <input type=file name=file>
#           <input type=url name=url pattern="https://.*" size="30">
#           <input type=submit value=Upload>
#         </form>
#         """

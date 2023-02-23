"""Routes for sensorML."""

# import requests
import re
from flask import Blueprint, current_app, g, make_response, render_template
from flask_rest_jsonapi.exceptions import JsonApiException

# from ..api.helpers.db import save_to_db
from sqlalchemy import and_

from ..api.auth.permission_utils import check_for_permission
from ..api.helpers.errors import ErrorResponse, NotFoundError, UnauthorizedError
from ..api.models import (
    Configuration,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
)
from ..api.models.base_model import db
from ..config import env

# from ..extensions.sensor_ml.sml import PhysicalSystem

sensor_ml_routes = Blueprint(
    "sensorml", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


def is_non_empty_device_property(dp):
    """Return true if the device property has enough information to be included in SensorML."""
    if dp.property_name or dp.property_uri or dp.label or dp.unit_name:
        return True
    return False


@sensor_ml_routes.route("/devices/<int:device_id>/sensorml", methods=["GET"])
def device_to_sensor_ml(device_id):
    """
    Export a device as sensorML.

    :param device_id: id
    :return: xml file
    """
    try:
        check_for_permission(model_class=Device, kwargs={"id": device_id})
        device = db.session.query(Device).filter_by(id=device_id).first()
        if device is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        else:
            gmlId = f"device_{device.id}"
            device.device_properties = list(
                filter(is_non_empty_device_property, device.device_properties)
            )
            template = render_template(
                "device_sensorml_template.xml",
                gmlId=gmlId,
                obj=device,
                contact_roles=device.device_contact_roles,
                cv_url=current_app.config["CV_URL"],
            )
            response = make_response(template)
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
        check_for_permission(model_class=Platform, kwargs={"id": platform_id})
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        if platform is None:
            raise NotFoundError({"pointer": ""}, "Object Not Found")
        else:
            gmlId = f"platform_{platform.id}"
            template = render_template(
                "platform_sensorml_template.xml",
                gmlId=gmlId,
                obj=platform,
                contact_roles=platform.platform_contact_roles,
                cv_url=current_app.config["CV_URL"],
            )
            response = make_response(template)
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
        else:
            if configuration.is_internal and not g.user:
                raise UnauthorizedError("Authentication required.")
            active_device_mounts = db.session.query(DeviceMountAction).filter(
                and_(DeviceMountAction.configuration_id == configuration_id)
            )
            active_platform_mounts = db.session.query(PlatformMountAction).filter(
                and_(PlatformMountAction.configuration_id == configuration_id)
            )

            children = {}
            top_level_mounts = []

            for active_platform_mount in active_platform_mounts:
                children.setdefault(active_platform_mount.platform_id, [])

                element_payload = {
                    "action_type": "platform_mount",
                    "entity": active_platform_mount.platform,
                    "children": children[active_platform_mount.platform_id],
                }
                if active_platform_mount.parent_platform_id:
                    children.setdefault(active_platform_mount.parent_platform_id, [])
                    if (
                        element_payload
                        not in children[active_platform_mount.parent_platform_id]
                    ):
                        children[active_platform_mount.parent_platform_id].append(
                            element_payload
                        )
                else:
                    if element_payload not in top_level_mounts:
                        top_level_mounts.append(element_payload)

            for active_device_mount in active_device_mounts:
                active_device_mount.device.device_properties = list(
                    filter(
                        is_non_empty_device_property,
                        active_device_mount.device.device_properties,
                    )
                )
                element_payload = {
                    "action_type": "device_mount",
                    "entity": active_device_mount.device,
                    "children": [],
                }
                if active_device_mount.parent_platform_id:
                    children.setdefault(active_device_mount.parent_platform_id, [])
                    if (
                        element_payload
                        not in children[active_device_mount.parent_platform_id]
                    ):
                        children[active_device_mount.parent_platform_id].append(
                            element_payload
                        )
                else:
                    if element_payload not in top_level_mounts:
                        top_level_mounts.append(element_payload)

            gmlId = f"configuration_{configuration.id}"
            template = render_template(
                "configuration_sensorml_template.xml",
                gmlId=gmlId,
                obj=configuration,
                contact_roles=configuration.configuration_contact_roles,
                tree=top_level_mounts,
                frontend_url=current_app.config["SMS_FRONTEND_URL"],
                cv_url=current_app.config["CV_URL"],
            )
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
            template = re.sub(r'gml:id="([^"]+)"', gml_id_replacement, template)
            response = make_response(template)
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

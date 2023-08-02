# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Classes to convert sms database models into sensorML models."""

from typing import List, Optional

from geoalchemy2.shape import to_shape

from ..api.models import Configuration
from ..api.models.base_model import db
from ..api.permissions.rules import filter_visible
from ..extensions.instances import pidinst
from . import cleanup
from .models import (
    GcoCharacterString,
    GmdAddress,
    GmdCiAddress,
    GmdCiContact,
    GmdCiOnlineResource,
    GmdCiResponsibleParty,
    GmdCiRoleCode,
    GmdCity,
    GmdContactInfo,
    GmdCountry,
    GmdDeliveryPoint,
    GmdElectronicalMailAddress,
    GmdIndividualName,
    GmdLinkage,
    GmdName,
    GmdOnlineResource,
    GmdOrganisationName,
    GmdPostalCode,
    GmdRole,
    GmdUrl,
    GmlBegin,
    GmlDescription,
    GmlEnd,
    GmlExterior,
    GmlLinearRing,
    GmlLocation,
    GmlName,
    GmlPolygon,
    GmlPos,
    GmlTimeInstant,
    GmlTimePeriod,
    GmlTimePosition,
    SmlClassification,
    SmlClassifier,
    SmlComponent,
    SmlComponents,
    SmlConfiguration,
    SmlContact,
    SmlContacts,
    SmlDocument,
    SmlDocumentation,
    SmlEvent,
    SmlHistory,
    SmlIdentification,
    SmlIdentifier,
    SmlLabel,
    SmlOutput,
    SmlOutputs,
    SmlParameter,
    SmlParameters,
    SmlPhysicalSystem,
    SmlPosition,
    SmlSettings,
    SmlSetValue,
    SmlTerm,
    SmlTime,
    SmlValidTime,
    SmlValue,
    SweExtension,
    SweLabel,
    SweQuantity,
    SweText,
    SweUom,
)


class AttachmentConverter:
    """Converter for sensorML for attachments."""

    def __init__(self, attachments, physical_system_gml_id):
        """Init the object."""
        self.attachments = attachments
        self.physical_system_gml_id = physical_system_gml_id

    def sml_document_list(self) -> List[SmlDocument]:
        """Return the list of sml:document entries."""
        result = []
        for attachment in self.attachments:
            sml_document = SmlDocument(
                xlink_arcrole="Attachment",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    id=f"Attachment_{attachment.id}_of_PhysicalSystem_{self.physical_system_gml_id}",
                    gmd_linkage=GmdLinkage(gmd_url=GmdUrl(text=attachment.url)),
                    gmd_name=GmdName(
                        gco_character_string=GcoCharacterString(text=attachment.label)
                    ),
                ),
            )
            result.append(sml_document)
        return result


class ContactRoleConverter:
    """Converter for sensorML for contact roles."""

    def __init__(self, contact_roles, cv_url):
        """Init the object."""
        self.contact_roles = contact_roles
        self.cv_url = cv_url

    def sml_contacts(self) -> Optional[SmlContacts]:
        """Return the sml:contacts."""
        sml_contact_list = []
        for contact_role in self.contact_roles:
            xlink_arcrole = None
            if contact_role.role_uri:
                xlink_arcrole = contact_role.role_uri

            gmd_individual_name = GmdIndividualName(
                gco_character_string=GcoCharacterString(
                    text=f"{contact_role.contact.given_name} {contact_role.contact.family_name}"
                )
            )
            gmd_organisation_name = None
            if contact_role.contact.organization:
                gmd_organisation_name = GmdOrganisationName(
                    gco_character_string=GcoCharacterString(
                        text=contact_role.contact.organization
                    )
                )
            gmd_address = GmdAddress(
                gmd_ci_address=GmdCiAddress(
                    gmd_electronical_mail_address=GmdElectronicalMailAddress(
                        gco_character_string=GcoCharacterString(
                            text=contact_role.contact.email
                        )
                    )
                )
            )
            gmd_online_resource = None
            if contact_role.contact.orcid:
                gmd_online_resource = GmdOnlineResource(
                    gmd_ci_online_resource=GmdCiOnlineResource(
                        gmd_linkage=GmdLinkage(
                            gmd_url=GmdUrl(
                                text=f"https://orcid.org/{contact_role.contact.orcid}"
                            )
                        ),
                    )
                )
            elif contact_role.contact.website:
                gmd_online_resource = GmdOnlineResource(
                    gmd_ci_online_resource=GmdCiOnlineResource(
                        gmd_linkage=GmdLinkage(
                            gmd_url=GmdUrl(text=contact_role.contact.website)
                        ),
                    )
                )
            gmd_contact_info = GmdContactInfo(
                gmd_ci_contact=GmdCiContact(
                    gmd_address=gmd_address, gmd_online_resource=gmd_online_resource
                )
            )
            role_code_list_value = ""
            if contact_role.role_uri:
                role_code_list_value = contact_role.role_uri.strip("/").split("/")[-1]
            gmd_role = GmdRole(
                gmd_ci_role_code=GmdCiRoleCode(
                    code_list=f"{self.cv_url}/contactroles",
                    code_list_value=role_code_list_value,
                    text=contact_role.role_name,
                )
            )
            sml_contact = SmlContact(
                xlink_arcrole=xlink_arcrole,
                gmd_ci_responsible_party=GmdCiResponsibleParty(
                    gmd_individual_name=gmd_individual_name,
                    gmd_organisation_name=gmd_organisation_name,
                    gmd_contact_info=gmd_contact_info,
                    gmd_role=gmd_role,
                ),
            )
            sml_contact_list.append(sml_contact)
        if not sml_contact_list:
            return None
        return SmlContacts(
            sml_contact_list=sml_contact_list,
        )


class ConfigurationConverter:
    """Converter for sensorML for configurations."""

    def __init__(self, configuration, cv_url, url_lookup):
        """Init the object."""
        self.configuration = configuration
        self.cv_url = cv_url
        self.url_lookup = url_lookup

    def sml_physical_system(self) -> SmlPhysicalSystem:
        """Return a sml:PhysicalSystem."""
        physical_system = SmlPhysicalSystem(
            gml_id=self.gml_id(),
            gml_name=self.gml_name(),
            gml_description=self.gml_description(),
            sml_valid_time=self.sml_valid_time(),
            sml_identification=self.sml_identification(),
            sml_classification=self.sml_classification(),
            sml_documentation=self.sml_documentation(),
            sml_contacts=self.sml_contacts(),
            sml_history=self.sml_history(),
            sml_parameters=self.sml_parameters(),
            sml_components=self.sml_components(),
        )
        return physical_system

    def gml_id(self) -> str:
        """Return the gml id of the physical system."""
        return f"configuration_{self.configuration.id}"

    def gml_name(self) -> GmlName:
        """Return the gml:name."""
        return GmlName(text=self.configuration.label)

    def gml_description(self) -> Optional[GmlDescription]:
        """Return the gml:description."""
        if not self.configuration.description:
            return None
        return GmlDescription(text=self.configuration.description)

    def sml_valid_time(self) -> Optional[SmlValidTime]:
        """Return the sml:validTime."""
        if not self.configuration.start_date:
            return None
        gml_begin = GmlBegin(
            gml_time_instant=GmlTimeInstant(
                gml_time_position=GmlTimePosition(text=self.configuration.start_date)
            )
        )
        gml_end = GmlEnd()
        if self.configuration.end_date:
            gml_end.gml_time_instant = GmlTimeInstant(
                gml_time_position=GmlTimePosition(text=self.configuration.end_date)
            )
        gml_time_period = GmlTimePeriod(
            gml_id=f"ValidTime_{self.gml_id()}", gml_begin=gml_begin, gml_end=gml_end
        )
        return SmlValidTime(gml_time_period=gml_time_period)

    def sml_identification(self) -> Optional[SmlIdentification]:
        """Return the sml:identification."""
        sml_identifier_list = []

        if self.configuration.persistent_identifier:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/Identifier",
                sml_label=SmlLabel(text="handle"),
                sml_value=SmlValue(text=self.configuration.persistent_identifier),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)
        if not sml_identifier_list:
            return None
        return SmlIdentification(sml_identifier_list=sml_identifier_list)

    def sml_classification(self) -> Optional[SmlClassification]:
        """Return the sml classification."""
        sml_classifier_list = []
        if self.configuration.project:
            sml_term = SmlTerm(
                definition="http://xmlns.com/foaf/0.1/#term_Project",
                sml_label=SmlLabel(text="Project"),
                sml_value=SmlValue(text=self.configuration.project),
            )
            sml_classifier = SmlClassifier(sml_term=sml_term)
            sml_classifier_list.append(sml_classifier)
        if not sml_classifier_list:
            return None
        return SmlClassification(sml_classifier_list=sml_classifier_list)

    def sml_contacts(self) -> Optional[SmlContacts]:
        """Return the sml:contacts."""
        return ContactRoleConverter(
            self.configuration.configuration_contact_roles, self.cv_url
        ).sml_contacts()

    def sml_documentation(self) -> Optional[SmlDocumentation]:
        """Return the sml:documentation."""
        sml_document_list = AttachmentConverter(
            self.configuration.configuration_attachments, self.gml_id()
        ).sml_document_list()
        if self.configuration.b2inst_record_id:
            sml_document = SmlDocument(
                xlink_arcrole="PIDINST",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=pidinst.b2inst.get_record_frontend_url(
                                self.configuration.b2inst_record_id
                            )
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)
        if not sml_document_list:
            return None
        return SmlDocumentation(sml_document_list=sml_document_list)

    def sml_history(self) -> Optional[SmlHistory]:
        """Return the sml:history."""
        sml_event_list = []

        for event in self.configuration.device_mount_actions:
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            sml_label=SmlLabel(text="DeviceMountAction"),
                            sml_value=SmlValue(text="DeviceMountAction"),
                            definition="DeviceMountAction",
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=event.begin_date),
                )
            )
            gml_end = GmlEnd()
            if event.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=event.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForDeviceMountAction_{event.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=event.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for event in self.configuration.platform_mount_actions:
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            sml_label=SmlLabel(text="PlatformMountAction"),
                            sml_value=SmlValue(text="PlatformMountAction"),
                            definition="PlatformMountAction",
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=event.begin_date),
                )
            )
            gml_end = GmlEnd()
            if event.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=event.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForPlatformMountAction_{event.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=event.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for event in self.configuration.configuration_static_location_begin_actions:
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            sml_label=SmlLabel(text="StaticLocationAction"),
                            sml_value=SmlValue(
                                text=event.label or "StaticLocationAction"
                            ),
                            definition="StaticLocationAction",
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=event.begin_date),
                )
            )
            gml_end = GmlEnd()
            if event.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=event.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForStaticLocationAction_{event.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=event.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)
        for event in self.configuration.configuration_dynamic_location_begin_actions:
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            sml_label=SmlLabel(text="DynamicLocationAction"),
                            sml_value=SmlValue(
                                text=event.label or "DynamicLocationAction"
                            ),
                            definition="DynamicLocationAction",
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=event.begin_date),
                )
            )
            gml_end = GmlEnd()
            if event.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=event.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForDynamicLocationAction_{event.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=event.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.configuration.generic_configuration_actions:
            definition = "Action"
            if action.action_type_uri:
                definition = action.action_type_uri
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            sml_label=SmlLabel(text=action.action_type_name),
                            sml_value=SmlValue(text=action.action_type_name),
                            definition=definition,
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=action.begin_date),
                )
            )
            gml_end = GmlEnd()
            if action.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.end_date),
                    )
                )
            gml_id = cleanup.identifier(
                f"TimePeriodFor{action.action_type_name}_{action.id}_of_{self.gml_id()}",
                replacement="",
            )
            gml_time_period = GmlTimePeriod(
                gml_id=gml_id,
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=action.description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)
        for parameter in self.configuration.configuration_parameters:
            for action in parameter.configuration_parameter_value_change_actions:
                sml_classification = SmlClassification(
                    [
                        SmlClassifier(
                            sml_term=SmlTerm(
                                definition="ParameterChange",
                                sml_label=SmlLabel(
                                    text=f"Changed parameter for {parameter.label}"
                                ),
                                sml_value=SmlValue(text=action.value),
                            )
                        )
                    ]
                )
                sml_time = SmlTime(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.date),
                    )
                )
                sml_configuration = SmlConfiguration(
                    sml_settings=SmlSettings(
                        sml_set_value=SmlSetValue(
                            ref=cleanup.identifier(parameter.label, replacement="_"),
                            text=action.value,
                        )
                    )
                )
                sml_event = SmlEvent(
                    sml_classification=sml_classification,
                    sml_time=sml_time,
                    sml_configuration=sml_configuration,
                )
                sml_event_list.append(sml_event)
        if not sml_event_list:
            return None
        return SmlHistory(sml_event_list=sml_event_list)

    def sml_parameters(self):
        """Return the sml:parameters."""
        sml_parameter_list = []
        for configuration_parameter in self.configuration.configuration_parameters:
            if configuration_parameter.label:
                name = cleanup.identifier(
                    configuration_parameter.label, replacement="_"
                )
                swe_quantity = None
                if configuration_parameter.unit_name:
                    swe_uom = SweUom(code=configuration_parameter.unit_name)
                    swe_quantity = SweQuantity(swe_uom=swe_uom)
                parameter = SmlParameter(name=name, swe_quantity=swe_quantity)
                sml_parameter_list.append(parameter)

        if not sml_parameter_list:
            return None
        return SmlParameters(sml_parameter_list=sml_parameter_list)

    def _build_tree(self):
        """Help to build a tree with the platforms & devices as children."""
        children = {}
        top_level_mounts = []

        for active_platform_mount in self.configuration.platform_mount_actions:
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

        for active_device_mount in self.configuration.device_mount_actions:
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
        return top_level_mounts

    def sml_components(self) -> Optional[SmlComponents]:
        """Return the sml components."""
        tree = self._build_tree()
        sml_component_list = []

        def insert_into_components(element, sml_component_list) -> None:
            """
            Help to fill the components list.

            Also allow recursion to add to sub lists.
            The function doesn't return anything, it is just used for
            the side effects (adding to the list).
            """
            if element["action_type"] == "platform_mount":
                sub_system = PlatformConverter(
                    element["entity"], self.cv_url
                ).sml_physical_system()
                sml_component = SmlComponent(
                    sml_physical_system=sub_system,
                    xlink_href=self.url_lookup(element["entity"]),
                    name=cleanup.identifier(element["entity"].short_name),
                    xlink_title=f"Link to Platform {element['entity'].id}",
                )
                sml_component_list.append(sml_component)

                sub_components_list = []
                for child in element["children"]:
                    # Call recursively to add all childs of the child to
                    # the sub list.
                    insert_into_components(child, sub_components_list)

                if sub_components_list:
                    sub_system.sml_components = SmlComponents(
                        sml_component_list=sub_components_list
                    )
            else:
                sub_system = DeviceConverter(
                    element["entity"], self.cv_url
                ).sml_physical_system()
                sml_component = SmlComponent(
                    sml_physical_system=sub_system,
                    xlink_href=self.url_lookup(element["entity"]),
                    name=cleanup.identifier(element["entity"].short_name),
                    xlink_title=f"Link to Device {element['entity'].id}",
                )
                sml_component_list.append(sml_component)

        for element in tree:
            insert_into_components(element, sml_component_list)

        if not sml_component_list:
            return None
        return SmlComponents(sml_component_list=sml_component_list)


class DeviceConverter:
    """Converter for sensorML for devices."""

    def __init__(self, device, cv_url):
        """Init the object."""
        self.device = device
        self.cv_url = cv_url

    def sml_physical_system(self) -> SmlPhysicalSystem:
        """Return a sml:PhysicalSystem."""
        physical_system = SmlPhysicalSystem(
            gml_id=self.gml_id(),
            gml_description=self.gml_description(),
            sml_identification=self.sml_identification(),
            sml_classification=self.sml_classification(),
            sml_outputs=self.sml_outputs(),
            sml_parameters=self.sml_parameters(),
            sml_documentation=self.sml_documentation(),
            sml_contacts=self.sml_contacts(),
            sml_history=self.sml_history(),
        )
        return physical_system

    def gml_id(self) -> str:
        """Return the gml:id of the physical system."""
        return f"device_{self.device.id}"

    def gml_description(self) -> Optional[GmlDescription]:
        """Return the gml:description."""
        if not self.device.description:
            return None
        return GmlDescription(text=self.device.description)

    def sml_outputs(self) -> Optional[SmlOutputs]:
        """Return the sml:outputs."""
        sml_output_list = []
        for device_property in self.device.device_properties:
            if (
                device_property.property_name
                or device_property.property_uri
                or device_property.label
                or device_property.unit_name
            ):
                name = cleanup.identifier(
                    device_property.property_name, replacement="_"
                )

                swe_label = SweLabel(text=device_property.label)
                swe_uom = SweUom()
                if device_property.unit_name:
                    swe_uom.code = device_property.unit_name

                definition = ""
                if device_property.property_uri:
                    definition = device_property.property_uri

                swe_quantity = SweQuantity(
                    swe_uom=swe_uom,
                    swe_label=swe_label,
                    definition=definition,
                )

                output = SmlOutput(name=name, swe_quantity=swe_quantity)
                sml_output_list.append(output)

        if not sml_output_list:
            return None
        return SmlOutputs(sml_output_list=sml_output_list)

    def sml_parameters(self):
        """Return the sml:parameters."""
        sml_parameter_list = []
        for device_parameter in self.device.device_parameters:
            if device_parameter.label:
                name = cleanup.identifier(device_parameter.label, replacement="_")
                swe_quantity = None
                if device_parameter.unit_name:
                    swe_uom = SweUom(code=device_parameter.unit_name)
                    swe_quantity = SweQuantity(swe_uom=swe_uom)
                parameter = SmlParameter(name=name, swe_quantity=swe_quantity)
                sml_parameter_list.append(parameter)

        if not sml_parameter_list:
            return None
        return SmlParameters(sml_parameter_list=sml_parameter_list)

    def sml_contacts(self) -> Optional[SmlContacts]:
        """Return the sml:contacts."""
        return ContactRoleConverter(
            self.device.device_contact_roles, self.cv_url
        ).sml_contacts()

    def sml_history(self) -> Optional[SmlHistory]:
        """Return the sml:history."""
        sml_event_list = []
        for action in self.device.device_mount_actions:

            label = f"Mounted to configuration {action.configuration.id}"
            if action.configuration.label:
                label = f"Mounted to {action.configuration.label}"
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition="Mount",
                            sml_label=SmlLabel(text=label),
                            sml_value=SmlValue(text="Mount"),
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=action.begin_date),
                )
            )
            gml_end = GmlEnd()
            if action.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForDeviceMountAction_{action.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=action.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.device.device_calibration_actions:

            # TODO: Find a valid way to put the formula & description in.
            # And also think about the next calibration date.
            value = ""
            if action.value is not None:
                value = str(action.value)
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition="Calibration",
                            sml_label=SmlLabel(text="Calibration"),
                            sml_value=SmlValue(text=value),
                        )
                    )
                ]
            )
            sml_time = SmlTime(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(
                        text=action.current_calibration_date
                    ),
                    gml_id=f"TimeInstantForCalibration_{action.id}_of_{self.gml_id()}",
                )
            )
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.device.generic_device_actions:

            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition=action.action_type_uri or "Action",
                            sml_label=SmlLabel(text=action.action_type_name),
                            sml_value=SmlValue(text=action.action_type_name),
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=action.begin_date),
                )
            )
            gml_end = GmlEnd()
            if action.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.end_date),
                    )
                )
            gml_id = cleanup.identifier(
                f"TimePeriodFor{action.action_type_name}_{action.id}_of_{self.gml_id()}",
                replacement="",
            )
            gml_time_period = GmlTimePeriod(
                gml_id=gml_id,
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(action.description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.device.device_software_update_actions:

            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition=action.software_type_uri or "SoftwareUpdate",
                            sml_label=SmlLabel(text=action.software_type_name),
                            sml_value=SmlValue(text=action.software_type_name),
                        )
                    )
                ]
            )
            gml_id = cleanup.identifier(
                f"TimeInstantFor{action.software_type_name}Update_{action.id}_of_{self.gml_id()}",
                replacement="",
            )
            gml_time_instant = GmlTimeInstant(
                gml_id=gml_id,
                gml_time_position=GmlTimePosition(text=action.update_date),
            )
            sml_time = SmlTime(gml_time_instant=gml_time_instant)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)
        for parameter in self.device.device_parameters:
            for action in parameter.device_parameter_value_change_actions:
                sml_classification = SmlClassification(
                    [
                        SmlClassifier(
                            sml_term=SmlTerm(
                                definition="ParameterChange",
                                sml_label=SmlLabel(
                                    text=f"Changed parameter for {parameter.label}"
                                ),
                                sml_value=SmlValue(text=action.value),
                            )
                        )
                    ]
                )
                sml_time = SmlTime(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.date),
                    )
                )
                sml_configuration = SmlConfiguration(
                    sml_settings=SmlSettings(
                        sml_set_value=SmlSetValue(
                            ref=cleanup.identifier(parameter.label, replacement="_"),
                            text=action.value,
                        )
                    )
                )
                sml_event = SmlEvent(
                    sml_classification=sml_classification,
                    sml_time=sml_time,
                    sml_configuration=sml_configuration,
                )
                sml_event_list.append(sml_event)
        if not sml_event_list:
            return None
        return SmlHistory(sml_event_list=sml_event_list)

    def sml_documentation(self) -> Optional[SmlDocumentation]:
        """Return the sml:documentation."""
        sml_document_list = [
            *AttachmentConverter(
                self.device.device_attachments, self.gml_id()
            ).sml_document_list()
        ]
        if self.device.website:
            sml_document = SmlDocument(
                xlink_arcrole="Website",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=self.device.website,
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)

        if self.device.b2inst_record_id:
            sml_document = SmlDocument(
                xlink_arcrole="PIDINST",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=pidinst.b2inst.get_record_frontend_url(
                                self.device.b2inst_record_id
                            )
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)

        if not sml_document_list:
            return None
        return SmlDocumentation(sml_document_list=sml_document_list)

    def sml_classification(self) -> Optional[SmlClassification]:
        """Return the sml:classification."""
        sml_classifier_list = []
        if self.device.device_type_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/SensorType",
                sml_label=SmlLabel(text="sensor type"),
                sml_value=SmlValue(text=self.device.device_type_name),
            )
            sml_classifier = SmlClassifier(sml_term=sml_term)
            sml_classifier_list.append(sml_classifier)
        if not sml_classifier_list:
            return None
        return SmlClassification(sml_classifier_list=sml_classifier_list)

    def sml_identification(self) -> Optional[SmlIdentification]:
        """Return the sml:identification."""
        sml_identifier_list = []

        if self.device.persistent_identifier:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/Identifier",
                sml_label=SmlLabel(text="handle"),
                sml_value=SmlValue(text=self.device.persistent_identifier),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.device.long_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/LongName",
                sml_label=SmlLabel(text="Long Name"),
                sml_value=SmlValue(text=self.device.long_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        sml_term = SmlTerm(
            definition="http://sensorml.com/ont/swe/property/ShortName",
            sml_label=SmlLabel(text="Short Name"),
            sml_value=SmlValue(text=self.device.short_name),
        )
        sml_identifier = SmlIdentifier(sml_term=sml_term)
        sml_identifier_list.append(sml_identifier)

        if self.device.model:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/ModelNumber",
                sml_label=SmlLabel(text="Model Number"),
                sml_value=SmlValue(text=self.device.model),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.device.status_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/SystemStatus",
                sml_label=SmlLabel(text="System Status"),
                sml_value=SmlValue(text=self.device.status_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.device.serial_number:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/SerialNumber",
                sml_label=SmlLabel(text="Serial Number"),
                sml_value=SmlValue(text=self.device.serial_number),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.device.manufacturer_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/Manufacturer",
                sml_label=SmlLabel(text="Manufacturer"),
                sml_value=SmlValue(text=self.device.manufacturer_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if not sml_identifier_list:
            return None
        return SmlIdentification(sml_identifier_list=sml_identifier_list)


class PlatformConverter:
    """Converter for sensorML for platforms."""

    def __init__(self, platform, cv_url):
        """Init the object."""
        self.platform = platform
        self.cv_url = cv_url

    def sml_physical_system(self) -> SmlPhysicalSystem:
        """Return the sml:PhysicalSystem."""
        physical_system = SmlPhysicalSystem(
            gml_id=self.gml_id(),
            gml_description=self.gml_description(),
            sml_identification=self.sml_identification(),
            sml_classification=self.sml_classification(),
            sml_documentation=self.sml_documentation(),
            sml_contacts=self.sml_contacts(),
            sml_history=self.sml_history(),
            sml_parameters=self.sml_parameters(),
        )
        return physical_system

    def gml_id(self):
        """Return the gml:id for the physical system."""
        return f"platform_{self.platform.id}"

    def gml_description(self) -> Optional[GmlDescription]:
        """Return the gml:description."""
        if not self.platform.description:
            return None
        return GmlDescription(text=self.platform.description)

    def sml_contacts(self) -> Optional[SmlContacts]:
        """Return the sml:contacts."""
        return ContactRoleConverter(
            self.platform.platform_contact_roles, self.cv_url
        ).sml_contacts()

    def sml_history(self) -> Optional[SmlHistory]:
        """Return the sml:history."""
        sml_event_list = []
        for action in self.platform.platform_mount_actions:

            label = f"Mounted to configuration {action.configuration.id}"
            if action.configuration.label:
                label = f"Mounted to {action.configuration.label}"
            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition="Mount",
                            sml_label=SmlLabel(text=label),
                            sml_value=SmlValue(text="Mount"),
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=action.begin_date),
                )
            )
            gml_end = GmlEnd()
            if action.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.end_date),
                    )
                )
            gml_time_period = GmlTimePeriod(
                gml_id=f"TimePeriodForPlatformMountAction_{action.id}_of_{self.gml_id()}",
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(text=action.begin_description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.platform.generic_platform_actions:

            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition=action.action_type_uri or "Action",
                            sml_label=SmlLabel(text=action.action_type_name),
                            sml_value=SmlValue(text=action.action_type_name),
                        )
                    )
                ]
            )
            gml_begin = GmlBegin(
                gml_time_instant=GmlTimeInstant(
                    gml_time_position=GmlTimePosition(text=action.begin_date),
                )
            )
            gml_end = GmlEnd()
            if action.end_date:
                gml_end = GmlEnd(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.end_date),
                    )
                )
            gml_id = cleanup.identifier(
                f"TimePeriodFor{action.action_type_name}_{action.id}_of_{self.gml_id()}",
                replacement="",
            )
            gml_time_period = GmlTimePeriod(
                gml_id=gml_id,
                gml_begin=gml_begin,
                gml_end=gml_end,
                gml_description=GmlDescription(action.description),
            )
            sml_time = SmlTime(gml_time_period=gml_time_period)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)

        for action in self.platform.platform_software_update_actions:

            sml_classification = SmlClassification(
                [
                    SmlClassifier(
                        sml_term=SmlTerm(
                            definition=action.software_type_uri or "SoftwareUpdate",
                            sml_label=SmlLabel(text=action.software_type_name),
                            sml_value=SmlValue(text=action.software_type_name),
                        )
                    )
                ]
            )
            gml_id = cleanup.identifier(
                f"TimeInstantFor{action.software_type_name}Update_{action.id}_of_{self.gml_id()}",
                replacement="",
            )
            gml_time_instant = GmlTimeInstant(
                gml_id=gml_id,
                gml_time_position=GmlTimePosition(text=action.update_date),
            )
            sml_time = SmlTime(gml_time_instant=gml_time_instant)
            sml_event = SmlEvent(
                sml_classification=sml_classification, sml_time=sml_time
            )
            sml_event_list.append(sml_event)
        for parameter in self.platform.platform_parameters:
            for action in parameter.platform_parameter_value_change_actions:
                sml_classification = SmlClassification(
                    [
                        SmlClassifier(
                            sml_term=SmlTerm(
                                definition="ParameterChange",
                                sml_label=SmlLabel(
                                    text=f"Changed parameter for {parameter.label}"
                                ),
                                sml_value=SmlValue(text=action.value),
                            )
                        )
                    ]
                )
                sml_time = SmlTime(
                    gml_time_instant=GmlTimeInstant(
                        gml_time_position=GmlTimePosition(text=action.date),
                    )
                )
                sml_configuration = SmlConfiguration(
                    sml_settings=SmlSettings(
                        sml_set_value=SmlSetValue(
                            ref=cleanup.identifier(parameter.label, replacement="_"),
                            text=action.value,
                        )
                    )
                )
                sml_event = SmlEvent(
                    sml_classification=sml_classification,
                    sml_time=sml_time,
                    sml_configuration=sml_configuration,
                )
                sml_event_list.append(sml_event)
        if not sml_event_list:
            return None
        return SmlHistory(sml_event_list=sml_event_list)

    def sml_parameters(self):
        """Return the sml:parameters."""
        sml_parameter_list = []
        for platform_parameter in self.platform.platform_parameters:
            if platform_parameter.label:
                name = cleanup.identifier(platform_parameter.label, replacement="_")
                swe_quantity = None
                if platform_parameter.unit_name:
                    swe_uom = SweUom(code=platform_parameter.unit_name)
                    swe_quantity = SweQuantity(swe_uom=swe_uom)
                parameter = SmlParameter(name=name, swe_quantity=swe_quantity)
                sml_parameter_list.append(parameter)

        if not sml_parameter_list:
            return None
        return SmlParameters(sml_parameter_list=sml_parameter_list)

    def sml_documentation(self) -> Optional[SmlDocumentation]:
        """Return the sml:documentation."""
        sml_document_list = [
            *AttachmentConverter(
                self.platform.platform_attachments, self.gml_id()
            ).sml_document_list()
        ]
        if self.platform.website:
            sml_document = SmlDocument(
                xlink_arcrole="Website",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=self.platform.website,
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)

        if self.platform.b2inst_record_id:
            sml_document = SmlDocument(
                xlink_arcrole="PIDINST",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=pidinst.b2inst.get_record_frontend_url(
                                self.platform.b2inst_record_id
                            )
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)

        if not sml_document_list:
            return None
        return SmlDocumentation(sml_document_list=sml_document_list)

    def sml_classification(self) -> Optional[SmlClassification]:
        """Return the sml classification."""
        sml_classifier_list = []
        if self.platform.platform_type_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/PlatformType",
                sml_label=SmlLabel(text="platform type"),
                sml_value=SmlValue(text=self.platform.platform_type_name),
            )
            sml_classifier = SmlClassifier(sml_term=sml_term)
            sml_classifier_list.append(sml_classifier)
        if not sml_classifier_list:
            return None
        return SmlClassification(sml_classifier_list=sml_classifier_list)

    def sml_identification(self) -> Optional[SmlIdentification]:
        """Return the sml:idenfication."""
        sml_identifier_list = []

        if self.platform.persistent_identifier:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/Identifier",
                sml_label=SmlLabel(text="handle"),
                sml_value=SmlValue(text=self.platform.persistent_identifier),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.platform.long_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/LongName",
                sml_label=SmlLabel(text="Long Name"),
                sml_value=SmlValue(text=self.platform.long_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        sml_term = SmlTerm(
            definition="http://sensorml.com/ont/swe/property/ShortName",
            sml_label=SmlLabel(text="Short Name"),
            sml_value=SmlValue(text=self.platform.short_name),
        )
        sml_identifier = SmlIdentifier(sml_term=sml_term)
        sml_identifier_list.append(sml_identifier)

        if self.platform.model:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/ModelNumber",
                sml_label=SmlLabel(text="Model Number"),
                sml_value=SmlValue(text=self.platform.model),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.platform.status_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/SystemStatus",
                sml_label=SmlLabel(text="System Status"),
                sml_value=SmlValue(text=self.platform.status_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.platform.serial_number:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/SerialNumber",
                sml_label=SmlLabel(text="Serial Number"),
                sml_value=SmlValue(text=self.platform.serial_number),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if self.platform.manufacturer_name:
            sml_term = SmlTerm(
                definition="http://sensorml.com/ont/swe/property/Manufacturer",
                sml_label=SmlLabel(text="Manufacturer"),
                sml_value=SmlValue(text=self.platform.manufacturer_name),
            )
            sml_identifier = SmlIdentifier(sml_term=sml_term)
            sml_identifier_list.append(sml_identifier)

        if not sml_identifier_list:
            return None
        return SmlIdentification(sml_identifier_list=sml_identifier_list)


class SiteConverter:
    """Converter for sensorML for sites."""

    def __init__(self, site, cv_url, url_lookup):
        """Init the object."""
        self.site = site
        self.cv_url = cv_url
        self.url_lookup = url_lookup

    def sml_physical_system(self) -> SmlPhysicalSystem:
        """Return a sml:PhysicalSystem."""
        physical_system = SmlPhysicalSystem(
            gml_id=self.gml_id(),
            gml_name=self.gml_name(),
            gml_description=self.gml_description(),
            gml_location=self.gml_location(),
            sml_contacts=self.sml_contacts(),
            sml_documentation=self.sml_documentation(),
            sml_classification=self.sml_classification(),
            sml_position=self.sml_position(),
            sml_components=self.sml_components(),
        )
        return physical_system

    def gml_id(self) -> str:
        """Return the gml id of the physical system."""
        return f"site_{self.site.id}"

    def gml_name(self) -> GmlName:
        """Return the gml:name."""
        return GmlName(text=self.site.label)

    def gml_description(self) -> Optional[GmlDescription]:
        """Return the gml:description."""
        if not self.site.description:
            return None
        return GmlDescription(text=self.site.description)

    def gml_location(self) -> Optional[GmlLocation]:
        if not self.site.geometry:
            return None
        shape = to_shape(self.site.geometry)
        exterior = shape.exterior
        gml_pos_list = []
        # Must be extended if we use more epsg codes.
        epsg_codes_with_y_x = ["4326"]
        for x, y in exterior.coords:
            # Depending on the EPSG code those elements need to be switched
            if self.site.epsg_code in epsg_codes_with_y_x:
                gml_pos_list.append(GmlPos(x=y, y=x))
            else:
                gml_pos_list.append(GmlPos(x=x, y=y))
        gml_linear_ring = GmlLinearRing(gml_pos_list=gml_pos_list)
        gml_exterior = GmlExterior(gml_linear_ring=gml_linear_ring)
        gml_id = f"{self.gml_id()}_geometry"
        srs_name = None
        if self.site.epsg_code:
            srs_name = f"http://www.opengis.net/def/crs/EPSG/0/{self.site.epsg_code}"
        gml_polygon = GmlPolygon(
            gml_id=gml_id, gml_exterior=gml_exterior, srs_name=srs_name
        )
        gml_location = GmlLocation(gml_polygon=gml_polygon)
        return gml_location

    def sml_contacts(self) -> Optional[SmlContacts]:
        """Return the sml:contacts."""
        return ContactRoleConverter(
            self.site.site_contact_roles, self.cv_url
        ).sml_contacts()

    def sml_documentation(self) -> Optional[SmlDocumentation]:
        """Return the sml:documentation."""
        sml_document_list = AttachmentConverter(
            self.site.site_attachments, self.gml_id()
        ).sml_document_list()
        if self.site.website:
            sml_document = SmlDocument(
                xlink_arcrole="Website",
                gmd_ci_online_resource=GmdCiOnlineResource(
                    gmd_linkage=GmdLinkage(
                        gmd_url=GmdUrl(
                            text=self.site.website,
                        )
                    ),
                ),
            )
            sml_document_list.append(sml_document)
        if not sml_document_list:
            return None
        return SmlDocumentation(sml_document_list=sml_document_list)

    def sml_classification(self) -> Optional[SmlClassification]:
        """Return the sml:classification."""
        sml_classifier_list = []
        if self.site.site_usage_name:
            sml_term = SmlTerm(
                definition="SiteUsage",
                sml_label=SmlLabel(text="site usage"),
                sml_value=SmlValue(text=self.site.site_usage_name),
            )
            sml_classifier = SmlClassifier(sml_term=sml_term)
            sml_classifier_list.append(sml_classifier)
        if self.site.site_type_name:
            sml_term = SmlTerm(
                definition="SiteType",
                sml_label=SmlLabel(text="site type"),
                sml_value=SmlValue(text=self.site.site_type_name),
            )
            sml_classifier = SmlClassifier(sml_term=sml_term)
            sml_classifier_list.append(sml_classifier)
        if not sml_classifier_list:
            return None
        return SmlClassification(sml_classifier_list=sml_classifier_list)

    def sml_position(self) -> Optional[SmlPosition]:
        """Return the sml:position."""
        if any(
            [
                self.site.city,
                self.site.zip_code,
                self.site.country,
                self.site.street,
                self.site.street_number,
                self.site.building,
                self.site.room,
            ]
        ):
            gmd_city = None
            if self.site.city:
                gco_character_string = GcoCharacterString(text=self.site.city)
                gmd_city = GmdCity(gco_character_string=gco_character_string)
            gmd_postal_code = None
            if self.site.zip_code:
                gco_character_string = GcoCharacterString(text=self.site.zip_code)
                gmd_postal_code = GmdPostalCode(
                    gco_character_string=gco_character_string
                )
            gmd_country = None
            if self.site.country:
                gco_character_string = GcoCharacterString(text=self.site.country)
                gmd_country = GmdCountry(gco_character_string=gco_character_string)
            gmd_delivery_point = None
            if any(
                [
                    self.site.street,
                    self.site.street_number,
                    self.site.building,
                    self.site.room,
                ]
            ):
                parts = []
                if self.site.street:
                    parts.append(self.site.street)
                if self.site.street_number:
                    parts.append(self.site.street_number)
                if self.site.building or self.site.room:
                    parts.append("-")
                if self.site.building:
                    parts.append(f"Building: {self.site.building}")
                if self.site.room:
                    parts.append(f"Room: {self.site.room}")
                gco_character_string = GcoCharacterString(text=" ".join(parts))
                gmd_delivery_point = GmdDeliveryPoint(
                    gco_character_string=gco_character_string
                )

            gmd_ci_address = GmdCiAddress(
                gmd_city=gmd_city,
                gmd_postal_code=gmd_postal_code,
                gmd_country=gmd_country,
                gmd_delivery_point=gmd_delivery_point,
            )
            swe_extension = SweExtension(
                gmd_ci_address=gmd_ci_address,
            )
            swe_text = SweText(swe_extension=swe_extension)
            sml_position = SmlPosition(swe_text=swe_text)
            return sml_position
        return None

    def sml_components(self) -> Optional[SmlComponents]:
        """Return the sml components."""
        sml_component_list = []

        for configuration in filter_visible(
            db.session.query(Configuration).filter_by(site_id=self.site.id)
        ):
            sml_physical_system = ConfigurationConverter(
                configuration, self.cv_url, self.url_lookup
            ).sml_physical_system()
            sml_component = SmlComponent(
                sml_physical_system=sml_physical_system,
                xlink_href=self.url_lookup(configuration),
                name=cleanup.identifier(configuration.label),
                xlink_title=f"Link to Configuration {configuration.id}",
            )
            sml_component_list.append(sml_component)

        if not sml_component_list:
            return None
        return SmlComponents(sml_component_list=sml_component_list)

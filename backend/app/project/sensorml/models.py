# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Model classes to handle sensorML.

Those only represent a subset of what is possible with sensorML
and xml in general. We can adjust it, based on the fields that we need
to cover.

The idea with those classes is to have a data class for every tag that
we use when handling sensorML - and accordingly the possible child
tags as fields in the dataclasses.

Often in XML there are alternatives: Two different fields with one
entry that can be present, while the other should not be there then.
We don't handle this on the data classes level yet, but set both to
be optional.

So it is not said that we will generate valid sensorML when we use the
data classes here. But it should help.
"""

import datetime
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional


class Namespace:
    """Helper class to handle xml namespaces and create tags."""

    def __init__(self, namespace):
        """Init the object with a namespace."""
        self.namespace = namespace

    def tag(self, tag):
        """Create a xml tag as ElementTree element using the namespace."""
        return ET.Element("{" + self.namespace + "}" + tag)

    def attrib(self, attrib):
        """Return the full qualitied attribute name."""
        return "{" + self.namespace + "}" + attrib


gco = Namespace("http://www.isotc211.org/2005/gco")
gmd = Namespace("http://www.isotc211.org/2005/gmd")
gml = Namespace("http://www.opengis.net/gml/3.2")
sml = Namespace("http://www.opengis.net/sensorml/2.0")
swe = Namespace("http://www.opengis.net/swe/2.0")
xlink = Namespace("http://www.w3.org/1999/xlink")


@dataclass
class GcoCharacterString:
    """Represent a gco:CharacterString."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = gco.tag("CharacterString")
        element.text = self.text
        return element


@dataclass
class GmdUrl:
    """Represent a gmd:URL."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("URL")
        element.text = self.text
        return element


@dataclass
class GmdName:
    """Represent a gmd:name."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("name")
        sub_element = self.gco_character_string.to_xml()
        element.append(sub_element)
        return element


@dataclass
class GmlTimePosition:
    """Represent a gml:timePosition."""

    text: datetime.datetime

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("timePosition")
        element.text = self.text.isoformat()
        return element


@dataclass
class GmlTimeInstant:
    """Represent a gml:TimeInstant."""

    gml_time_position: GmlTimePosition
    gml_id: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("TimeInstant")
        element.append(self.gml_time_position.to_xml())
        if self.gml_id:
            element.attrib[gml.attrib("id")] = self.gml_id
        return element


@dataclass
class GmlBegin:
    """Represent a gml:begin."""

    # Think about adding a handling for a nil reason.
    # gco_nil_reason: Optional[str]
    gml_time_instant: Optional[GmlTimeInstant] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("begin")
        sub_element = self.gml_time_instant.to_xml()
        element.append(sub_element)
        # TODO Add gco nil reason
        return element


@dataclass
class GmlEnd:
    """Represent a gmd:end."""

    # Think about adding a handling for a nil reason
    # gco_nil_reason: Optional[str]
    gml_time_instant: Optional[GmlTimeInstant] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("end")
        if self.gml_time_instant:
            element.append(self.gml_time_instant.to_xml())
        # TODO Add gco nil reason
        return element


@dataclass
class GmlDescription:
    """Represent a gml:description."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("description")
        element.text = self.text
        return element


@dataclass
class GmlTimePeriod:
    """Represent a gml:TimePeriod."""

    gml_id: Optional[str] = None
    gml_description: Optional[GmlDescription] = None
    gml_begin: Optional[GmlBegin] = None
    gml_end: Optional[GmlEnd] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("TimePeriod")
        if self.gml_id:
            element.attrib[gml.attrib("id")] = self.gml_id
        if self.gml_description:
            sub_element = self.gml_description.to_xml()
            element.append(sub_element)

        if self.gml_begin:
            sub_element = self.gml_begin.to_xml()
            element.append(sub_element)

        if self.gml_end:
            sub_element = self.gml_end.to_xml()
            element.append(sub_element)

        return element


@dataclass
class SmlTime:
    """Represent a sml:time."""

    gml_time_period: Optional[GmlTimePeriod] = None
    gml_time_instant: Optional[GmlTimeInstant] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("time")
        if self.gml_time_period:
            element.append(self.gml_time_period.to_xml())
        if self.gml_time_instant:
            element.append(self.gml_time_instant.to_xml())
        return element


@dataclass
class SweUom:
    """Represent a swe:uom."""

    code: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("uom")
        if self.code:
            element.attrib["code"] = self.code
        return element


@dataclass
class SweLabel:
    """Represent a swe:label."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("label")
        element.text = self.text
        return element


@dataclass
class SweQuantity:
    """Represent a swe:Quantity."""

    swe_uom: SweUom
    swe_label: Optional[SweLabel] = None
    definition: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("Quantity")
        if self.definition:
            element.attrib["definition"] = self.definition
        if self.swe_label:
            element.append(self.swe_label.to_xml())
        element.append(self.swe_uom.to_xml())
        return element


@dataclass
class SmlOutput:
    """Represent a sml:output."""

    name: str
    swe_quantity: SweQuantity

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("output")
        element.attrib["name"] = self.name
        element.append(self.swe_quantity.to_xml())
        return element


@dataclass
class SmlOutputs:
    """Represent a sml:outputs."""

    sml_output_list: List[SmlOutput] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("outputs")
        sub_element = sml.tag("OutputList")

        for entry in self.sml_output_list:
            sub_element.append(entry.to_xml())
        element.append(sub_element)
        return element


@dataclass
class SmlParameter:
    """Represent a sml:parameter."""

    name: str
    swe_quantity: Optional[SweQuantity] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("parameter")
        element.attrib["name"] = self.name
        if self.swe_quantity:
            element.append(self.swe_quantity.to_xml())
        return element


@dataclass
class SmlParameters:
    """Represent a sml:parameters."""

    sml_parameter_list: List[SmlParameter] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("parameters")
        sub_element = sml.tag("ParameterList")
        for entry in self.sml_parameter_list:
            sub_element.append(entry.to_xml())
        element.append(sub_element)
        return element


@dataclass
class GmdIndividualName:
    """Represent a gmd:individualName."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("individualName")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdOrganisationName:
    """Represent a gmd:organisationName."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("organisationName")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdElectronicalMailAddress:
    """Represent a gmd:electronicMailAddress."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("electronicMailAddress")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdCity:
    """Represent a gmd:city."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("city")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdPostalCode:
    """Represent a gmd:postalCode."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("postalCode")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdCountry:
    """Represent a gmd:country."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("country")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdDeliveryPoint:
    """Represent a gmd:deliveryPoint."""

    gco_character_string: GcoCharacterString

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("deliveryPoint")
        element.append(self.gco_character_string.to_xml())
        return element


@dataclass
class GmdCiAddress:
    """Represent a gmd:CI_Address."""

    gmd_electronical_mail_address: Optional[GmdElectronicalMailAddress] = None
    gmd_city: Optional[GmdCity] = None
    gmd_postal_code: Optional[GmdPostalCode] = None
    gmd_country: Optional[GmdCountry] = None
    gmd_delivery_point: Optional[GmdDeliveryPoint] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("CI_Address")
        if self.gmd_delivery_point:
            element.append(self.gmd_delivery_point.to_xml())
        if self.gmd_city:
            element.append(self.gmd_city.to_xml())
        if self.gmd_postal_code:
            element.append(self.gmd_postal_code.to_xml())
        if self.gmd_country:
            element.append(self.gmd_country.to_xml())
        if self.gmd_electronical_mail_address:
            element.append(self.gmd_electronical_mail_address.to_xml())
        return element


@dataclass
class GmdAddress:
    """Represent a gmd:address."""

    gmd_ci_address: GmdCiAddress

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("address")
        element.append(self.gmd_ci_address.to_xml())
        return element


@dataclass
class GmdLinkage:
    """Represent a gmd:linkage."""

    gmd_url: GmdUrl

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("linkage")
        element.append(self.gmd_url.to_xml())
        return element


@dataclass
class GmdCiOnlineResource:
    """Represent a gmd:CI_OnlineResource."""

    gmd_linkage: GmdLinkage
    id: Optional[str] = None
    gmd_name: Optional[GmdName] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("CI_OnlineResource")
        if self.id:
            element.attrib["id"] = self.id
        element.append(self.gmd_linkage.to_xml())
        if self.gmd_name:
            element.append(self.gmd_name.to_xml())
        return element


@dataclass
class GmdOnlineResource:
    """Represent a gmd:onlineResource."""

    gmd_ci_online_resource: GmdCiOnlineResource

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("onlineResource")
        element.append(self.gmd_ci_online_resource.to_xml())
        return element


@dataclass
class GmdCiContact:
    """Represent a gmd:CI_Contact."""

    gmd_address: GmdAddress
    gmd_online_resource: Optional[GmdOnlineResource] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("CI_Contact")
        element.append(self.gmd_address.to_xml())
        if self.gmd_online_resource:
            element.append(self.gmd_online_resource.to_xml())
        return element


@dataclass
class GmdContactInfo:
    """Represent a gmd:contactInfo."""

    gmd_ci_contact: GmdCiContact

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("contactInfo")
        element.append(self.gmd_ci_contact.to_xml())
        return element


@dataclass
class GmdCiRoleCode:
    """Represent a gmd:CI_RoleCode."""

    code_list: str
    code_list_value: str
    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("CI_RoleCode")
        element.attrib["codeList"] = self.code_list
        element.attrib["codeListValue"] = self.code_list_value
        element.text = self.text
        return element


@dataclass
class GmdRole:
    """Represent a gmd:role."""

    gmd_ci_role_code: GmdCiRoleCode

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("role")
        element.append(self.gmd_ci_role_code.to_xml())
        return element


@dataclass
class GmdCiResponsibleParty:
    """Represent a gmd:CI_ResponsibleParty."""

    gmd_contact_info: GmdContactInfo
    gmd_individual_name: GmdIndividualName
    gmd_organisation_name: Optional[GmdOrganisationName] = None
    gmd_role: Optional[GmdRole] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gmd.tag("CI_ResponsibleParty")
        element.append(self.gmd_individual_name.to_xml())
        if self.gmd_organisation_name:
            element.append(self.gmd_organisation_name.to_xml())
        element.append(self.gmd_contact_info.to_xml())
        if self.gmd_role:
            element.append(self.gmd_role.to_xml())
        return element


@dataclass
class SmlContact:
    """Represent a sml:contact."""

    gmd_ci_responsible_party: GmdCiResponsibleParty
    xlink_arcrole: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("contact")
        if self.xlink_arcrole:
            element.attrib[xlink.attrib("arcrole")] = self.xlink_arcrole
        element.append(self.gmd_ci_responsible_party.to_xml())
        return element


@dataclass
class SmlContacts:
    """Represent a sml:contacts."""

    sml_contact_list: List[SmlContact] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("contacts")
        list_element = sml.tag("ContactList")
        for entry in self.sml_contact_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class SmlDocument:
    """Represent a sml:document."""

    gmd_ci_online_resource: GmdCiOnlineResource
    xlink_arcrole: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("document")
        if self.xlink_arcrole:
            element.attrib[xlink.attrib("arcrole")] = self.xlink_arcrole
        element.append(self.gmd_ci_online_resource.to_xml())
        return element


@dataclass
class SmlLabel:
    """Represent a sml:label."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("label")
        element.text = self.text
        return element


@dataclass
class SmlValue:
    """Represent a sml:value."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("value")
        element.text = self.text
        return element


@dataclass
class SmlTerm:
    """Represent a sml:Term."""

    sml_label: SmlLabel
    sml_value: SmlValue
    definition: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("Term")
        if self.definition:
            element.attrib["definition"] = self.definition
        element.append(self.sml_label.to_xml())
        element.append(self.sml_value.to_xml())
        return element


@dataclass
class SmlIdentifier:
    """Represent a sml:identifier."""

    sml_term: SmlTerm

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("identifier")
        element.append(self.sml_term.to_xml())
        return element


@dataclass
class SmlClassifier:
    """Represent a sml:classifier."""

    sml_term: SmlTerm

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("classifier")
        element.append(self.sml_term.to_xml())
        return element


@dataclass
class SmlIdentification:
    """Represent a sml:identification."""

    sml_identifier_list: List[SmlIdentifier] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("identification")
        list_element = sml.tag("IdentifierList")
        for entry in self.sml_identifier_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class SmlClassification:
    """Represent a sml:classification."""

    sml_classifier_list: List[SmlClassifier] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("classification")
        list_element = sml.tag("ClassifierList")
        for entry in self.sml_classifier_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class SmlDocumentation:
    """Represent a sml:documentation."""

    sml_document_list: List[SmlDocument] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("documentation")
        list_element = sml.tag("DocumentList")
        for entry in self.sml_document_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class GmlName:
    """Represent a gml:name."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("name")
        element.text = self.text
        return element


@dataclass
class SmlValidTime:
    """Represent a sml:validTime."""

    gml_time_period: GmlTimePeriod

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("validTime")
        element.append(self.gml_time_period.to_xml())
        return element


# Forward definition. Later replaced by the "real" data class.
class SmlPhysicalSystem:
    """Forward definition to be replaced later."""

    pass


@dataclass
class SmlComponent:
    """Represent the sml:component."""

    sml_physical_system: SmlPhysicalSystem
    name: Optional[str] = None
    xlink_href: Optional[str] = None
    xlink_title: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("component")
        if self.xlink_href:
            element.attrib[xlink.attrib("href")] = self.xlink_href
        if self.xlink_title:
            element.attrib[xlink.attrib("title")] = self.xlink_title
        if self.name:
            element.attrib["name"] = self.name
        element.append(self.sml_physical_system.to_xml())
        return element


@dataclass
class SmlComponents:
    """Represent the sml:components."""

    sml_component_list: List[SmlComponent] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("components")
        list_element = sml.tag("ComponentList")
        for entry in self.sml_component_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class SmlSetValue:
    """Represent the sml:setValue."""

    ref: str
    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("setValue")
        element.attrib["ref"] = self.ref
        element.text = self.text
        return element


@dataclass
class SmlSettings:
    """Represent the sml:Settings."""

    sml_set_value: SmlSetValue

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("Settings")
        element.append(self.sml_set_value.to_xml())
        return element


@dataclass
class SmlConfiguration:
    """Represent the sml:configuration."""

    sml_settings: SmlSettings

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("configuration")
        element.append(self.sml_settings.to_xml())
        return element


@dataclass
class SmlEvent:
    """Represent a sml:event."""

    sml_classification: SmlClassification
    sml_time: SmlTime
    sml_configuration: Optional[SmlConfiguration] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("event")
        sub_element = sml.tag("Event")
        sub_element.append(self.sml_classification.to_xml())
        sub_element.append(self.sml_time.to_xml())
        if self.sml_configuration:
            sub_element.append(self.sml_configuration.to_xml())
        element.append(sub_element)
        return element


@dataclass
class SmlHistory:
    """Represent a sml:history."""

    sml_event_list: List[SmlEvent] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("history")
        list_element = sml.tag("EventList")
        for entry in self.sml_event_list:
            list_element.append(entry.to_xml())
        element.append(list_element)
        return element


@dataclass
class GmlPos:
    """Represent a gml:pos."""

    x: float
    y: float

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("pos")
        element.text = f"{self.x} {self.y}"
        return element


@dataclass
class GmlLinearRing:
    """Represent a gml:LinearRing."""

    gml_pos_list: List[GmlPos]

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("LinearRing")
        for pos in self.gml_pos_list:
            element.append(pos.to_xml())
        return element


@dataclass
class GmlExterior:
    """Represent a gml:exterior."""

    gml_linear_ring: GmlLinearRing

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("exterior")
        element.append(self.gml_linear_ring.to_xml())
        return element


@dataclass
class GmlPolygon:
    """Represent a gml:Polygon."""

    gml_id: str
    gml_exterior: GmlExterior
    srs_name: Optional[str] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("Polygon")
        element.attrib[gml.attrib("id")] = self.gml_id
        if self.srs_name:
            element.attrib["srsName"] = self.srs_name
        element.append(self.gml_exterior.to_xml())
        return element


@dataclass
class GmlLocation:
    """Represents a gml:location."""

    gml_polygon: Optional[GmlPolygon] = None

    def to_xml(self):
        """Transform to xml element."""
        element = gml.tag("location")
        if self.gml_polygon:
            element.append(self.gml_polygon.to_xml())
        return element


@dataclass
class SweExtension:
    """Represent a swe:extension."""

    gmd_ci_address: Optional[GmdCiAddress] = None
    gml_polygon: Optional[GmlPolygon] = None

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("extension")
        if self.gmd_ci_address:
            element.append(self.gmd_ci_address.to_xml())
        if self.gml_polygon:
            element.append(self.gml_polygon.to_xml())
        return element


@dataclass
class SweValue:
    """Represent a swe:value."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("value")
        element.text = self.text
        return element


@dataclass
class SweText:
    """Represent a swe:Text."""

    swe_value: Optional[SweValue] = None
    swe_extension: Optional[SweExtension] = None

    def to_xml(self):
        """Transform to xml element."""
        element = swe.tag("Text")
        if self.swe_value:
            element.append(self.swe_value.to_xml())
        if self.swe_extension:
            element.append(self.swe_extension.to_xml())
        return element


@dataclass
class SmlPosition:
    """Represent a sml:position."""

    swe_text: Optional[SweText] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("position")
        if self.swe_text:
            element.append(self.swe_text.to_xml())
        return element


@dataclass
class SmlKeyword:
    """Represent a sml:keyword."""

    text: str

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("keyword")
        element.text = self.text
        return element


@dataclass
class SmlKeywords:
    """Represent a sml:keywords."""

    sml_keyword_list: List[SmlKeyword] = field(default_factory=lambda: [])

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("keywords")
        sub_element = sml.tag("KeywordList")
        for entry in self.sml_keyword_list:
            sub_element.append(entry.to_xml())
        element.append(sub_element)
        return element


@dataclass
class SmlPhysicalSystem:
    """Represent a sml:PhysicalSystem."""

    gml_id: Optional[str] = None
    gml_name: Optional[GmlName] = None
    gml_description: Optional[GmlDescription] = None
    gml_location: Optional[GmlLocation] = None
    sml_keywords: Optional[SmlKeywords] = None
    sml_identification: Optional[SmlIdentification] = None
    sml_classification: Optional[SmlClassification] = None
    sml_documentation: Optional[SmlDocumentation] = None
    sml_contacts: Optional[SmlContacts] = None
    sml_outputs: Optional[SmlOutputs] = None
    sml_parameters: Optional[SmlParameters] = None
    sml_valid_time: Optional[SmlValidTime] = None
    sml_history: Optional[SmlHistory] = None
    sml_components: Optional[SmlComponents] = None
    sml_position: Optional[SmlPosition] = None

    def to_xml(self):
        """Transform to xml element."""
        element = sml.tag("PhysicalSystem")
        if self.gml_id:
            element.attrib[gml.attrib("id")] = self.gml_id
        if self.gml_description:
            element.append(self.gml_description.to_xml())
        if self.gml_name:
            element.append(self.gml_name.to_xml())
        if self.gml_location:
            element.append(self.gml_location.to_xml())
        if self.sml_keywords:
            element.append(self.sml_keywords.to_xml())
        if self.sml_valid_time:
            element.append(self.sml_valid_time.to_xml())
        if self.sml_identification:
            element.append(self.sml_identification.to_xml())
        if self.sml_classification:
            element.append(self.sml_classification.to_xml())
        if self.sml_documentation:
            element.append(self.sml_documentation.to_xml())
        if self.sml_contacts:
            element.append(self.sml_contacts.to_xml())
        if self.sml_outputs:
            element.append(self.sml_outputs.to_xml())
        if self.sml_history:
            element.append(self.sml_history.to_xml())
        if self.sml_parameters:
            element.append(self.sml_parameters.to_xml())
        if self.sml_position:
            element.append(self.sml_position.to_xml())
        if self.sml_components:
            element.append(self.sml_components.to_xml())

        return element

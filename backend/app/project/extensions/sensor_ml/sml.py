# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

# # Adopted from https://github.com/nanoos-pnw/ioos-ws/blob/master/sensorml.py
# # This still Work in Progress.
#
# # import errno
# # import io
# # import os
# from collections import OrderedDict
#
# import pandas as pd
# # from jinja2 import Environment, PackageLoader
# from owslib.etree import etree
# # from owslib.namespaces import Namespaces
# from owslib.util import extract_xml_list, testXMLAttribute, testXMLValue
#
#
# # from datetime import datetime
#
#
# class Namespaces_:
#     """
#     Class for holding and maniputlating a dictionary containing the various namespaces for
#     each standard.
#     """
#
#     namespace_dict = {
#         "atom": "http://www.w3.org/2005/Atom",
#         "csw": "http://www.opengis.net/cat/csw/2.0.2",
#         "csw30": "http://www.opengis.net/cat/csw/3.0",
#         "dc": "http://purl.org/dc/elements/1.1/",
#         "dct": "http://purl.org/dc/terms/",
#         "dif": "http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/",
#         "draw": "gov.usgs.cida.gdp.draw",
#         "fes": "http://www.opengis.net/fes/2.0",
#         "fgdc": "http://www.opengis.net/cat/csw/csdgm",
#         "gco": "http://www.isotc211.org/2005/gco",
#         "gfc": "http://www.isotc211.org/2005/gfc",
#         "gm03": "http://www.interlis.ch/INTERLIS2.3",
#         "gmd": "http://www.isotc211.org/2005/gmd",
#         "gmi": "http://www.isotc211.org/2005/gmi",
#         "gml": "http://www.opengis.net/gml/3.2",
#         "gml311": "http://www.opengis.net/gml",
#         "gml32": "http://www.opengis.net/gml/3.2",
#         "gmx": "http://www.isotc211.org/2005/gmx",
#         "gts": "http://www.isotc211.org/2005/gts",
#         "ogc": "http://www.opengis.net/ogc",
#         "om": "http://www.opengis.net/om/1.0",
#         "om10": "http://www.opengis.net/om/1.0",
#         "om100": "http://www.opengis.net/om/1.0",
#         "om20": "http://www.opengis.net/om/2.0",
#         "ows": "http://www.opengis.net/ows",
#         "ows100": "http://www.opengis.net/ows",
#         "ows110": "http://www.opengis.net/ows/1.1",
#         "ows200": "http://www.opengis.net/ows/2.0",
#         "rim": "urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0",
#         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
#         "sa": "http://www.opengis.net/sampling/1.0",
#         "sml": "http://www.opengis.net/sensorml/2.0",
#         "sml101": "http://www.opengis.net/sensorML/1.0.1",
#         "sos": "http://www.opengis.net/sos/1.0",
#         "sos20": "http://www.opengis.net/sos/2.0",
#         "srv": "http://www.isotc211.org/2005/srv",
#         "swe": "http://www.opengis.net/swe/2.0",
#         "swe10": "http://www.opengis.net/swe/1.0",
#         "swe101": "http://www.opengis.net/swe/1.0.1",
#         "swe20": "http://www.opengis.net/swe/2.0",
#         "swes": "http://www.opengis.net/swes/2.0",
#         "tml": "ttp://www.opengis.net/tml",
#         "wfs": "http://www.opengis.net/wfs",
#         "wfs20": "http://www.opengis.net/wfs/2.0",
#         "wcs": "http://www.opengis.net/wcs",
#         "wms": "http://www.opengis.net/wms",
#         "wps": "http://www.opengis.net/wps/1.0.0",
#         "wps100": "http://www.opengis.net/wps/1.0.0",
#         "xlink": "http://www.w3.org/1999/xlink",
#         "xs": "http://www.w3.org/2001/XMLSchema",
#         "xs2": "http://www.w3.org/XML/Schema",
#         "xsi": "http://www.w3.org/2001/XMLSchema-instance",
#         "wml2": "http://www.opengis.net/waterml/2.0",
#     }
#
#     def get_namespace(self, key):
#         """
#         Retrieves a namespace from the dictionary
#
#         Example:
#         --------
#
#         >> from owslib.namespaces import Namespaces
#         >> ns = Namespaces()
#         >> ns.get_namespace('csw')
#         'http://www.opengis.net/cat/csw/2.0.2'
#         >> ns.get_namespace('wfs20')
#         'http://www.opengis.net/wfs/2.0'
#         """
#         retval = None
#         if key in self.namespace_dict:
#             retval = self.namespace_dict[key]
#         return retval
#
#     def get_versioned_namespace(self, key, ver=None):
#         """
#         Retrieves a namespace from the dictionary with a specific version number
#
#         Example:
#         --------
#
#         >> from owslib.namespaces import Namespaces
#         >> ns = Namespaces()
#         >> ns.get_versioned_namespace('ows')
#         'http://www.opengis.net/ows'
#         >> ns.get_versioned_namespace('ows','1.1.0')
#         'http://www.opengis.net/ows/1.1'
#         """
#
#         if ver is None:
#             return self.get_namespace(key)
#
#         version = ""
#         # Strip the decimals out of the passed in version
#         for s in ver.split("."):
#             version += s
#
#         key += version
#
#         retval = None
#         if key in self.namespace_dict:
#             retval = self.namespace_dict[key]
#
#         return retval
#
#     def get_namespaces(self, keys=None):
#         """
#         Retrieves a dict of namespaces from the namespace mapping
#
#         Parameters
#         ----------
#         - keys: List of keys query and return
#
#         Example:
#         --------
#         >> ns = Namespaces()
#         >> x = ns.get_namespaces(['csw','gmd'])
#         >> x == {'csw': 'http://www.opengis.net/cat/csw/2.0.2', 'gmd': 'http://www.isotc211.org/2005/gmd'}
#         True
#         >> x = ns.get_namespaces('csw')
#         >> x == {'csw': 'http://www.opengis.net/cat/csw/2.0.2'}
#         True
#         >> ns.get_namespaces()
#         {...}
#         """
#         # If we aren't looking for any namespaces in particular return the whole dict
#         if keys is None or len(keys) == 0:
#             return self.namespace_dict
#
#         if isinstance(keys, str):
#             return {keys: self.get_namespace(keys)}
#
#         retval = {}
#         for key in keys:
#             retval[key] = self.get_namespace(key)
#
#         return retval
#
#     def get_namespace_from_url(self, url):
#         for k, v in list(self.namespace_dict.items()):
#             if v == url:
#                 return k
#         return None
#
#
# def get_namespaces():
#     n = Namespaces_()
#     namespaces = n.get_namespaces(["sml", "gml", "xlink", "gmd", "gco"])
#     namespaces["ism"] = "urn:us:gov:ic:ism:v2"
#     return namespaces
#
#
# def nspath_eval(xpath, namespaces):
#     """Return an etree friendly xpath"""
#     out = []
#     for chunks in xpath.split("/"):
#         namespace, element = chunks.split(":")
#         out.append("{%s}%s" % (namespaces[namespace], element))
#     return "/".join(out)
#
#
# namespaces = get_namespaces()
#
#
# def nsp(path):
#     return nspath_eval(path, namespaces)
#
#
# class PhysicalSystem:
#     def __init__(self, element):
#         self.identifiers = None
#         self.classifiers = None
#         if isinstance(element, str) or isinstance(element, bytes):
#             self._root = etree.fromstring(element)
#         else:
#             self._root = element
#
#         if hasattr(self._root, "getroot"):
#             self._root = self._root.getroot()
#         GeneralInfoGroup.__init__(self, self._root)
#         AbstractProcess.__init__(self, self._root)
#         PhysicalPropertiesGroup.__init__(self, self._root)
#         CompositePropertiesGroup.__init__(self, self._root)
#
#     def get_identifiers_by_name(self, name):
#         """
#         Return list of Identifier objects by name, case insensitive
#         """
#         return [
#             self.identifiers[identifier]
#             for identifier in list(self.identifiers.keys())
#             if identifier.lower() == name.lower()
#         ]
#
#     def get_classifiers_by_name(self, name):
#         """
#         Return list of Classifier objects by name, case insensitive
#         """
#         return [
#             self.classifiers[classi]
#             for classi in list(self.classifiers.keys())
#             if classi.lower() == name.lower()
#         ]
#
#     def sensor_as_df(self):
#         """
#         returns a data from the object
#         :return:
#         """
#         sensor = OrderedDict()
#         sensor["station_urn"] = ""
#         sensor["sos_url"] = "sos_url_params"
#         sensor["describesensor_url"] = "describe_sensor_url[station_urn]"
#         sensor["shortName"] = "ds.shortName"
#         sensor["longName"] = "ds.longName"
#         sensor["platformType"] = "ds.platformType"
#         sensor["parameters"] = ",".join(sensor["variables"])
#
#         station_recs = []
#         station_recs.append(sensor)
#         stations_df = pd.DataFrame.from_records(station_recs, columns=sensor.keys())
#         stations_df.index = stations_df["station_urn"]
#         return stations_df
#
#     # def generate_iso(self, df):
#     #     """ """
#     #
#     #     # set up the Jinja2 template:
#     #     env = Environment(
#     #         loader=PackageLoader("sensorml2iso", "templates"),
#     #         trim_blocks=True,
#     #         lstrip_blocks=True,
#     #         autoescape=True,
#     #     )
#     #     template = env.get_template("sensorml_iso.xml")
#     #
#     #     for idx, station in df.iterrows():
#     #         ctx = {}
#     #         # populate some general elements for the template:
#     #         # we can use format filters in the template to format dates...
#     #         # ctx['metadataDate'] = "{metadata_date:%Y-%m-%d}".format(metadata_date=datetime.today())
#     #         ctx["metadataDate"] = datetime.now()
#     #
#     #         # debug: get the first station:
#     #         # station = df.iloc[0]
#     #
#     #         ctx["identifier"] = station.station_urn
#     #         ctx["contacts_dct"] = station["contacts_dct"]
#     #         ctx["documents_dct"] = station["documents_dct"]
#     #
#     #         ctx["sos_url"] = station["sos_url"]
#     #         ctx["describesensor_url"] = station["describesensor_url"]
#     #
#     #         ctx["lon"] = station["lon"]
#     #         ctx["lat"] = station["lat"]
#     #         ctx["shortName"] = station.shortName
#     #         ctx["longName"] = station.longName
#     #         ctx["wmoID"] = station.wmoID
#     #         ctx["serverName"] = station.serverName
#     #
#     #         ctx["title"] = station.title
#     #         ctx["abstract"] = station.abstract
#     #         ctx["keywords"] = station.keywords
#     #         ctx["beginServiceDate"] = station.begin_service_date
#     #
#     #         ctx["platformType"] = station.platformType
#     #         ctx["parentNetwork"] = station.parentNetwork
#     #         ctx["sponsor"] = station.sponsor
#     #
#     #         ctx["starting"] = station.starting
#     #         ctx["ending"] = station.ending
#     #
#     #         ctx["parameter_uris"] = station.parameter_uris
#     #         ctx["parameters"] = station.parameter_uris
#     #         ctx["variables"] = station.variables
#     #         ctx["response_formats"] = station.response_formats
#     #         ctx["download_formats"] = station.download_formats
#     #         ctx["getobs_req_dct"] = station.getobs_req_dct
#     #
#     #         output_filename = os.path.join(
#     #             self.output_directory,
#     #             "{serverName}-{station}.xml".format(
#     #                 serverName=self.server_name,
#     #                 station=station.station_urn.replace(":", "_"),
#     #             ),
#     #         )
#     #         try:
#     #             iso_xml = template.render(ctx)
#     #             output_file = io.open(output_filename, mode="wt", encoding="utf8")
#     #             output_file.write(iso_xml)
#     #             output_file.close()
#     #             if self.verbose:
#     #                 self.log.write(
#     #                     "\n\nMetadata for station: {station} written to output file: {out_file}".format(
#     #                         station=station.station_urn,
#     #                         out_file=os.path.abspath(output_filename),
#     #                     )
#     #                 )
#     #                 print(
#     #                     "\nMetadata for station: {station} written to output file: {out_file}".format(
#     #                         station=station.station_urn,
#     #                         out_file=os.path.abspath(output_filename),
#     #                     )
#     #                 )
#     #         except OSError as ex:
#     #             if ex.errno == errno.EEXIST:
#     #                 if self.verbose:
#     #                     self.log.write(
#     #                         "\nWarning, output file: {out_file} already exists, and can't be written to, \
#     #                         skipping.".format(
#     #                             out_file=output_filename
#     #                         )
#     #                     )
#     #                     print(
#     #                         "Warning, output file: {out_file} already exists, and can't be written to, \
#     #                         skipping.".format(
#     #                             out_file=output_filename
#     #                         )
#     #                     )
#     #             else:
#     #                 self.log.write(
#     #                     "Warning: Unable to open output file: {out_file} for writing, skipping.".format(
#     #                         out_file=output_filename
#     #                     )
#     #                 )
#     #                 print(
#     #                     "Warning: Unable to open output file: {out_file} for writing, skipping.".format(
#     #                         out_file=output_filename
#     #                     )
#     #                 )
#     #                 continue
#
#
# class Member:
#     def __new__(cls, element):
#         t = element[-1].tag.split("}")[-1]
#
#         if t == "PhysicalSystem":
#             return System(element.find(nsp("sml:PhysicalSystem")))
#         elif t == "ProcessChain":
#             return ProcessChain(element.find(nsp("sml:ProcessChain")))
#         elif t == "ProcessModel":
#             return ProcessModel(element.find(nsp("sml:ProcessModel")))
#         elif t == "Component":
#             return Component(element.find(nsp("sml:Component")))
#
#
# class PropertyGroup:
#     def __init__(self, element):
#
#         self.capabilities = []
#         for capability in element.findall(
#             nsp("sml:capabilities/sml:CapabilityList/sml:capability")
#         ):
#             cap = Capability(capability)
#             self.capabilities.append(cap.__dict__)
#
#         self.characteristics = []
#         for cha in element.findall(
#             nsp("sml:characteristics/sml:CharacteristicList/sml:characteristic")
#         ):
#             name = testXMLAttribute(cha, "name")
#             if name is not None:
#                 self.characteristics[name] = cha[0]
#
#     def get_capabilities_by_name(self, name):
#         """
#         Return list of element by name, case insensitive
#         """
#         match = None
#         for capab in list(self.capabilities.keys()):
#             if capab.lower() == name.lower():
#                 match = self.capabilities[capab]
#         return match
#
#     def get_characteristics_by_name(self, name):
#         """
#         Return list of element objects by name, case insensitive
#         """
#         match = None
#         for charac in list(self.characteristics.keys()):
#             if charac.lower() == name.lower():
#                 match = self.characteristics[charac]
#         return match
#
#
# class ConstraintGroup:
#     def __init__(self, element):
#         # ism:SecurityAttributesOptionsGroup
#         self.security = element.findall(
#             nsp("sml:securityConstraint/sml:Security/ism:SecurityAttributesOptionGroup")
#         )
#         # gml:TimeInstant or gml:TimePeriod element
#         self.validTime = element.find(nsp("sml:validTime"))
#         self.rights = [
#             Right(x) for x in element.findall(nsp("sml:legalConstraint/sml:Rights"))
#         ]
#
#
# class Documentation:
#     def __init__(self, element):
#         self.arcrole = testXMLAttribute(element, nsp("xlink:arcrole"))
#         self.url = testXMLAttribute(element, nsp("xlink:href"))
#         self.documents = [Document(d) for d in element.findall(nsp("sml:Document"))]
#
#
# class Document:
#     def __init__(self, element):
#         self.id = testXMLAttribute(element, nsp("gml:id"))
#         self.version = testXMLValue(element.find(nsp("sml:version")))
#         self.description = testXMLValue(element.find(nsp("gml:description")))
#         self.date = testXMLValue(element.find(nsp("sml:date")))
#         try:
#             self.contact = Contact(element.find(nsp("sml:contact")))
#         except AttributeError:
#             self.contact = None
#         self.format = testXMLValue(element.find(nsp("sml:format")))
#         self.url = testXMLAttribute(
#             element.find(nsp("sml:onlineResource")), nsp("xlink:href")
#         )
#
#
# class Right:
#     def __init__(self, element):
#         self.id = testXMLAttribute(element, nsp("gml:id"))
#         self.privacyAct = testXMLAttribute(element, nsp("sml:privacyAct"))
#         self.intellectualPropertyRights = testXMLAttribute(
#             element, nsp("sml:intellectualPropertyRights")
#         )
#         self.copyRights = testXMLAttribute(element, nsp("sml:copyRights"))
#         self.documentation = [
#             Documentation(x) for x in element.findall(nsp("sml:documentation"))
#         ]
#
#
# class ReferenceGroup:
#     def __init__(self, element):
#         self.contacts = []
#         for contact in element.findall(nsp("sml:contacts/sml:ContactList/sml:contact")):
#             cont = Contact(contact)
#             self.contacts.append(cont.__dict__)
#
#         self.documentation = [
#             Documentation(x) for x in element.findall(nsp("sml:documentation"))
#         ]
#
#
# class GeneralInfoGroup:
#     def __init__(self, element):
#         self.keywords = extract_xml_list(
#             element.findall(nsp("sml:keywords/sml:KeywordList/sml:keyword"))
#         )
#
#         self.identifiers = {}
#         for identifier in element.findall(
#             nsp("sml:identification/sml:IdentifierList/sml:identifier")
#         ):
#             ident = Identifier(identifier)
#             self.identifiers[ident.label] = ident.value
#             self.identifiers[f"{ident.label} Definition"] = ident.definition
#
#         self.classifiers = {}
#         for classifier in element.findall(
#             nsp("sml:classification/sml:ClassifierList/sml:classifier")
#         ):
#             classi = Classifier(classifier)
#             self.classifiers[classi.label] = classi.value
#             self.classifiers[f"{classi.label} Definition"] = classi.definition
#
#     def get_identifiers_by_name(self, name):
#         """
#         Return list of Identifier objects by name, case insensitive
#         """
#         match = None
#         for identifier in list(self.identifiers.keys()):
#             if identifier.lower() == name.lower():
#                 match = self.identifiers[identifier]
#         return match
#
#     def get_classifiers_by_name(self, name):
#         """
#         Return list of Classifier objects by name, case insensitive
#         """
#         match = None
#         for classi in list(self.classifiers.keys()):
#             if classi.lower() == name.lower():
#                 match = self.classifiers[classi]
#         return match
#
#
# class Contact:
#     def __init__(self, element):
#         # contact information here.
#         self.role = testXMLAttribute(
#             element.find(nsp("gmd:CI_ResponsibleParty/sml:role")), nsp("gco:nilReason")
#         )
#         # self.role = testXMLAttribute(element.find(nsp("gmd:role"), "gco:nilReason"))
#         self.href = testXMLAttribute(element, nsp("xlink:href"))
#         self.organization = testXMLValue(
#             element.find(
#                 nsp("gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString")
#             )
#         )
#         self.name = testXMLValue(
#             element.find(
#                 nsp("gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString")
#             )
#         )
#         self.phone = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:voice"
#                 )
#             )
#         )
#         self.address = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/\
#                     gmd:deliveryPoint/gco:CharacterString"
#                 )
#             )
#         )
#         self.city = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/\
#                     gmd:CI_Address/gmd:city/gco:CharacterString"
#                 )
#             )
#         )
#         self.region = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/\
#                     gmd:administrativeArea/gco:CharacterString"
#                 )
#             )
#         )
#         self.postcode = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/\
#                     gmd:postalCode/gco:CharacterString"
#                 )
#             )
#         )
#         self.country = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/\
#                     gmd:country/gco:CharacterString"
#                 )
#             )
#         )
#         self.email = testXMLValue(
#             element.find(
#                 nsp(
#                     "gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/\
#                     gmd:electronicMailAddress/gco:CharacterString"
#                 )
#             )
#         )
#         self.url = testXMLAttribute(
#             element.find(
#                 nsp("sml:ResponsibleParty/gmd:contactInfo/gmd:onlineResource")
#             ),
#             nsp("xlink:href"),
#         )
#
#
# class HistoryGroup:
#     def __init__(self, element):
#         self.history = {}
#         for event_member in element.findall(nsp("sml:history/sml:EventList/sml:event")):
#             self.classifiers = {}
#             for classifier in element.findall(
#                 nsp("sml:classification/sml:ClassifierList/sml:classifier")
#             ):
#                 classi = Classifier(classifier)
#                 self.classifiers[classi.label] = classi.value
#
#             # name = testXMLAttribute(event_member, "name")
#             # if self.history.get(name) is None:
#             #     self.history[name] = []
#             for e in event_member.findall(nsp("sml:Event")):
#                 for classifier in e.findall(
#                     nsp("sml:classification/sml:ClassifierList/sml:classifier")
#                 ):
#                     classi = Classifier(classifier)
#                     self.classifiers[classi.label] = classi.value
#                     self.history[classi.label.replace(" ", "_")] = classi.__dict__
#                 # for time in e.findall(
#                 #         nsp("sml:time/gml:TimePeriod")
#                 # ):
#                 #     timi = Time(time)
#                 #     self.times[timi.description] = timi
#                 #     self.history[timi.label.replace(" ", "_")] = timi.__dict__
#
#     def get_history_by_name(self, name):
#         """
#         Return Events list by members name
#         """
#         return self.history.get(name.lower(), [])
#
#
# class Event(ReferenceGroup, GeneralInfoGroup):
#     def __init__(self, element):
#         ReferenceGroup.__init__(self, element)
#         GeneralInfoGroup.__init__(self, element)
#         self.id = testXMLAttribute(element, nsp("gml:id"))
#         self.date = testXMLValue(element.find(nsp("sml:date")))
#         self.description = testXMLValue(element.find(nsp("gml:description")))
#
#
# class MetadataGroup(
#     GeneralInfoGroup, PropertyGroup, ConstraintGroup, ReferenceGroup, HistoryGroup
# ):
#     def __init__(self, element):
#         GeneralInfoGroup.__init__(self, element)
#         PropertyGroup.__init__(self, element)
#         ConstraintGroup.__init__(self, element)
#         ReferenceGroup.__init__(self, element)
#         HistoryGroup.__init__(self, element)
#
#
# class AbstractFeature:
#     def __init__(self, element):
#         self.name = testXMLValue(element.find(nsp("gml:name")))
#         self.description = testXMLValue(element.find(nsp("gml:description")))
#         self.gmlBoundedBy = testXMLValue(element.find(nsp("gml:boundedBy")))
#
#
# class AbstractProcess(AbstractFeature, MetadataGroup):
#     def __init__(self, element):
#         AbstractFeature.__init__(self, element)
#         MetadataGroup.__init__(self, element)
#         # sml:IoComponentPropertyType
#         self.inputs = element.findall(nsp("sml:input"))
#         # sml:IoComponentPropertyType
#         self.outputs = element.findall(nsp("sml:output"))
#         # swe:DataComponentPropertyType
#         self.parameters = element.findall(nsp("sml:parameter"))
#
#
# class AbstractRestrictedProcess(AbstractFeature):
#     """Removes ('restricts' in xml schema language) gml:name, gml:description,
#     and sml:metadataGroup from an AbstractProcess"""
#
#     def __init__(self, element):
#         AbstractFeature.__init__(self, element)
#         self.name = None
#         self.description = None
#
#
# class AbstractPureProcess(AbstractRestrictedProcess):
#     def __init__(self, element):
#         AbstractRestrictedProcess.__init__(self, element)
#
#         # sml:IoComponentPropertyType
#         self.inputs = element.findall(nsp("sml:input"))
#         # sml:IoComponentPropertyType
#         self.outputs = element.findall(nsp("sml:output"))
#         # swe:DataComponentPropertyType
#         self.parameters = element.findall(nsp("sml:parameter"))
#
#
# class ProcessModel(AbstractPureProcess):
#     def __init__(self, element):
#         AbstractPureProcess.__init__(self, element)
#         self.method = ProcessMethod(element.find("method"))
#
#
# class CompositePropertiesGroup:
#     def __init__(self, element):
#         # All components should be of instance AbstractProcess (sml:_Process)
#         self.components = element.findall(
#             nsp("sml:components/sml:ComponentList/sml:component")
#         )
#         # sml:Link or sml:ArrayLink element
#         self.connections = element.findall(
#             nsp("sml:connections/sml:ConnectionList/sml:connection")
#         )
#
#
# class PhysicalPropertiesGroup:
#     def __init__(self, element):
#         # gml:EngieeringCRS element
#         self.spatialReferenceFrame = element.find(
#             nsp("sml:spatialReferenceFrame/gml:EngineeringCRS")
#         )
#         # gml:TemporalCRS element
#         self.temporalReferenceFrame = element.find(
#             nsp("sml:temporalReferenceFrame/gml:TemporalCRS")
#         )
#         # gml:Envelope element
#         self.smlBoundedBy = element.find(nsp("sml:boundedBy"))
#         # swe:Time or sml:_Process element
#         self.timePosition = element.find(nsp("sml:timePosition"))
#
#         # It is either a sml:position OR and sml:location element here.  Process both.
#         # swe:Position, swe:Vector, or sml:_Process element
#         self.positions = element.findall(nsp("sml:position"))
#         # gml:Point of gml:_Curve
#         self.location = element.find(nsp("sml:location"))
#
#         try:
#             self.interface = Interface(element.find(nsp("sml:interface")))
#         except AttributeError:
#             self.interface = None
#
#
# class ProcessChain(AbstractPureProcess, CompositePropertiesGroup):
#     def __init__(self, element):
#         AbstractPureProcess.__init__(self, element)
#         CompositePropertiesGroup.__init__(self, element)
#
#
# class System(AbstractProcess, PhysicalPropertiesGroup, CompositePropertiesGroup):
#     def __init__(self, element):
#         AbstractProcess.__init__(self, element)
#         PhysicalPropertiesGroup.__init__(self, element)
#         CompositePropertiesGroup.__init__(self, element)
#
#
# class Component(AbstractProcess, PhysicalPropertiesGroup):
#     def __init__(self, element):
#         AbstractProcess.__init__(self, element)
#         PhysicalPropertiesGroup.__init__(self, element)
#         self.method = ProcessMethod(element.find("method"))
#
#
# class Term:
#     def __init__(self, element):
#         self.codeSpace = testXMLAttribute(
#             element.find(nsp("sml:Term/sml:codeSpace")), nsp("xlink:href")
#         )
#         self.definition = testXMLAttribute(element.find(nsp("sml:Term")), "definition")
#         self.label = testXMLValue(element.find(nsp("sml:Term/sml:label")))
#         self.value = testXMLValue(element.find(nsp("sml:Term/sml:value")))
#
#
# class DataRecord:
#     def __init__(self, element):
#         self.codeSpace = testXMLAttribute(
#             element.find(nsp("swe:DataRecord/sml:codeSpace")), nsp("xlink:href")
#         )
#         self.definition = testXMLAttribute(
#             element.find(nsp("swe:characteristic")), "definition"
#         )
#         self.label = testXMLValue(element.find(nsp("swe:DataRecord/swe:label")))
#         self.value = testXMLValue(element.find(nsp("swe:DataRecord/swe:value")))
#
#
# class Characteristic(DataRecord):
#     def __init__(self, element):
#         DataRecord.__init__(self, element)
#
#
# class Capability(DataRecord):
#     def __init__(self, element):
#         DataRecord.__init__(self, element)
#
#
# class Classifier(Term):
#     def __init__(self, element):
#         Term.__init__(self, element)
#
#
# class Identifier(Term):
#     def __init__(self, element):
#         Term.__init__(self, element)
#
#
# # class TimePeriod:
# #     def __init__(self, element):
# #         self.codeSpace = testXMLAttribute(
# #             element.find(nsp("sml:Term/sml:codeSpace")), nsp("xlink:href")
# #         )
# #         self.definition = testXMLAttribute(element.find(nsp("sml:Term")), "definition")
# #         self.label = testXMLValue(element.find(nsp("sml:Term/sml:label")))
# #         self.value = testXMLValue(element.find(nsp("sml:Term/sml:value")))
# #
# #
# # class Time(TimePeriod):
# #     def __init__(self, element):
# #         Term.__init__(self, element)
# #         super().__init__(element)
#
#
# class ProcessMethod(MetadataGroup):
#     """Inherits from gml:AbstractGMLType"""
#
#     def __init__(self, element):
#         MetadataGroup.__init__(self, element)
#         self.rules = element.find(nsp("sml:rules"))
#         self.ioStructure = element.find(nsp("sml:IOStructureDefinition"))
#         self.algorithm = element.find(nsp("sml:algorithm"))
#         self.implementations = element.findall(nsp("sml:implementation"))
#
#
# class Interface:
#     def __init__(self, element):
#         self.name = testXMLAttribute(element, "name")
#         self.interface_definition = InterfaceDefinition(
#             element.find(nsp("sml:InterfaceDefinition"))
#         )
#
#
# class InterfaceDefinition:
#     def __init__(self, element):
#         raise NotImplementedError(
#             "InterfaceDefinition is not implemented in OWSLib (yet)"
#         )
#
#
# class Link:
#     def __init__(self, element):
#         raise NotImplementedError("Link is not implemented in OWSLib (yet)")
#
#
# class ArrayLink:
#     def __init__(self, element):
#         raise NotImplementedError("ArrayLink is not implemented in OWSLib (yet)")
#
#
# if __name__ == "__main__":
#     pass
#     # xml = open("/tmp/test_1.xml", "rb").read()
#     # root = PhysicalSystem(xml)
#     # print()
#     # print(root.__dict__)
#     # print(root.get_identifiers_by_name("short name"))
#     # description = (root.description or None,)
#     # short_name = (root.get_identifiers_by_name("short name")[0],)
#     # long_name = (root.get_identifiers_by_name("long name")[0],)
#     # serial_number = (root.get_identifiers_by_name("Serial Number"),)
#     # manufacturer_uri = (
#     #     root.get_identifiers_by_name("Manufacturer Definition") or None,
#     # )
#     # manufacturer_name = (root.get_identifiers_by_name("Manufacturer") or None,)
#     # model = (root.get_identifiers_by_name("model Number") or None,)
#     # persistent_identifier = (root.get_identifiers_by_name("uniqueID") or None,)
#     # status_uri = (root.get_identifiers_by_name("System Status Definition") or None,)
#     # status_name = (root.get_identifiers_by_name("System Status") or None,)
#     #
#     # device_type_uri = (root.get_classifiers_by_name("Sensor Type Definition") or None,)
#     # device_type_name = (root.get_classifiers_by_name("Sensor Type") or None,)

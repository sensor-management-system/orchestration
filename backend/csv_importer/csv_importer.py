# SPDX-FileCopyrightText: 2020 - 2023
# - Florian Gransee <florian.gransee@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import numbers

import pandas as pd
import requests

"""
Import processor for devices to an sms instance (currently UFZ only).

How to call it:

>>> SmsDeviceImporter(
        filepath="~/data/somewhere/former_devices_export.csv",
        run_type="local",
        api_key="ABC1234"
    ).process()
"""


class SMSDeviceImporter:
    def __init__(self, filepath, run_type, api_key):
        self.filepath = filepath
        self.run_type = run_type
        self.api_key = api_key
        self.headers = {
            "X-APIKEY": self.api_key,
            "Content-Type": "application/vnd.api+json",
        }
        self.base_urls = {
            "local": "https://localhost.localdomain/backend/api/v1/",
            "stage": "https://webapp-stage.intranet.ufz.de/sms/backend/api/v1/",
            "prod": "https://webapp.ufz.de/sms/backend/api/v1/",
        }
        self.url = self.base_urls[self.run_type]
        self.cv_base_urls = {
            "local": "http://localhost:8000/cv/api/v1/",
            "stage": "https://webapp-stage.intranet.ufz.de/sms/cv/api/v1/",
            "prod": "https://webapp.ufz.de/sms/cv/api/v1/",
        }
        self.cv_base_url = self.cv_base_urls[self.run_type]
        self.cv_mapping = {
            "manufacturer_name": "manufacturers",
            "properties_([0-9]|[1-9][0-9])_unit_name": "units",
            "properties_([0-9]|[1-9][0-9])_compartment_name": "compartments",
            "properties_([0-9]|[1-9][0-9])_property_name": "measuredquantities",
            "properties_([0-9]|[1-9][0-9])_sample_medium_name": "samplingmedia",
            "contact_([0-9]|[1-9][0-9])_contact_role": "contactroles",
        }

    def get_cv_terms(self):
        cv_terms = dict()
        for k, v in self.cv_mapping.items():
            response = requests.get(
                self.cv_base_url + v + "?page[size]=10000", verify=False
            )
            terms = [i["attributes"]["term"] for i in response.json()["data"]]
            cv_terms[v] = terms

        return cv_terms

    def check_cv_entries(self, data):
        cv_terms = self.get_cv_terms()
        not_in_cv = dict()
        for k, v in self.cv_mapping.items():
            l = list()
            for idx, row in data.iterrows():
                e = row.filter(regex=(k))
                l += list(e)
                l = [i for i in l if i != ""]
            not_in_cv[v] = set(list(l)).difference(cv_terms[v])

        return not_in_cv

    def check_cv(self, data):
        not_in_cv = self.check_cv_entries(data)
        missing = list()
        for k, v in not_in_cv.items():
            missing += list(v)
        return not_in_cv, missing

    def attributes_types(self):
        return {
            "properties": {
                "body_method": self.create_device_proerty_body,
                "post_method": self.post_device_property,
            },
            "customfields": {
                "body_method": self.create_customfield_body,
                "post_method": self.post_customfield,
            },
            "attachments": {
                "body_method": self.create_attachment_body,
                "post_method": self.post_attachment,
            },
        }

    def read_device_csv(self):
        data = pd.read_csv(self.filepath, encoding="cp1252", sep=";")
        data = data.fillna("")

        return data

    def get_cv_contactroles(self):
        response = requests.get(
            self.cv_base_url + "contactroles?page[size]=10000", verify=False
        )
        response_json = response.json()["data"]
        cv_roles = {i["attributes"]["term"]: i["links"]["self"] for i in response_json}

        return cv_roles

    @staticmethod
    def get_number_of_attributes(data, attributes_types):
        counters_dict = dict()
        for attribute in attributes_types:
            row_attributes = list(filter(lambda k: attribute in k, data.columns))
            counters = set(int(row.split("_")[1]) for row in row_attributes)
            counters_dict[attribute] = list(counters)

        return counters_dict

    @staticmethod
    def create_contact_body(series, regex):
        body = {
            "data": {
                "attributes": {
                    "given_name": series.get(regex + "_given_name", ""),
                    "family_name": series.get(regex + "_familiy_name", ""),
                    "website": series.get(regex + "_website", None),
                    "email": series.get(regex + "_email", ""),
                },
                "type": "contact",
            }
        }
        return body

    def post_contact(self, body):
        response = requests.post(
            self.url + "contacts", json=body, headers=self.headers, verify=False
        )
        if response.status_code == 201:
            contact_id = response.json()["data"]["id"]
            print("Contact {0} created".format(contact_id))

    def post_contacts(self, data, counter):
        for contact in counter:
            df_contact = data[
                [
                    f"contact_{contact}_given_name",
                    f"contact_{contact}_familiy_name",
                    f"contact_{contact}_email",
                ]
            ]
            df_contact = df_contact.drop_duplicates()
            regex = "contact_" + str(contact)
            for _, row in df_contact.iterrows():
                body = self.create_contact_body(row, regex)
                self.post_contact(body)

    @staticmethod
    def create_post_device_body(row):
        body = {
            "data": {
                "attributes": {
                    "description": row.get("description", None),
                    "short_name": row.get("short_name"),
                    "long_name": row.get("long_name", None),
                    "serial_number": row.get("serial_number"),
                    "manufacturer_uri": row.get("manufacturer_uri", None),
                    "manufacturer_name": row.get("manufacturer_name"),
                    "dual_use": row.get("dual_use", None),
                    "model": row.get("model", None),
                    "inventory_number": str(row.get("inventory_number", None)),
                    # "persistent_identifier": row.get("persistent_identifier"),
                    "website": row.get("website", None),
                    "device_type_uri": row.get("device_type_uri", None),
                    "device_type_name": row.get("device_type_name", None),
                    "status_uri": row.get("status_uri", None),
                    "status_name": row.get("status_name", None),
                    "is_public": row.get("is_public", None),
                    "is_internal": row.get("is_internal", None),
                    "is_private": row.get("is_private", None),
                    "group_ids": str(row.get("group_ids")).split(";"),
                },
                "type": "device",
            }
        }
        return body

    def post_device(self, data_row):
        body = self.create_post_device_body(data_row)
        response = requests.post(
            self.url + "devices", json=body, headers=self.headers, verify=False
        )
        if response.status_code == 201:
            device_id = response.json()["data"]["id"]
            print("device {} created!".format(device_id))
            return device_id, response.status_code
        else:
            return response, response.status_code

    @staticmethod
    def create_attachment_body(series, device_id, regex, cv_roles):
        body = {
            "data": {
                "attributes": {
                    "label": series.get(regex + "_label", ""),
                    "url": series.get(regex + "_url", ""),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device_id}}
                },
                "type": "device_attachment",
            }
        }

        return body

    def post_attachment(self, body):
        response = requests.post(
            self.url + "device-attachments",
            json=body,
            headers=self.headers,
            verify=False,
        )
        if response.status_code == 201:
            attachment_id = response.json()["data"]["id"]
            print(
                "Attachment {0} for device {1} created".format(
                    attachment_id,
                    response.json()["data"]["relationships"]["device"]["data"]["id"],
                )
            )

    @staticmethod
    def create_customfield_body(series, device_id, regex, cv_role):
        value = (
            series.get(regex + "_value")
            if type(series.get(regex + "_value", 0)) != float
            else str(int(series.get(regex + "_value", 0)))
        )
        key = series.get(regex + "_key", "")
        body = {
            "data": {
                "type": "customfield",
                "attributes": {"key": key, "value": value},
                "relationships": {
                    "device": {"data": {"type": "device", "id": device_id}}
                },
            }
        }
        return body

    def post_customfield(self, body):
        response = requests.post(
            self.url + "customfields", json=body, headers=self.headers, verify=False
        )
        if response.status_code == 201:
            customfield_id = response.json()["data"]["id"]
            print(
                "Customfield {0} for device {1} created".format(
                    customfield_id,
                    response.json()["data"]["relationships"]["device"]["data"]["id"],
                )
            )

    @staticmethod
    def check_if_number(value):
        if not isinstance(value, numbers.Number):
            return None

        return value

    def create_device_proerty_body(self, series, device_id, regex, cv_roles):
        measuring_range_min = self.check_if_number(
            series.get(regex + "_measuring_range_min")
        )
        measuring_range_max = self.check_if_number(
            series.get(regex + "_measuring_range_max")
        )
        failure_value = self.check_if_number(series.get(regex + "_failure_value"))
        accuracy = self.check_if_number(series.get(regex + "_accuracy"))
        resolution = self.check_if_number(series.get(regex + "_resolution"))
        body = {
            "data": {
                "attributes": {
                    "measuring_range_min": measuring_range_min,
                    "measuring_range_max": measuring_range_max,
                    "failure_value": failure_value,
                    "accuracy": accuracy,
                    "label": series.get(regex + "_label", ""),
                    "unit_uri": series.get(regex + "_unit_uri", ""),
                    "unit_name": series.get(regex + "_unit_name", ""),
                    "compartment_uri": series.get(regex + "_compartment_uri", ""),
                    "compartment_name": series.get(regex + "_compartment_name", ""),
                    "property_uri": series.get(regex + "_property_uri", ""),
                    "property_name": series.get(regex + "_property_name", ""),
                    "sampling_media_uri": series.get(
                        regex + "_sampling_medium_uri", ""
                    ),
                    "sampling_media_name": series.get(
                        regex + "_sampling_medium_name", ""
                    ),
                    "resolution": resolution,
                    "resolution_unit_uri": series.get(
                        regex + "_resolution_unit_uri", ""
                    ),
                    "resolution_unit_name": series.get(
                        regex + "_resolution_unit_name", ""
                    ),
                },
                "type": "device_property",
                "relationships": {
                    "device": {"data": {"type": "device", "id": device_id}}
                },
            }
        }

        return body

    def post_device_property(self, body):
        response = requests.post(
            self.url + "device-properties",
            json=body,
            headers=self.headers,
            verify=False,
        )
        if response.status_code == 201:
            property_id = response.json()["data"]["id"]
            print(
                "Device property {0} for device {1} created".format(
                    property_id,
                    response.json()["data"]["relationships"]["device"]["data"]["id"],
                )
            )

    def process(self):
        log_list = list()
        data = self.read_device_csv()
        not_in_cv, missing = self.check_cv(data)
        if missing:
            print("The following elements of the csv file are not found in CV:")
            print(not_in_cv)
            return False
        else:
            print("All elements found in CV!")
        cv_roles = self.get_cv_contactroles()
        contact_counter = self.get_number_of_attributes(data, {"contact": {}})
        self.post_contacts(data, contact_counter["contact"])
        attributes_types = self.attributes_types()
        attribute_counter = self.get_number_of_attributes(data, attributes_types)
        for _, row in data.iterrows():
            device_id, status_code = self.post_device(row)
            if status_code == 201:
                for attribute, counter in attribute_counter.items():
                    create_body_method = attributes_types[attribute]["body_method"]
                    post_method = attributes_types[attribute]["post_method"]
                    for c in counter:
                        regex = attribute + "_" + str(c)
                        filtered_data = row.filter(regex=regex)
                        if set(filtered_data.values) != {""}:
                            body = create_body_method(
                                filtered_data, str(device_id), regex, cv_roles
                            )
                            post_method(body)
                log_list.append(
                    {
                        "sms_device_id": device_id,
                        "short_name": row.short_name,
                        "long_name": row.long_name,
                        "serial_number": row.serial_number,
                    }
                )
            else:
                print("error posting device")
                print(status_code)
                print(device_id.text)
        pd.DataFrame(log_list).to_csv(
            f"IMPORT_'{self.filepath}'_{self.run_type}.csv", index=False
        )

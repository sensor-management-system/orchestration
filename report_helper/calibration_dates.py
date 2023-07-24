#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Aim of the script is to crate an overview table of the calibration dates.

This should be done for all devices of a permission group.
"""

import argparse
import dataclasses
import datetime
import fnmatch
import json
import os
import sys
import tempfile
import typing
import webbrowser

import dateutil.parser
import jinja2
import pytz
import requests

URL = "https://sensors.gfz-potsdam.de"
# You may want to set it in the shell with export SMS_APIKEY=123456...
APIKEY = os.environ.get("SMS_APIKEY")


calibrations_template = jinja2.Template(
    """
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body>
        <div class="relative overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50
                     dark:bg-gray-700 dark:text-gray-400"
            >
              <tr>
                <th scope="col" class="px-6 py-3">SMS</th>
                <th scope="col" class="px-6 py-3">Short name</th>
                <th scope="col" class="px-6 py-3">Manufacturer</th>
                <th scope="col" class="px-6 py-3">Model</th>
                <th scope="col" class="px-6 py-3">Serial number</th>
                <th scope="col" class="px-6 py-3">Latest calibration date</th>
                <th scope="col" class="px-6 py-3">Contact for last calibration</th>
              </tr>
            </thead>
            {% for row in rows %}
              <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <a href="{{ url }}/devices/{{ row.device_id }}" target="_blank">
                    <svg
                      class="w-6 h-6 text-gray-800 dark:text-white"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 18 18"
                    >
                      <path
                        d="M17 0h-5.768a1 1 0 1 0 0 2h3.354L8.4
                           8.182A1.003 1.003 0 1 0 9.818 9.6L16
                           3.414v3.354a1 1 0 0 0 2 0V1a1 1 0 0 0-1-1Z"
                      >
                      </path>
                      <path
                        d="m14.258 7.985-3.025 3.025A3 3 0 1 1 6.99
                           6.768l3.026-3.026A3.01 3.01 0 0 1 8.411
                           2H2.167A2.169 2.169 0 0 0 0 4.167v11.666A2.169
                           2.169 0 0 0 2.167 18h11.666A2.169 2.169 0 0 0
                           16 15.833V9.589a3.011 3.011 0 0 1-1.742-1.604Z"
                      >
                      </path>
                    </svg>
                  </a>
                </th>
                <td class="px-6 py-4">{{ row.short_name }}</td>
                <td class="px-6 py-4">{{ row.manufacturer_name }}</td>
                <td class="px-6 py-4">{{ row.model }}</td>
                <td class="px-6 py-4">{{ row.serial_number }}</td>
                <td class="px-6 py-4">
                  {{ row.latest_calibration_date if row.latest_calibration_date else '-' }}
                </td>
                <td class="px-6 py-4">
                  {{ row.contact_name if row.contact_name else '-' }}
                </td>
              </tr>
            {% endfor %}
          </table>
        </div>
      </body>
    </html>
    """
)


@dataclasses.dataclass
class PermissionGroup:
    """Class to represent a sms permission group."""

    id: str
    name: str


@dataclasses.dataclass
class Device:
    """Class to represent a sms device."""

    id: str
    short_name: str
    manufacturer_name: str
    model: str
    serial_number: str
    group_ids: typing.List[str]


@dataclasses.dataclass
class DeviceCalibrationAction:
    """Class to represent a sms calibration action."""

    id: str
    current_calibration_date: datetime.datetime
    device_id: str
    contact_id: str


@dataclasses.dataclass
class Contact:
    """Class to represent a sms contact."""

    id: str
    given_name: str
    family_name: str


class Row:
    """Class to represent a row in our result table."""

    def __init__(
        self, device, latest_calibration, permission_group_lookup, contact_lookup
    ):
        """Init the object."""
        self.device = device
        self.latest_calibration = latest_calibration
        self.permission_group_lookup = permission_group_lookup
        self.contact_lookup = contact_lookup

    @property
    def device_id(self) -> str:
        """Return the id of the device."""
        return self.device.id

    @property
    def short_name(self) -> str:
        """Return the short name of the device."""
        return self.device.short_name

    @property
    def manufacturer_name(self) -> str:
        """Return the manufacturer of the device."""
        return self.device.manufacturer_name

    @property
    def model(self) -> str:
        """Return the model of the device."""
        return self.device.model

    @property
    def serial_number(self) -> str:
        """Return the serial number of the device."""
        return self.device.serial_number

    @property
    def latest_calibration_date(self) -> typing.Optional[str]:
        """Return the latest calibration date as formatted string."""
        if self.latest_calibration:
            return self.latest_calibration.current_calibration_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return None

    @property
    def contact_name(self) -> typing.Optional[str]:
        """Return the optional contact name for the latest calibration."""
        if not self.latest_calibration:
            return None
        contact = self.contact_lookup[self.latest_calibration.contact_id]
        return f"{contact.given_name} {contact.family_name}"


class Sms:
    """Helper class to interact with the SMS backend."""

    def __init__(self, url, apikey):
        """Initialize the object."""
        self.url = url
        self.apikey = apikey

    def get_permission_groups(self) -> typing.List[PermissionGroup]:
        """Return the list of permission groups."""
        resp = requests.get(
            f"{self.url}/backend/api/v1/permission-groups", {"page[size]": 10_000}
        )
        resp.raise_for_status()
        result = []
        for entry in resp.json()["data"]:
            result.append(
                PermissionGroup(id=entry["id"], name=entry["attributes"]["name"])
            )
        return result

    def get_contacts(self) -> typing.List[Contact]:
        """Return the list of contacts."""
        resp = requests.get(
            f"{self.url}/backend/api/v1/contacts",
            {"page[size]": 10_000},
            headers={"X-APIKEY": self.apikey},
        )
        resp.raise_for_status()
        result = []
        for entry in resp.json()["data"]:
            result.append(
                Contact(
                    id=entry["id"],
                    given_name=entry["attributes"]["given_name"],
                    family_name=entry["attributes"]["family_name"],
                )
            )
        return result

    def get_devices(
        self, permission_groups: typing.List[PermissionGroup]
    ) -> typing.List[Device]:
        """Return the list of devices for the permission groups."""
        filter_settings = []
        group_ids = [p.id for p in permission_groups]
        possible_filters = [
            {"name": "group_ids", "op": "any", "val": group_id}
            for group_id in group_ids
        ]
        or_filter = {"or": possible_filters}
        filter_settings.append(or_filter)
        resp = requests.get(
            f"{self.url}/backend/api/v1/devices",
            {
                "page[size]": 10_000,
                "filter": json.dumps(filter_settings, separators=(",", ":")),
                "sort": "short_name",
            },
            headers={"X-APIKEY": self.apikey},
        )
        resp.raise_for_status()
        result = []
        for entry in resp.json()["data"]:
            result.append(
                Device(
                    id=entry["id"],
                    short_name=entry["attributes"]["short_name"],
                    manufacturer_name=entry["attributes"]["manufacturer_name"],
                    model=entry["attributes"]["model"],
                    serial_number=entry["attributes"]["serial_number"],
                    group_ids=entry["attributes"]["group_ids"] or [],
                )
            )
        return result

    def get_calibration_actions(
        self, device: Device
    ) -> typing.List[DeviceCalibrationAction]:
        """Return the list of calibration actions for the device."""
        resp = requests.get(
            f"{self.url}/backend/api/v1/devices/{device.id}/device-calibration-actions",
            {"page[size]": 10_000},
            headers={"X-APIKEY": self.apikey},
        )
        resp.raise_for_status()
        result = []
        for entry in resp.json()["data"]:
            result.append(
                DeviceCalibrationAction(
                    id=entry["id"],
                    current_calibration_date=dateutil.parser.parse(
                        entry["attributes"]["current_calibration_date"]
                    ),
                    device_id=device.id,
                    contact_id=entry["relationships"]["contact"]["data"]["id"],
                )
            )
        return result


def main():
    """Run the main function to get the sms data & create a table to show."""
    usage = """
    Script to create a table with an overview of the latest calibration dates at the moment.

    ./calibration_dates.py <group>
    """
    argument_parser = argparse.ArgumentParser(usage=usage)
    argument_parser.add_argument("group", help="Pattern to search for groupsin the sms")

    args = argument_parser.parse_args()

    sms = Sms(URL, APIKEY)
    permission_groups = sms.get_permission_groups()
    filtered_groups = [
        p for p in permission_groups if fnmatch.fnmatch(p.name, args.group)
    ]
    if not filtered_groups:
        print("No such groups found.", file=sys.stderr)
        exit(-1)
    filtered_groups.sort(key=lambda x: x.name)

    contacts = sms.get_contacts()

    devices = sms.get_devices(filtered_groups)
    rows = []

    now = datetime.datetime.now(pytz.utc)

    permission_group_lookup = {p.id: p for p in permission_groups}
    contact_lookup = {c.id: c for c in contacts}

    for device in devices:
        calibration_actions = sms.get_calibration_actions(device)

        past_calibrations = [
            c for c in calibration_actions if c.current_calibration_date < now
        ]
        latest_calibration = None
        if past_calibrations:
            latest_calibration = past_calibrations[-1]

        row = Row(
            device=device,
            latest_calibration=latest_calibration,
            permission_group_lookup=permission_group_lookup,
            contact_lookup=contact_lookup,
        )

        rows.append(row)

    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w+t", delete=False
    ) as temp_file:
        print(calibrations_template.render(rows=rows, url=URL), file=temp_file)
        webbrowser.open("file://" + temp_file.name)


if __name__ == "__main__":
    main()

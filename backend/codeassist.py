#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


"""
Helper script to solve coding problems for the app.

The logic is not included in the manage.py as it can happen
that the overall container doesn't start properly, so that
the manage.py can't be accessed.

To solve those problems is hard and that is what this module here is for.
"""

import datetime
import functools
import json
import pathlib
import re
from xml.etree import ElementTree

import click
import requests


class Node:
    """Node class to handle a tree like structure."""

    def __init__(self, value):
        """Init the object."""
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """Add a child node."""
        self.children.append(child_node)

    def __repr__(self):
        """Return a string representation of the Node."""
        return f"Node({repr(self.value)}, {repr(self.children)})"


@click.group()
def main():
    """Run the codeassist."""
    pass


@main.group()
def inspect():
    """Inspect data."""
    pass


@inspect.group()
def migrations():
    """Inspect migrations."""
    pass


@migrations.command()
def ordering():
    """
    Inspect the migrations ordering.

    The alembic migratins need to run in a clear specified
    ordering.
    Often we have the situation that we add migrations in one
    branch while the target branch moves on and have some more
    migrations added in the mean time so that the ordering
    of running the migrations at the end is no longer clearly
    specified (two or more with the very same down_migration).
    """
    path_to_this_file = pathlib.Path(__file__)
    path_to_this_dir = path_to_this_file.parent
    path_to_migrations = path_to_this_dir / "app" / "migrations" / "versions"

    migration_files = path_to_migrations.glob("*.py")

    revision_extractor = re.compile(r"(?:down_)?revision = ['\"]([a-zA-Z0-9]+)['\"]")

    down_revision_by_revision = {}
    for migration_file in migration_files:
        with migration_file.open() as infile:
            # Those files have entries for 'revision'
            # and 'down_revision' (what is the migration that must
            # run before the current one).
            revision = None
            down_revision = None
            for line in infile.readlines():
                if line.startswith("revision = "):
                    # We always have the revision entry
                    revision = revision_extractor.match(line).group(1)
                if line.startswith("down_revision = "):
                    match = revision_extractor.match(line)
                    # But it can be that we have no down revision
                    if match:
                        down_revision = match.group(1)
            down_revision_by_revision[revision] = down_revision
    # Convert it into a tree
    node_by_revision = {}
    for revision in down_revision_by_revision.keys():
        node_by_revision[revision] = Node(revision)
    root_nodes = []
    for revision, down_revision in down_revision_by_revision.items():
        revision_node = node_by_revision[revision]
        down_revision_node = node_by_revision.get(down_revision)
        if down_revision_node:
            down_revision_node.add_child(revision_node)
        else:
            root_nodes.append(revision_node)

    def traverse_tree(node, level):
        for child in node.children:
            next_level = level + 1
            yield child, next_level
            yield from traverse_tree(child, next_level)

    # Print it out & say if it is problematic or not.
    # We don't want to have migrations that have two childs
    # as alembic doesn't know in which order to execute them.
    for root_node in root_nodes:
        print(root_node.value)
        already_set_level = set()
        for child, level in traverse_tree(root_node, level=0):
            problematic = ""
            if level not in already_set_level:
                already_set_level.add(level)
            else:
                problematic = " problematic !"

            print(f"{level} {child.value} {problematic}")


@main.group()
def download():
    """Download data."""


@download.group()
def schemas():
    """Download schemas."""


@schemas.command()
def sensorml():
    """Download the sensorml schema & store it in a pickle file."""
    import pickle

    import xmlschema

    schema = xmlschema.XMLSchema(
        "https://schemas.opengis.net/sensorML/2.0/sensorML.xsd"
    )
    output_filename = "app/project/tests/api/helpers/sensorml_schema_validator.pickle"
    with open(output_filename, "wb") as outfile:
        pickle.dump(schema, outfile)


@download.command()
def organization_names():
    """Download the organzation names and store it in a json file."""
    # We use here that all of the organizations that are connected
    # to the helmholtz aai are either part of edugain or the dfn aai.
    #
    # But first we want to fetch content & we want to cache it locally.
    def cache_local(f):
        tmp = pathlib.Path("/tmp") / datetime.date.today().strftime("%Y%m%d")

        @functools.wraps(f)
        def wrapper(url):
            if not tmp.exists():
                tmp.mdir()

            base_name = pathlib.Path(url).name
            temp_file = tmp / base_name
            if temp_file.exists():
                return temp_file.open("rt").read()
            result = f(url)
            with temp_file.open("wt") as outfile:
                outfile.write(result)
            return result

        return wrapper

    @cache_local
    def fetch(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    # Now we can extract from our two files.
    organizations = {}
    urls = [
        "https://www.aai.dfn.de/metadata/dfn-aai-idp-metadata.xml",
        "https://www.aai.dfn.de/metadata/dfn-aai-edugain+idp-metadata.xml",
    ]
    for url in urls:
        xml_content = fetch(url)
        et = ElementTree.fromstring(xml_content)
        for entity_descriptor in et.findall(
            "{urn:oasis:names:tc:SAML:2.0:metadata}EntityDescriptor"
        ):
            idp_sso_descriptor = entity_descriptor.find(
                "{urn:oasis:names:tc:SAML:2.0:metadata}IDPSSODescriptor"
            )
            if idp_sso_descriptor is not None:
                extensions = idp_sso_descriptor.find(
                    "{urn:oasis:names:tc:SAML:2.0:metadata}Extensions"
                )
                if extensions is not None:
                    scope = extensions.find("{urn:mace:shibboleth:metadata:1.0}Scope")
                    if scope is not None:
                        if scope.attrib.get("regexp") not in [True, "true", "1"]:
                            scope_text = scope.text

                            organization = entity_descriptor.find(
                                "{urn:oasis:names:tc:SAML:2.0:metadata}Organization"
                            )
                            if organization is not None:
                                name_en = None
                                name_de = None
                                for display_name in organization.findall(
                                    "{urn:oasis:names:tc:SAML:2.0:metadata}OrganizationDisplayName"
                                ):
                                    lang = display_name.attrib.get(
                                        "{http://www.w3.org/XML/1998/namespace}lang"
                                    )
                                    if lang == "en":
                                        name_en = display_name.text
                                    elif lang == "de":
                                        name_de = display_name.text
                                name = name_en or name_de
                                organizations[scope_text] = name
                            # If we didn't got an display name by the organization,
                            # then we can still extract it from the ui_info of the extensions.
                            if not organizations.get(scope_text):
                                ui_info = extensions.find(
                                    "{urn:oasis:names:tc:SAML:metadata:ui}UIInfo"
                                )
                                display_names = ui_info.findall(
                                    "{urn:oasis:names:tc:SAML:metadata:ui}DisplayName"
                                )
                                name_en = None
                                name_de = None
                                for display_name in display_names:
                                    lang = display_name.attrib.get(
                                        "{http://www.w3.org/XML/1998/namespace}lang"
                                    )
                                    if lang == "en":
                                        name_en = display_name.text
                                    elif lang == "de":
                                        name_de = display_name.text
                                name = name_en or name_de
                                organizations[scope_text] = name

    for key in organizations:
        organizations[key] = organizations[key].encode("latin1").decode("utf8")

    output_file = (
        pathlib.Path(__file__).parent
        / "app"
        / "project"
        / "static"
        / "organization_names.json"
    )
    json.dump(
        organizations, output_file.open("wt", encoding="utf8"), indent=4, sort_keys=True
    )


if __name__ == "__main__":
    main()

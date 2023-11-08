# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Helper functions to work with configurations."""

import collections

TypeIdTuple = collections.namedtuple("TypeIdTuple", ["type", "id"])


def build_tree(platform_mounts, device_mounts, f_platform_mount, f_device_mount):
    """
    Build the tree of platforms & devices.

    It basically builds a tree like this:
    [
      {
        "element": PlatformMount(1),
        "children": [
          {
            "element": PlatformMount(2),
            "children": [
              {
                "element": DeviceMount(1),
                "children": [
                  {
                    "element": DeviceMount(2),
                    "children": []
                  }
                ]
              }
            ]
          }
        ]
      }
    ]

    while we can specify the keys next to "children" with the functions that
    we give into our procedure here (the example sets just the mount in an
    "element" entry in the result dict).
    With some more functions we can add more entries in the dict of the tree.

    Result at the end are the top level elements (all others are reachable via the
    children entries).
    """
    top_level_elements = []
    children = {}

    for platform_mount in platform_mounts:
        children.setdefault(TypeIdTuple("platform", platform_mount.platform_id), [])
        entries = f_platform_mount(platform_mount)
        element = {
            **entries,
            "children": children[TypeIdTuple("platform", platform_mount.platform_id)],
        }

        if platform_mount.parent_platform_id:
            children.setdefault(
                TypeIdTuple("platform", platform_mount.parent_platform_id), []
            )
            if (
                element
                not in children[
                    TypeIdTuple("platform", platform_mount.parent_platform_id)
                ]
            ):
                children[
                    TypeIdTuple("platform", platform_mount.parent_platform_id)
                ].append(element)
        else:
            if element not in top_level_elements:
                top_level_elements.append(element)

    for device_mount in device_mounts:
        children.setdefault(TypeIdTuple("device", device_mount.device_id), [])
        entries = f_device_mount(device_mount)
        element = {
            **entries,
            "children": children[TypeIdTuple("device", device_mount.device_id)],
        }

        if device_mount.parent_platform_id:
            children.setdefault(
                TypeIdTuple("platform", device_mount.parent_platform_id), []
            )
            if (
                element
                not in children[
                    TypeIdTuple("platform", device_mount.parent_platform_id)
                ]
            ):
                children[
                    TypeIdTuple("platform", device_mount.parent_platform_id)
                ].append(element)
        elif device_mount.parent_device_id:
            children.setdefault(
                TypeIdTuple("device", device_mount.parent_device_id), []
            )
            if (
                element
                not in children[TypeIdTuple("device", device_mount.parent_device_id)]
            ):
                children[TypeIdTuple("device", device_mount.parent_device_id)].append(
                    element
                )
        else:
            if element not in top_level_elements:
                top_level_elements.append(element)

    return top_level_elements

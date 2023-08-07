<!--
SPDX-FileCopyrightText: 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: HEESIL-1.0
-->

## 1.4.0 (Unreleased)

Added:
- parameters for devices, platforms & configurations
- attachments for sites
- b2inst support for PIDs
- FZJ logo
- sensorML for sites
- pagination for device & platform search in mount wizzard

Changed:
- map to display sites: Only polygon instead of map markers

Fixes:
- improved file upload for mimetypes with encodings
- less 406 responses when opening backend urls with the browser
- better handling of url parameters for search pages
- switch to gitlab API to create issues after submitting new suggestions for CV entries
- ignore ids of users in the full text search
- improved display of very long links
- fixed filter for contact names in mount wizzard
- form to edit site assignment of configurations
- increased page sizes for some list queries



## 1.3.0 - 2023-07-06

Added:
- license & aggregation period for tsm linkings

Fixes:
- improved full text search with smaller search texts
- removed entries with `updated_at=null` from recent activities
- renamed sites to sites & labs

## 1.2.1 - 2023-07-03

Fixes:
- organization names with special characters
- better status codes when deleting datastreams or device properties

## 1.2.0 - 2023-06-28

Added:
- tsm linkings
- new wizzard for dynamic location actions

## 1.1.0 - 2023-06-26

Added:
- orcids & organizations for contacts
- labels for location actions
- description, project and PID for configurations
- aggregation types for device properties

Fixed:
- improved search by contact names
- more restrictive handling of device properties
- extended sensorML export
- updated large parts of openAPI docs


## 1.0.0 - 2022-12-15

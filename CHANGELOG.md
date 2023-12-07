<!--
SPDX-FileCopyrightText: 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: HEESIL-1.0
-->
## 1.9.0 (Unreleased)

Added:
- option to create site hierarchies
- PID links in search results
- support for searches with asterisk

Changed:
- change occurrencies of `TSM-Linking(s)` in the UI to `TSM Linking(s)`
- (UFZ): changed to SMS-IDL to use Hifis VO (and subgroups) and allowed syncing of these groups
- (UFZ): Switched link for UFZ group management to Hifis VOs
- adjust default icons for expandable text

Fixed:
- improved display of very long email addresses
- search for site selection of configurations doesn't use preset filters
  from the extended site search anymore
- Links into the GFZ website


## 1.8.1 - 2023-11-28

Fixed:
- No redirect for location pages of public configurations if the user is not logged in

## 1.8.0 - 2023-11-28

Added:
- links from profile page to contact page
- Keywords
- field to set the country of origin for devices & platforms to support export control
- checks to ensure that no duplicated contact role entries can be added
- Tab to show the locations of all the configurations for a site
- Pagination for device selection for tsm linkings

Changed:
- Devices can now also be mounted on other devices
- Increased number of workers for gunicorn
- Included material design icons for styleguidist in frontend to avoid calling external ressources 

Fixed:
- information about selected item in configuration tree sticks while scrolling

## 1.7.0 - 2023-11-06

Added:
- extended display of definitions from the CV for contact roles,
  device types, manufacturers and platform types
- more usage statistic values (pids, uploads, ...)
- Activated B2INST support on UFZ instance (stage/production)

Changed:
- the ordering of the platforms & devices on the mounting-actions endpoint is now by short name
- Combine entries for different roles of the same person when showing the contacts of
  devices/platforms/configurations/sites.
- updated privacy policy for B2INST usage on UFZ

## 1.6.0 - 2023-10-24

Added:
- description fields for device properties, attachments & custom fields
- autocompletion for attachment labels
- automatic selection of measured quantities and parameters for action data if there is only one
  element to select
- QR Code functionality
- button to use the set the current location for static locations of configurations
- Activated B2INST support on GFZ instance (production)

Changed:
- removed the strong linkage of site usage and site type so that we can
  set any combination of both
- ufz changed cv url for frontend stage image 
- use service desk of the orchestration repo instead of the separate service desk repo

## 1.5.1 - 2023-10-04

Fixed:
- default count for sites on landing page

## 1.5.0 - 2023-10-04

Added:
- Activated B2INST support on GFZ instance (staging)
- description on landing page for sites & labs
- sites and labs added to latest activity log
- preview of the resulting configuration tree in the submit stage of the mount wizzard

Changed:
- updated privacy policy for B2INST usage on GFZ
- extended user deprovising script to remove user data from B2INST
- updated schema used for b2inst
- Update to psycopg3 for the CV. Please check all `SQL_ENGINE` env variables.
- switch to a central CV instance (https://sms-cv.helmholtz.cloud)

Fixes:
- problem resolved that mask for device creation stays open when creating a PID failed
- improved wording for hint if a platform can't be unmounted due to still mounted child devices/platforms


## 1.4.0 - 2023-08-24

Added:
- parameters for devices, platforms & configurations
- attachments for sites
- b2inst support for PIDs
- FZJ logo and group page
- sensorML for sites
- pagination for device & platform search in mount wizzard
- filter for action pages

Changed:
- map to display sites: Only polygon instead of map markers
- changed layout of action cards
- store for loading spinner

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
- resolved warnings for SQLAlchemy Backrefs
- better handling for delete dialogs on long running requests



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

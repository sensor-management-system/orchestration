<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->

## 1.24.3 (Unreleased)

Changed:
- improvements when creating new data linkings ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/547))

Fixed:
- it is now possible to copy internal devices to be private devices if the user wasn't the creator of the original device ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/637))
- Allow release notes to be empty in newly created version sections in changelog ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/561))

## 1.24.2 - 2026-01-22

Changed:
- use gfz.de domain for the handle server ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/634))

Fixed:
- QR code generator now includes base paths ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/628))


## 1.24.1 - 2026-01-20

Added:
- Option to allow or ignore entitlements for permission management ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/632))

Fixed:
- made the permission group membership test more robust ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/631))

## 1.24.0 - 2026-01-19

Changed:
- permission group handling is now fully integrated into the SMS backend ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/604))
- combine the permissions for group members and group administrators ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/604))
- Extended the warning when deleting mount actions ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/624))

## 1.23.3 - 2026-01-12

Changed:
- Added gfz and sandbox endpoints for the sms device csv importer ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/609))
- Update KIT TSM endpoints via docker-compose configs ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/613))
- Updated the legal notice page for GFZ with new section head and new administrative director ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/614))
- Updated the legal notice page for UFZ ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/615))
- Improved usability an robustness of csv importer ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/617))
- Fixed typos in URLs of the import profiles in the csv importer ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/620))

Fixed:
- Removed the dual use field in the csv importer for devices as it was moved in a different model ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/610))
- Fixed handling of complex links for software update action repository urls ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/619))
- Removed non null constraint for manufacturer names ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/621))
- Explicit conversion of serial number and inventory number to strings ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/618))

## 1.23.2 - 2025-11-17

Changed:
- Updated GFZ name for the zenodo publication ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/600))
- IDL component now supports fetching the entitlements ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/602))
- ordering of the measured quantities is kept when copying devices ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/605))
- Updated the login process for the FZJ staging instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/606))

Fixed:
- Show release notes now works with generic frontend image ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/603))
- The privacy policy page bugs have been fixed for the FZJ instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/607))

## 1.23.1 - 2025-10-23

Added:
- The resource capability for group management has been enabled to the FZJ prod instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/587))
- The FZJ dev instance has been implemented and deployed with Gitlab CI/CD workflow ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/591))
- exportcontrol.gfz.de redirects now to the SMS GFZ instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/598))

Changed:
- Switched from labeling the usage of sites to land use ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/582))
- Update KIT deployment data management contact email ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/595))

Fixed:
- Call the sync with hifis groups for the idl no matter which institue ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/589))
- In FZJ staging instance, the OIDC well known URL, Client ID and VO/RC conventions have been fixed for group management ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/590))
- Added missing final nginx:alpine webserver stage in Dockerfile for FZJ dev build. ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/593))
- Fixed Docker Compose service names and container ports for the FZJ dev instance. ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/594))
- Fixed Nginx routes Minio within the ibg3dev environment for the FZJ dev instance. ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/597))

## 1.23.0 - 2025-09-15

Added:
- Management command to update the urls of the registered handles for sites ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/586))

Changed:
- The latest version of docker compose file has been updated for the FZJ staging deployment ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/569))
- The new front-end URL has been updated for FZJ staging instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/583))
- Moved the main url for the GFZ instance to sensors.gfz.de ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/585))

## 1.22.0 - 2025-08-26

Added:
- Support for resource capabilities for group management ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/580))

Changed:
- KIT deployment, web server: bump nginx to 1.29 on alpine ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/578))

Fixed:
- the usage-statistics endpoint now works accepts `True` as truish value ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/579))
- Missing frontend implementation for visibility restrictions ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/556))

## 1.21.2 - 2025-08-20

Added:
- Option to show maintenance information without a redeployment ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/568))
- Display of mount ids in the confiugration page ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/573))

Changed:
- KIT deployment, frontend: bump node runtime to 22.17 on bookworm-slim base image, add IAI tsmdl endpoint ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/566))
- KIT deployment, backend: bump base image to slim-bookworm ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/566))
- Privacy Policy for FZJ instance has been updated with revised contents ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/557))
- Configurations, reuse: rename button "Copy Mounts" to "Import Mounts" ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/574))

Fixed:
- Release notes are shown for the FZJ productive instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/564))
- Fixed a problem on patching mount actions without any attributes ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/572))
- Allow to unset end contacts for mount actions ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/576))

## 1.21.1 - 2025-07-14

Changed:
- Switch to sensors-sandbox.gfz.de for the SMS test user test system ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/562))
- Updated debian base images ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/563))

## 1.21.0 - 2025-07-07

Added:
- Show Release Notes (Changelog) on landing page ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/528))

Changed:
- Device detail page now shows the extended name instead of the short name in the app bar ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/542))
- improvements in table to view data linkings of a configuration ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/515))

Fixed:
- KIT deployment, docker-compose: make `SMS_FRONTEND_URL` env variable available to frontend container so that data linking works correctly ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/552))
- PID generation while the description is still None ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/555))
- Removed shared state between the input forms to mount devices and platforms ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/558))

## 1.20.0 - 2025-03-31

Added:
- Labels for datastream links ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/543))

Fixed:
- Loading of favicon for a default base url ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/538))
- Zenodo publication now only contains the very latest version as zipped source code ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/539))

Changed:
- Made several cosmetic improvements to UI of Mount wizard components ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/480))
- Old swagger endpoints are removed, openapi endpoints should be used instead ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/541))

## 1.19.0 - 2025-03-17

Added:
- Possibility to copy an existing mount setup (complete or partially) from any configuration and update the mount details ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/443))
- Public SMS instance URL of FZJ is added in the README file ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/529))

Fixed:
- Typos on frontend landing page were fixed ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/527))
- Fixed a CORS issue when using the GFZ tsmdl ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/534))
- Being unable to edit mount dates was fixed ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/532))

Changed:
- Updated elasticsearch to version 7.17.28 ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/533))

## 1.18.4 - 2025-03-03

Changed:
- MQTT will only be used if broker url, username and password are configured ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/519))

## 1.18.3 - 2025-02-25

Added:
- button to easily set the begin and end date of a mount to the begin and end dates of the corresponding configuration ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/478))

Fixed:
- Reference for mq image in sms sandbox release ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/514))

## 1.18.2 - 2025-02-25

Fixed:
- Volume name for the MQTT containers in the sms sandbox release ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/513))

## 1.18.1 - 2025-02-25

Fixed:
- tag names for the sms sandbox release for MQTT initialization containers ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/511))

## 1.18.0 - 2025-02-25

Added:
- Fuzzy matching mechanism to help with reducting cv suggestions for already existing cv entries ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/428))
- MQTT interface to receive updates from the SMS ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/295))  

Fixed:
- problem on validation of mount contact when mounting devices or platforms ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/490))
- corrected string when a device or platform is not available for mounting ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/495))  
- corrected error message and removed duplicated loading of platform attachments([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/498))
- Prod path updated for FZJ prod nginx image ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/503))
- when unmounting offsets got overriden ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/502))  

Changed:
- mechanism to find the contact of the current user uses now the contact id of the user info object ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/491))
- updated default organization name for GFZ users ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/492))
- Removed usage of pytz ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/496))
- Removed deprecated code for creating old ufz frontend image ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/487))
- Action names defined in the SMS follow the same structure as for the CV with only one upper case letter ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/501))
- Update to docker 27.5.1 for the builds in the CI pipeline ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/505))

## 1.17.2 - 2025-01-28

Added:
- Footer section pages (Legal notice, Privacy policy and Terms of use) for FZJ prod instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/455))
- Devices and platforms can now be unmounted recursively, including proper validation of nodes serving as future parent nodes ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/440))
- Buttons for linked Datasources/Things/Datastreams navigating to their respective resources within an STA instance ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/381))

Fixed:
- Time amount for adding/updating mount actions was reduced by updating less entries
  in the elastic search ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/479))

Changed:
- MinIO GFZ backup goes now into the central s3 storage ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/482))
- Usage of the new GFZ name & logo ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/484))
## 1.17.1 - 2024-12-02

Fixed:
- Base url parameter on GFZ systems ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/470))

## 1.17.0 - 2024-12-02
Added:
- new generic frontend image, can be used to set the environment variables during runtime ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/441))  
- UX improvements (winter only) ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/469))

Fixed:
- Problem with truncated items in navigation drawer ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/465))

Changed:
- detached footer on landing page, navigation drawer and footer sharing screen width ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/465))

## 1.16.3 - 2024-11-28

Added:
- common form component for attachments ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/439))
- fullscreen image preview and delimiters on image overview ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/431))
- hint for wiki on landing page ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/453))

Fixed:
- Problem on non refreshing messages if a device or platform is not available to be mounted ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/451))
- Problem that links without http or https prefix are not linked correctly ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/452))

## 1.16.2 - 2024-10-23

Added:
- improved filter options for get list endpoint of datastream links
- page to show basic information about one datastream link
- automatic creation of versions for zenodo publication
- frontend shows ids of measured quantities
- frontend can now open and focus on a selected measured quantities by a given url
- page to lookup the by the measured quantity id
- more labels and notes on suggestion dialog for new manufacturers
- "sites&labs" page has a map which shows listed sites and a button to show a specific listed site on the map
- possibility to automatically render a created image attachment on the Basic data page
- devices that are involved in the measurement (loggers, multiplexers) can now be added to the datastream link
- Include provenance term and ucum case sensitive symbol for cv units

Fixed:
- loaddata command is now more robust according to files with just a new line
- startup for M2 Mac OS with docker desktop was improved
- typo in validation message when setting the unmount date for a parent platform
- don't try to check platform mounts for usage in dynamic location actions

Changed:
- Cleanup of unused docker images on GFZ servers is now done via `docker image prune`
- Usage of the absolute url to checkout the git submodule for the CV
- Improved style of items in device select of a data linking
- Adjusted the executative directors entries in the GFZ legal notice page

## 1.16.1 - 2024-08-06

Fixed:
- favicon can now be loaded for sms instances, which don't run under root path

## 1.16.0 - 2024-08-01

Added:
- added possibility to edit location actions from the actions tab of a configuration
- visibility markers for export control information (public or export control only)
- created at field for the manufacturer models in order to keep track when those were added to the system
- extended openapi specs
- multiple wildcard idl conventions are now supported
- Scripts to update cv related names from the latest entries in the controlled vocabulary
  as well as code to analyse for which entries we still miss to have links to CV
- add more links from the frontend to the CV entries
- show info if an image (URL attachment) is no longer available
- heatmap of days and activity within the system
- PIDs for sites
- integrated sms logos
- labels for the mounts
- display scale on maps
- added validation to numeric fields of device measured quantities
- added a dragger at the bottom of maps to adjust the size of maps
- loaddata command can update fields based on some unique criteria

Changed:
- dialog to suggest new manfacturer entries now mentions RORs for the provenance url
- the licenes of the system is now the EUPL-1.2
- Renamed tsm linking to data linking
- Related units are now suggested, but all units are selectable for measured quantities
- Harmonized field-titles "Begin description" & "End description" of the mount information
- Improved the validation performance of the "mount information step" when mounting a platform/device on a configuration ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/389)) 
- improved messages for cases that mount edits can't be done
- Revised README.md and moved institute-specific information to separate directory

Fixed:
- SensorML validation for unit name values that contain whitespaces
- Fixed https://codebase.helmholtz.cloud/hub-terra/sms/service-desk/-/issues/89
- The "Open in new tab" of a device or platform in the mounting wizard (step 3) of a configuration now opens the correct URL (also when creating a new tsm linking)
- Fixed a problem when inserting small values like 0.05 (stating with 0.0) in some of the number fields
- Added CSRF trusted origins for the IDL component
- Updated IDL image, so that github accounts can be used again
- Fixes a bug in the management of manufacturer model entries
- Fixed bug when deleting contact in mount wizard step 4 "Add mount information" ([Merge Request](https://codebase.helmholtz.cloud/hub-terra/sms/orchestration/-/merge_requests/391))
- Bug on validating time span ranges on device mounts with child mounts

## 1.15.1 - 2024-04-24

Changed:
- computed offsets are now round on micrometer scale to avoid showing odd values due to floating point arithmetic

Fixed:
- updated the UFZ group info page for the switch to Hifis VO

## 1.15.0 - 2024-04-15

Changed:
- (UFZ): changed to SMS-IDL to use Hifis VO (and subgroups) and allowed syncing of these groups

## 1.14.0 - 2024-04-08

Added:
- Images are also previewed in edit mode on mobile devices
- Setup for SMS sandbox deployment on https://sensors-sandbox.gfz-potsdam.de
- (GFZ): GFZ IDL Version 0.4 will be used
- Autocompletion for keywords
- Export control workflow support
- Organization and search by manufacturer and model
- Extended sarch option for own configurations
- SensorML for devices and platforms now contain a gml:name attribute
- Campaign field for configurations

Changed:
- The SMS now sends values for missing information according to the datacite values for unknown information
- Owner information for B2inst are now the institutions
- Re-added the inventory number for the B2inst export

Fixed:
- Improve/Enable the correct rearranging of images
- Images are shown via a proxy, so that we can show images on servers with more CORS restrictions
- Fixed loading of image urls after saving configurations
- Fixed some typos on the tsm linking wizzard


## 1.13.0 - 2024-02-29

Added:
- Image attachments of devices, platforms, configurations and sites can now be selected as rendered preview images on the `Basic Data` tab
- Mount actions listed in the 'actions' tab of a configuration now have the "edit" option, which redirect to the edit form of that mount action   
- Mounts can have explicit coordinates
- Shortcut to add a value for a parameter of device, platform or configuration 
- Endpoint URL is displayed in the tsm linking form when selecting a endpoint
- Tooltip to explain why a parameter can not be deleted if the delete button is disabled
- Shortcut to edit or delete a value of a parameter of device, platform or configuration
- Locations of configurations in sensorML
- Autocompletion for device & platform model fields

Changed:
- Parameters of device, platform or configuration are now sorted alphabetically

Fixed:
- Adjusted the ordering of the elements in sensorML 
- Stop showing the back to search button when opening the search page manually
- After editing the name of a parameter of device, platform or configuration the updated name will also be displayed in the parameter value table for a selected date


## 1.12.0 - 2024-01-17

Added:
- Buttons to return to search pages

Changed:
- Tree with hierarchy of platforms and devices on a configuration now
  shows the device & platform types instead of generic "Device" and "Platform"
  texts


Fixed:
- The lower button "Add Attachment" in Platform Attachment now works. 
- Improved id filters for json:api relationships

## 1.11.0 - 2023-12-14

Changed:
- (UFZ): reverted changes to use the Hifis VO back to old service

## 1.10.0 - 2023-12-14

Added:
- Updated the content of legal notice, privacy policy and terms of use within the footer pages for a FZJ instance's demo version.
- show version numbers based on git tags
- Unit for accuracy
- sites locations tab shows sub sites
- Add hint for the selected date at `Platforms and Devices` tab of configuration
- manage.py commands to update b2inst records

Changed:
- improved sort logic for mounts and unmounts that have the very same date
- inventory numbers are removed from B2inst export

Fixed:
- Improved handling of missing values for sites

## 1.9.0 - 2023-12-07

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

Fixed:
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

Fixed:
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

Fixed:
- improved full text search with smaller search texts
- removed entries with `updated_at=null` from recent activities
- renamed sites to sites & labs

## 1.2.1 - 2023-07-03

Fixed:
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

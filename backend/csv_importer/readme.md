<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
# CSV importer

With the csv importer it is possible to import many devices in
a fast way into the SMS instances.

## Requirements

### Software
You need to have the following tools/libs installed:

- python 3
- pandas
- requests

### SMS

You need an api key to run the script.


## Usage


```python
>>> from csv_importer import SMSDeviceImporter
>>> SMSDeviceImporter(
        filepath="~/data/somewhere/former_devices_export.csv",
        run_type="local",
        api_key="ABC1234"
    ).process()
```

## Limitations

There are some limitations that you should be aware about:

- Currently it only supports UFZ SMS instances (staging, prod, as well as lcocal development instance)

- there is only support for device related objects up to 99 elements for each device for:
  - device properties,
  - contacts`*`,
  - attachments,
  - customfields each

- it will only import:
  - devices
  - contacts`*`,
  - device contact roles*
  - attachments
  - customfields

- the file format must be identifical to the one of the [example file](./ufz_sample_file.csv).
- the importer is currently fixed to `cp1252` encoding
- the importer will not import PIDs

Please note: `*` The import for contact roles is currently broken.


## Run types

The following run types are supproted:

| Run type | Explanation |
|----------|---------|
| local | A system that runs locally on the developers computer. |
| stage | A test system that is only accessible locally at UFZ. |
| sandbox | The public test system for the users. |
| ufz | The production instance at UFZ. |
| gfz | The production instance at GFZ. |
| kit | The production instance at KIT. |

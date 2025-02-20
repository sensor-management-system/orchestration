<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Script to display some messages from MQTT

This script is for testing purposes for the interaction with the mqtt message queue.

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then it should be possible to start it with

```
python3 main.py
```

It should work out-of-the-box with the default configuration.
However, if you changed some of the settings, make sure that you also
adjust the variables in this script.

## Configuration

Check the docker-compose.yml in the main folder of the project.

The following variables / sections correspont to the entries you need to use:

| main.py variable | docker-compose.yml                                                                                        |
|------------------|-----------------------------------------------------------------------------------------------------------|
| broker           | Should be localhost if the script runs independtly from the docker-compose. Otherwise it should be `mq`. |
| port             | `services.mq.ports[0]`                                                                                      |
| username         | `services.mq_init.environment.MQTT_BACKEND_USER`                                                            |
| password         | `services.mq_init.environment.MQTT_BACKEND_PASSWORD`                                                        |

## Topics

The script so far only displays messages that are related to device changes.

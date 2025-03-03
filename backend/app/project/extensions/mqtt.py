# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Classes for the mqtt handling."""

from flask import current_app


class LazyMqttInitWrapper:
    """
    A wrapper around flask_mqtt.Mqtt.

    This is here to make the initialization lazy,
    so that we run the init when we run our first publish
    of an event.

    We can do that as this extension is for publishing
    only. If we would need to listen, we would need the
    initialization way earlier...
    """

    def __init__(self, mqtt):
        """Wrap the mqtt object."""
        self.mqtt = mqtt

    def init_app(self, app):
        """Don't run any code."""
        pass

    def _enforce_initialization(self, app):
        """Enforce that we run the initialization & have a connection."""
        if not self.mqtt.connected:
            self.mqtt.init_app(current_app)

    def publish(self, *args, **kwargs):
        """
        Publish an event on mqtt.

        Runs the initialization if needed.
        """
        if self._mqtt_config(current_app):
            self._enforce_initialization(current_app)
            return self.mqtt.publish(*args, **kwargs)

    def _mqtt_config(self, app):
        config = app.config
        fields_that_must_be_set = ["MQTT_BROKER_URL", "MQTT_USERNAME", "MQTT_PASSWORD"]
        return all([config[f] for f in fields_that_must_be_set])

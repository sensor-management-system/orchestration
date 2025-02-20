#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Script to query the mqtt server."""
# See https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# for an example (used here to write this code).

import time

from paho.mqtt import client as mqtt_client


def connect_mqtt(broker, port, username, password):
    """Connect to the broker with a persistent session."""

    def on_connect(client, userdata, flags, rc):
        """Handle the event that we are connected to the server."""
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = "example-fetch"
    client = mqtt_client.Client(client_id=client_id, clean_session=False)
    client.username_pw_set(username=username, password=password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client, topics):
    """Subscribe to the given topics with a persistent session."""

    def on_message(client, userdata, msg):
        """Handle the event that we get a message."""
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    for topic in topics:
        client.subscribe(topic, 1)
    client.on_message = on_message


def main():
    """Connect to the broker and show the messages on the console."""
    broker = "localhost"
    port = 8883
    topics = ["sms/patch-device", "sms/post-device", "sms/delete-device"]
    username = "sms_backend_user"
    password = "changeme"

    client = connect_mqtt(broker, port, username, password)
    subscribe(client, topics)
    client.loop_start()
    try:
        while True:
            time.sleep(1)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()

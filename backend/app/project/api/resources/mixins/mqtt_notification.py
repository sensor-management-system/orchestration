# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Mixin class for the resources that allows to send informations out via mqtt."""
import json

from project.extensions.instances import mqtt


def dasherize(name_with_underscores):
    """
    Help to transform snake_case into kebab-case.

    >>> dasherize("device_attachment")
    "device-attachment"
    >>> dasherize("device")
    "device"
    """
    return name_with_underscores.replace("_", "-")


class MqttNotificationMixin:
    """
    Class to be mixed in into resource classes.

    Will send messages out via mqtt.
    """

    def post(self, *args, **kwargs):
        """Run the post request and send the result to mqtt."""
        result = super().post(*args, **kwargs)

        for topic in self._notification_post_topics():
            # We send only the first data entry out.
            # Part of the issue here is that the post endpoint belongs
            # to a list resource.
            # Those uses the schema with many=True - to use them
            # to serialize a list of entities.
            # However, after the post we only return one single instance.
            mqtt.publish(topic, json.dumps(result[0]), 2)

        return result

    def patch(self, *args, **kwargs):
        """Run the patch request and send the result to mqtt."""
        result = super().patch(*args, **kwargs)

        for topic in self._notification_patch_topics():
            mqtt.publish(topic, json.dumps(result), 2)

        return result

    def delete(self, *args, **kwargs):
        """Run the delete requests and send an info to mqtt."""
        result = super().delete(*args, **kwargs)
        id_ = kwargs["id"]

        type_ = self.schema.Meta.type_
        for topic in self._notification_delete_topics():
            mqtt.publish(
                topic,
                json.dumps(
                    {
                        # We create a similar payload here, as we have
                        # for the others.
                        "data": {"type": type_, "id": str(id_)}
                    }
                ),
                2,
            )

        return result

    # There are different strategies for the topics.
    # One is to have seperate post, patch & delete topics
    # for every entity.
    #
    # Those would look like this:
    # - sms/post-device
    # - sms/patch-device
    # - sms/delete-device
    # - sms/post-device-property
    # - sms/patch-device-property
    # - sms/delete-device-property
    # ...
    #
    # This approach creates a lot of topics, but it will allow the clients
    # to handle all the different cases individually without a lot of
    # extra code to check what exactly happens. And the clients will need
    # to react differently on creating (posting) a device and modifying
    # (patching) a device property anyway.
    # The only challange here is to keep track of the topics as the data model
    # of the SMS gets larger and larger.
    #
    # However the clients need to know anyway what they are interested in.
    # (But if we really want we can add more - generic - topics too.

    def _notification_post_topics(self):
        """Generate a list of topics to send to after post requests."""
        type_ = self.schema.Meta.type_
        topic = f"sms/post-{dasherize(type_)}"
        yield topic

    def _notification_patch_topics(self):
        """Generate a list of topics to send to after patch requests."""
        type_ = self.schema.Meta.type_
        topic = f"sms/patch-{dasherize(type_)}"
        yield topic

    def _notification_delete_topics(self):
        """Generate a list of topics to send to after delete requests."""
        type_ = self.schema.Meta.type_
        topic = f"sms/delete-{dasherize(type_)}"
        yield topic

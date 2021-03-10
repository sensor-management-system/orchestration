import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_software_update_actions_attachment_model import (
    add_device_software_update_action_attachment,
)


class TestDeviceSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateActionAttachment endpoints."""

    device_software_update_action_attachment_url = (
        base_url + "/device-software-update-action-attachments"
    )
    object_type = "device_software_update_action_attachment"

    def test_get_device_software_update_action_attachment(self):
        """Ensure the GET /device_software_update_action_attachment route reachable."""
        response = self.client.get(self.device_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_attachment_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateActionAttachment objects"""
        _ = add_device_software_update_action_attachment()
        with self.client:
            response = self.client.get(
                self.device_software_update_action_attachment_url
            )
        _ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_device_software_update_action_attachment(self):
        """TEST Create DeviceSoftwareUpdateActionAttachment"""
        # d = Device(short_name="Device 277")
        # jwt1 = generate_token_data()
        # c = Contact(
        #     given_name=jwt1["given_name"],
        #     family_name=jwt1["family_name"],
        #     email=jwt1["email"],
        # )
        # db.session.add(d)
        # db.session.commit()
        # a = DeviceAttachment(label=fake.pystr(), url=fake.url(), device_id=d.id)
        # dsu = DeviceSoftwareUpdateAction(
        #     device=d,
        #     software_type_name=fake.pystr(),
        #     software_type_uri=fake.uri(),
        #     update_date=fake.date(),
        #     version="0.5455",
        #     repository_url=fake.url(),
        #     description=fake.paragraph(nb_sentences=3),
        #     contact=c,
        # )
        # db.session.add_all([d, a, c, dsu])
        # db.session.commit()
        # data = {
        #     "data": {
        #         "type": self.object_type,
        #         "attributes": {},
        #         "relationships": {
        #             "action": {"data": {"type": "action", "id": dsu.id}},
        #             "attachment": {"data": {"type": "attachment", "id": a.id}}, },
        #     }
        # }
        # _ = super().add_object(
        #     url=f"{self.device_software_update_action_attachment_url}?include=action,attachment",
        #     data_object=data,
        #     object_type=self.object_type,
        # )

    def test_update_device_software_update_action_attachment(self):
        """TEST Update DeviceSoftwareUpdateActionAttachment"""

    def test_delete_device_software_update_action_attachment(self):
        """TEST Delete DeviceSoftwareUpdateActionAttachment"""
        dsu = add_device_software_update_action_attachment()
        _ = super().delete_object(
            url=f"{self.device_software_update_action_attachment_url}/{dsu.id}",
        )

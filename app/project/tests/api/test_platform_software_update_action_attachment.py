from project import base_url
from project.api.models import (
    Contact,
    Platform,
    PlatformAttachment,
    PlatformSoftwareUpdateAction,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_software_update_actions_attachment_model import (
    add_platform_software_update_action_attachment_model,
)


class TestPlatformSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateActionAttachment endpoints."""

    platform_software_update_action_attachment_url = (
        base_url + "/platform-software-update-action-attachments"
    )
    object_type = "platform_software_update_action_attachment"

    def test_get_platform_software_update_action_attachment(self):
        """Ensure the GET /platform_software_update_action_attachments route reachable."""
        response = self.client.get(self.platform_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_attachment_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateActionAttachment objects"""
        _ = add_platform_software_update_action_attachment_model()
        with self.client:
            response = self.client.get(
                self.platform_software_update_action_attachment_url
            )
        self.assertEqual(response.status_code, 200)

    def test_post_platform_software_update_action_attachment(self):
        """Create PlatformSoftwareUpdateActionAttachment"""
        p = Platform(short_name="Platform 144")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        db.session.add(p)
        db.session.commit()
        a = PlatformAttachment(label=fake.pystr(), url=fake.url(), platform_id=p.id)
        psu = PlatformSoftwareUpdateAction(
            platform=p,
            software_type_name=fake.pystr(),
            software_type_uri=fake.uri(),
            update_date=fake.date(),
            version="0.54",
            repository_url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            contact=c,
        )
        db.session.add_all([p, a, c, psu])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "platform_software_update_action",
                            "id": psu.id,
                        }
                    },
                    "attachment": {"data": {"type": "platform_attachment", "id": a.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.platform_software_update_action_attachment_url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_platform_software_update_action_attachment(self):
        """Update PlatformSoftwareUpdateActionAttachment"""
        old = add_platform_software_update_action_attachment_model()
        p = Platform(short_name="Platform new 144")
        db.session.add(p)
        db.session.commit()
        a = PlatformAttachment(label=fake.pystr(), url=fake.url(), platform_id=p.id)
        db.session.add(a)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": old.id,
                "attributes": {},
                "relationships": {
                    "attachment": {"data": {"type": "platform_attachment", "id": a.id}},
                },
            }
        }
        _ = super().update_object(
            url=f"{self.platform_software_update_action_attachment_url}/{old.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_platform_software_update_action_attachment(self):
        """Delete PlatformSoftwareUpdateActionAttachment """
        psu_a = add_platform_software_update_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.platform_software_update_action_attachment_url}/{psu_a.id}",
        )

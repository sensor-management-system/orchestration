# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permission group model."""

from project.api.models import PermissionGroup
from project.tests.base import BaseTestCase


class TestPermissionGroup(BaseTestCase):
    """Test class for the permission group model."""

    def test_convert_entitlement_to_name(self):
        """Ensure we can create a shorter name for the entitlement."""
        test_cases = [
            (
                "urn:geant:helmholtz.de:gfz:group:cegit#idp.gfz-potsdam.de",
                "cegit",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:demo.gfz-sms-admin#idp.gfz-potsdam.de",
                "demo.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:department5.gfz-sms-admin#idp.gfz-potsdam.de",
                "department5.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:department5.gfz-sms-member#idp.gfz-potsdam.de",
                "department5.gfz-sms-member",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:eqexplorer-shakemap-configuration#idp.gfz-potsdam.de",
                "eqexplorer-shakemap-configuration",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:hydro.gfz-sms-admin#idp.gfz-potsdam.de",
                "hydro.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:ig.gfz-sms-admin#idp.gfz-potsdam.de",
                "ig.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:mefe.gfz-sms-admin#idp.gfz-potsdam.de",
                "mefe.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:sec52.gfz-sms-admin#idp.gfz-potsdam.de",
                "sec52.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:sensor-management-system-export-control#idp.gfz-potsdam.de",
                "sensor-management-system-export-control",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:sf.gfz-sms-admin#idp.gfz-potsdam.de",
                "sf.gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:gfz:group:telegrafenwald#idp.gfz-potsdam.de",
                "telegrafenwald",
            ),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement:imk-aaf:gfz-sms-member#login.helmholtz.de",
                "KIT_SensorManagement:imk-aaf:gfz-sms-member",
            ),
            (
                "urn:geant:helmholtz.de:group:Helmholtz-member#login.helmholtz.de",
                "Helmholtz-member",
            ),
            ("urn:geant:helmholtz.de:group:UFZ-TSM#login.helmholtz.de", "UFZ-TSM"),
            (
                "urn:geant:helmholtz.de:group:Moses:Team-DM#login.helmholtz.de",
                "Moses:Team-DM",
            ),
            (
                "urn:geant:helmholtz.de:group:WETSCAPES2.0:SMS:gfz-sms-admin#login.helmholtz.de",
                "WETSCAPES2.0:SMS:gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:group:Moses:Heat-Drought#login.helmholtz.de",
                "Moses:Heat-Drought",
            ),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement:imk-aaf:gfz-sms-admin#login.helmholtz.de",
                "KIT_SensorManagement:imk-aaf:gfz-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:group:Helmholtz-all#login.helmholtz.de",
                "Helmholtz-all",
            ),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement:imk-aaf:kit-sms-member#login.helmholtz.de",
                "KIT_SensorManagement:imk-aaf:kit-sms-member",
            ),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement:imk-aaf#login.helmholtz.de",
                "KIT_SensorManagement:imk-aaf",
            ),
            ("urn:geant:helmholtz.de:group:GFZ#login.helmholtz.de", "GFZ"),
            (
                "urn:geant:helmholtz.de:group:Moses:Permafrost#login.helmholtz.de",
                "Moses:Permafrost",
            ),
            (
                "urn:geant:helmholtz.de:group:WETSCAPES2.0#login.helmholtz.de",
                "WETSCAPES2.0",
            ),
            (
                "urn:geant:helmholtz.de:group:UFZ-TSM:First project#login.helmholtz.de",
                "UFZ-TSM:First project",
            ),
            (
                "urn:geant:helmholtz.de:group:HelmholtzDataHub#login.helmholtz.de",
                "HelmholtzDataHub",
            ),
            (
                "urn:geant:helmholtz.de:group:UFZ-TSM:First project:ufz-sms-member#login.helmholtz.de",
                "UFZ-TSM:First project:ufz-sms-member",
            ),
            (
                "urn:geant:helmholtz.de:group:Moses:Mariner-Kohlenstoff#login.helmholtz.de",
                "Moses:Mariner-Kohlenstoff",
            ),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement#login.helmholtz.de",
                "KIT_SensorManagement",
            ),
            (
                "urn:geant:helmholtz.de:group:Moses:HydrEx#login.helmholtz.de",
                "Moses:HydrEx",
            ),
            (
                "urn:geant:helmholtz.de:group:WETSCAPES2.0:SMS#login.helmholtz.de",
                "WETSCAPES2.0:SMS",
            ),
            ("urn:geant:helmholtz.de:group:Moses#login.helmholtz.de", "Moses"),
            (
                "urn:geant:helmholtz.de:group:KIT_SensorManagement:imk-aaf:kit-sms-admin#login.helmholtz.de",
                "KIT_SensorManagement:imk-aaf:kit-sms-admin",
            ),
            (
                "urn:geant:helmholtz.de:group:Sensors-Sandbox#login.helmholtz.de",
                "Sensors-Sandbox",
            ),
            (
                "urn:geant:helmholtz.de:res:FZJ-IBG-3_Sensor_Management_System:agrasim:members#login.helmholtz.de",
                "FZJ-IBG-3_Sensor_Management_System:agrasim:members",
            ),
            (
                "a:a:a:group:VO:Group2#",
                "VO:Group2",
            ),
            (
                "urn:geant:helmholtz.de:group:x:group:res:Some difficult #name#login.helmholtz.de",
                "x:group:res:Some difficult #name",
            ),
        ]

        for test_input, expected_output in test_cases:
            output = PermissionGroup.convert_entitlement_to_name(test_input)
            self.assertEqual(output, expected_output)

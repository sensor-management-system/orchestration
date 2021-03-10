import unittest

from .api.test_configuration_generic_action import (
    TestGenericConfigurationActionServices,
)
from .api.test_configurations import TestConfigurationsService
from .api.test_contacts import TestContactServices
from .api.test_device_calibration_action import TestDeviceCalibrationAction
from .api.test_device_calibration_attachment import TestDeviceCalibrationAttachment
from .api.test_device_mount_action import TestDeviceMountAction
from .api.test_device_property_calibration import TestDevicePropertyCalibration
from .api.test_device_software_update_action_attachment import (
    TestDeviceSoftwareUpdateActionAttachment,
)
from .api.test_device_software_update_actions import TestDeviceSoftwareUpdateAction
from .api.test_device_unmount_action import TestDeviceUnmountAction
from .api.test_devices import TestDeviceService
from .api.test_generic_configuration_action import TestGenericConfigurationAction
from .api.test_generic_configuration_action_attachment import \
    TestGenericConfigurationActionAttachment
from .api.test_generic_device_action import TestGenericDeviceAction
from .api.test_generic_device_action_attachment import TestGenericDeviceActionAttachment
from .api.test_generic_platform_action import TestGenericPlatformAction
from .api.test_generic_platform_action_attachment import TestGenericPlatformActionAttachment
from .api.test_platform_software_update_action import TestPlatformSoftwareUpdateAction
from .api.test_platform_unmount_action import TestPlatformUnmountAction
from .api.test_platforms import TestPlatformServices
from .models.test_configuration_generic_action_model import (
    TestConfigurationObjectsModel,
)
from .models.test_configurations_model import TestConfigurationsModel
from .models.test_contacts import TestContactModels
from .models.test_device_calibration_action_model import (
    TestDeviceCalibrationActionModel,
)
from .models.test_device_calibration_attachment_model import (
    TestDeviceCalibrationAttachmentModel,
)
from .models.test_devices_model import TestDeviceModel
from .models.test_generic_action_attachment_model import TestGenericActionModel
from .models.test_generic_actions_models import TestGenericActions
from .models.test_mount_actions_model import TestMountActionsModel
from .models.test_platforms import TestPlatformModel
from .models.test_software_update_actions_attachment_model import (
    TestSoftwareUpdateActionAttachmentModel,
)
from .models.test_software_update_actions_model import (
    TestDeviceSoftwareUpdateActionModel,
)
from .models.test_unmount_actions_model import TestUnMountActionModel
from .models.test_user_model import TestUsersModel
from .test_config import TestDevelopmentConfig, TestProductionConfig, TestTestingConfig
from .test_esquerybuilder import TestEsQueryBuilder
from .test_health_check import HealthCheck
from .test_render_csv import Test


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HealthCheck))
    suite.addTest(unittest.makeSuite(TestDevelopmentConfig))
    suite.addTest(unittest.makeSuite(TestTestingConfig))
    suite.addTest(unittest.makeSuite(TestProductionConfig))
    suite.addTest(unittest.makeSuite(Test))
    suite.addTest(unittest.makeSuite(TestEsQueryBuilder))
    # Models
    suite.addTest(unittest.makeSuite(TestConfigurationObjectsModel))
    suite.addTest(unittest.makeSuite(TestConfigurationsModel))
    suite.addTest(unittest.makeSuite(TestContactModels))
    suite.addTest(unittest.makeSuite(TestDeviceCalibrationActionModel))
    suite.addTest(unittest.makeSuite(TestDeviceCalibrationAttachmentModel))
    suite.addTest(unittest.makeSuite(TestDeviceModel))
    suite.addTest(unittest.makeSuite(TestGenericActionModel))
    suite.addTest(unittest.makeSuite(TestGenericActions))
    suite.addTest(unittest.makeSuite(TestMountActionsModel))
    suite.addTest(unittest.makeSuite(TestPlatformModel))
    suite.addTest(unittest.makeSuite(TestSoftwareUpdateActionAttachmentModel))
    suite.addTest(unittest.makeSuite(TestDeviceSoftwareUpdateActionModel))
    suite.addTest(unittest.makeSuite(TestUnMountActionModel))
    suite.addTest(unittest.makeSuite(TestUsersModel))
    # API
    suite.addTest(unittest.makeSuite(TestGenericConfigurationActionServices))
    suite.addTest(unittest.makeSuite(TestConfigurationsService))
    suite.addTest(unittest.makeSuite(TestContactServices))
    suite.addTest(unittest.makeSuite(TestDeviceCalibrationAction))
    suite.addTest(unittest.makeSuite(TestDeviceMountAction))
    suite.addTest(unittest.makeSuite(TestDevicePropertyCalibration))
    suite.addTest(unittest.makeSuite(TestDeviceSoftwareUpdateActionAttachment))
    suite.addTest(unittest.makeSuite(TestDeviceUnmountAction))
    suite.addTest(unittest.makeSuite(TestDeviceService))
    suite.addTest(unittest.makeSuite(TestGenericConfigurationAction))
    suite.addTest(unittest.makeSuite(TestGenericConfigurationActionAttachment))
    suite.addTest(unittest.makeSuite(TestGenericDeviceAction))
    suite.addTest(unittest.makeSuite(TestGenericDeviceActionAttachment))
    suite.addTest(unittest.makeSuite(TestGenericPlatformAction))
    suite.addTest(unittest.makeSuite(TestGenericPlatformActionAttachment))
    suite.addTest(unittest.makeSuite(TestPlatformSoftwareUpdateAction))
    suite.addTest(unittest.makeSuite(TestPlatformUnmountAction))
    suite.addTest(unittest.makeSuite(TestPlatformServices))
    suite.addTest(unittest.makeSuite(TestDeviceCalibrationAttachment))
    suite.addTest(unittest.makeSuite(TestDeviceSoftwareUpdateAction))
    return suite

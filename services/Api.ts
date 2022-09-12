/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { AxiosRequestConfig } from 'axios'

import { createAxios } from '@/utils/axiosHelper'

import { PermissionGroup } from '@/models/PermissionGroup'

import { ContactApi } from '@/services/sms/ContactApi'
import { DeviceApi } from '@/services/sms/DeviceApi'
import { DevicePropertyApi } from '@/services/sms/DevicePropertyApi'
import { PlatformApi } from '@/services/sms/PlatformApi'
import { ConfigurationApi } from '@/services/sms/ConfigurationApi'
import { ConfigurationStatusApi } from '@/services/sms/ConfigurationStatusApi'
import { CustomfieldsApi } from '@/services/sms/CustomfieldsApi'
import { DeviceAttachmentApi } from '@/services/sms/DeviceAttachmentApi'
import { DeviceCalibrationActionApi } from '@/services/sms/DeviceCalibrationActionApi'
import { PlatformAttachmentApi } from '@/services/sms/PlatformAttachmentApi'
import { GenericDeviceActionApi } from '@/services/sms/GenericDeviceActionApi'
import { GenericDeviceActionAttachmentApi, GenericPlatformActionAttachmentApi } from '@/services/sms/GenericActionAttachmentApi'
import { DeviceSoftwareUpdateActionApi } from '@/services/sms/DeviceSoftwareUpdateActionApi'
import { PlatformSoftwareUpdateActionApi } from '@/services/sms/PlatformSoftwareUpdateActionApi'
import { DeviceSoftwareUpdateActionAttachmentApi, PlatformSoftwareUpdateActionAttachmentApi } from '@/services/sms/SoftwareUpdateActionAttachmentApi'
import { StaticLocationBeginActionApi } from '@/services/sms/StaticLocationBeginActionApi'
import { StaticLocationEndActionApi } from '@/services/sms/StaticLocationEndActionApi'
import { DynamicLocationBeginActionApi } from '@/services/sms/DynamicLocationBeginActionApi'
import { DynamicLocationEndActionApi } from '@/services/sms/DynamicLocationEndActionApi'
import { UploadApi } from '@/services/sms/UploadApi'
import { PermissionGroupApi } from '@/services/sms/PermissionGroupApi'

import { CompartmentApi } from '@/services/cv/CompartmentApi'
import { CvContactRoleApi } from '@/services/cv/CvContactRoleApi'
import { DeviceTypeApi } from '@/services/cv/DeviceTypeApi'
import { ManufacturerApi } from '@/services/cv/ManufacturerApi'
import { PlatformTypeApi } from '@/services/cv/PlatformTypeApi'
import { PropertyApi } from '@/services/cv/PropertyApi'
import { SamplingMediaApi } from '@/services/cv/SamplingMediaApi'
import { StatusApi } from '@/services/cv/StatusApi'
import { UnitApi } from '@/services/cv/UnitApi'
import { MeasuredQuantityUnitApi } from '@/services/cv/MeasuredQuantityUnitApi'
import { ActionTypeApi } from '@/services/cv/ActionTypeApi'
import { SoftwareTypeApi } from '@/services/cv/SoftwareTypeApi'

import { DeviceMountActionApi } from '@/services/sms/DeviceMountActionApi'
import { PlatformMountActionApi } from '@/services/sms/PlatformMountActionApi'
import { GenericPlatformActionApi } from '@/services/sms/GenericPlatformActionApi'
import { DeviceCalibrationActionAttachmentApi } from '@/services/sms/DeviceCalibrationActionAttachmentApi'
import { DeviceCalibrationDevicePropertyApi } from '@/services/sms/DeviceCalibrationDevicePropertyApi'
import { MountingActionsControllerApi } from '@/services/sms/MountingActionsControllerApi'
import { StatisticsApi } from '@/services/sms/StatisticsApi'

import { ElevationDatumApi } from '@/services/cv/ElevationDatumApi'
import { EpsgCodeApi } from '@/services/cv/EpsgCodeApi'
import { UserInfoApi } from '@/services/sms/UserInfoApi'

const SMS_BASE_URL = process.env.smsBackendUrl
const CV_BASE_URL = process.env.cvBackendUrl

export class Api {
  private readonly _contactApi: ContactApi
  private readonly _deviceApi: DeviceApi
  private readonly _platformApi: PlatformApi
  private readonly _configurationApi: ConfigurationApi
  private readonly _configurationStatesApi: ConfigurationStatusApi
  private readonly _customfieldsApi: CustomfieldsApi
  private readonly _deviceAttachmentApi: DeviceAttachmentApi
  private readonly _platformAttachmentApi: PlatformAttachmentApi
  private readonly _devicePropertyApi: DevicePropertyApi
  private readonly _genericDeviceActionApi: GenericDeviceActionApi
  private readonly _genericPlatformActionApi: GenericPlatformActionApi
  private readonly _genericDeviceActionAttachmentApi: GenericDeviceActionAttachmentApi
  private readonly _genericPlatformActionAttachmentApi: GenericPlatformActionAttachmentApi
  private readonly _deviceSoftwareUpdateActionApi: DeviceSoftwareUpdateActionApi
  private readonly _deviceSoftwareUpdateActionAttachmentApi: DeviceSoftwareUpdateActionAttachmentApi
  private readonly _platformSoftwareUpdateActionApi: PlatformSoftwareUpdateActionApi
  private readonly _platformSoftwareUpdateActionAttachmentApi: PlatformSoftwareUpdateActionAttachmentApi
  private readonly _deviceCalibrationActionAttachmentApi: DeviceCalibrationActionAttachmentApi
  private readonly _devicePropertyCalibrationApi: DeviceCalibrationDevicePropertyApi
  private readonly _deviceCalibrationActionApi: DeviceCalibrationActionApi
  private readonly _staticLocationBeginActionApi: StaticLocationBeginActionApi
  private readonly _staticLocationEndActionApi: StaticLocationEndActionApi
  private readonly _dynamicLocationBeginActionApi: DynamicLocationBeginActionApi
  private readonly _dynamicLocationEndActionApi: DynamicLocationEndActionApi
  private readonly _mountingActionsControllerApi: MountingActionsControllerApi
  private readonly _uploadApi: UploadApi
  private readonly _statisticsApi: StatisticsApi

  private readonly _manufacturerApi: ManufacturerApi
  private readonly _platformTypeApi: PlatformTypeApi
  private readonly _statusApi: StatusApi
  private readonly _deviceTypeApi: DeviceTypeApi
  private readonly _compartmentApi: CompartmentApi
  private readonly _samplingMediaApi: SamplingMediaApi
  private readonly _propertyApi: PropertyApi
  private readonly _unitApi: UnitApi
  private readonly _measuredQuantityUnitApi: MeasuredQuantityUnitApi
  private readonly _actionTypeApi: ActionTypeApi
  private readonly _softwareTypeApi: SoftwareTypeApi
  private readonly _cvContactRoleApi: CvContactRoleApi

  private readonly _elevationDatumApi: ElevationDatumApi
  private readonly _epsgCodeApi: EpsgCodeApi

  private readonly _userInfoApi: UserInfoApi
  private readonly _permissionGroupApi: PermissionGroupApi

  constructor (
    getIdToken: () => string | null,
    smsBaseUrl: string | undefined = SMS_BASE_URL,
    cvBaseUrl: string | undefined = CV_BASE_URL
  ) {
    // here we can set settings for all the sms api calls
    const smsConfig: AxiosRequestConfig = {
      // for the SMS Backend we need the explicit vnd.api+json
      headers: {
        'Content-Type': 'application/vnd.api+json'
      }
    }
    // For the sms we also want to send the id token, if we currently
    // have one in the store.
    this._contactApi = new ContactApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/contacts'
    )
    this._platformApi = new PlatformApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/platforms',
      // callback function to fetch permission groups
      async (): Promise<PermissionGroup[]> => {
        const api = new PermissionGroupApi(
          createAxios(smsBaseUrl, smsConfig, getIdToken),
          '/permission-groups'
        )
        return await api.findAll(true)
      }
    )
    this._deviceApi = new DeviceApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/devices',
      // callback function to fetch permission groups
      async (): Promise<PermissionGroup[]> => {
        const api = new PermissionGroupApi(
          createAxios(smsBaseUrl, smsConfig, getIdToken),
          '/permission-groups'
        )
        return await api.findAll(true)
      }
    )

    const deviceMountActionApi = new DeviceMountActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-mount-actions'
    )
    const platformMountActionApi = new PlatformMountActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/platform-mount-actions'
    )
    this._staticLocationBeginActionApi = new StaticLocationBeginActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/static-location-begin-actions'
    )
    this._staticLocationEndActionApi = new StaticLocationEndActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/static-location-end-actions'
    )
    this._dynamicLocationBeginActionApi = new DynamicLocationBeginActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/dynamic-location-begin-actions'
    )
    this._dynamicLocationEndActionApi = new DynamicLocationEndActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/dynamic-location-end-actions'
    )
    this._mountingActionsControllerApi = new MountingActionsControllerApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/controller/configurations'
    )
    this._configurationApi = new ConfigurationApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/configurations',
      deviceMountActionApi,
      platformMountActionApi,
      this._staticLocationBeginActionApi,
      this._staticLocationEndActionApi,
      this._dynamicLocationBeginActionApi,
      this._dynamicLocationEndActionApi,
      this._mountingActionsControllerApi,
      // callback function to fetch permission groups
      async (): Promise<PermissionGroup[]> => {
        const api = new PermissionGroupApi(
          createAxios(smsBaseUrl, smsConfig, getIdToken),
          '/permission-groups'
        )
        return await api.findAll()
      }
    )
    this._configurationStatesApi = new ConfigurationStatusApi()

    this._customfieldsApi = new CustomfieldsApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/customfields'
    )

    this._deviceAttachmentApi = new DeviceAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-attachments'
    )

    this._platformAttachmentApi = new PlatformAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/platform-attachments'
    )

    this._devicePropertyApi = new DevicePropertyApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-properties'
    )

    this._genericDeviceActionAttachmentApi = new GenericDeviceActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-device-action-attachments'
    )

    this._genericDeviceActionApi = new GenericDeviceActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-device-actions',
      this._genericDeviceActionAttachmentApi
    )

    this._genericPlatformActionAttachmentApi = new GenericPlatformActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-platform-action-attachments'
    )

    this._genericPlatformActionApi = new GenericPlatformActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-platform-actions',
      this._genericPlatformActionAttachmentApi
    )

    this._deviceSoftwareUpdateActionAttachmentApi = new DeviceSoftwareUpdateActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-software-update-action-attachments'
    )

    this._deviceSoftwareUpdateActionApi = new DeviceSoftwareUpdateActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-software-update-actions',
      this._deviceSoftwareUpdateActionAttachmentApi
    )

    this._platformSoftwareUpdateActionAttachmentApi = new PlatformSoftwareUpdateActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/platform-software-update-action-attachments'
    )

    this._platformSoftwareUpdateActionApi = new PlatformSoftwareUpdateActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/platform-software-update-actions',
      this._platformSoftwareUpdateActionAttachmentApi
    )

    this._deviceCalibrationActionAttachmentApi = new DeviceCalibrationActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-calibration-attachments'
    )

    this._devicePropertyCalibrationApi = new DeviceCalibrationDevicePropertyApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-property-calibrations'
    )

    this._deviceCalibrationActionApi = new DeviceCalibrationActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/device-calibration-actions',
      this._deviceCalibrationActionAttachmentApi,
      this._devicePropertyCalibrationApi
    )

    this._uploadApi = new UploadApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/upload'
    )

    this._statisticsApi = new StatisticsApi(createAxios(smsBaseUrl, smsConfig, getIdToken), '')

    // and here we can set settings for all the cv api calls
    const cvConfig: AxiosRequestConfig = {
      headers: {
        Accept: 'application/vnd.api+json'
      }
    }

    this._compartmentApi = new CompartmentApi(
      createAxios(cvBaseUrl, cvConfig),
      '/compartments/'
    )
    this._deviceTypeApi = new DeviceTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/equipmenttypes/'
    )
    this._manufacturerApi = new ManufacturerApi(
      createAxios(cvBaseUrl, cvConfig),
      '/manufacturers/'
    )
    this._platformTypeApi = new PlatformTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/platformtypes/'
    )
    this._propertyApi = new PropertyApi(
      createAxios(cvBaseUrl, cvConfig),
      '/measuredquantities/'
    )
    this._samplingMediaApi = new SamplingMediaApi(
      createAxios(cvBaseUrl, cvConfig),
      '/samplingmedia/'
    )
    this._statusApi = new StatusApi(
      createAxios(cvBaseUrl, cvConfig),
      '/equipmentstatus/'
    )
    this._unitApi = new UnitApi(
      createAxios(cvBaseUrl, cvConfig),
      '/units/'
    )
    this._measuredQuantityUnitApi = new MeasuredQuantityUnitApi(
      createAxios(cvBaseUrl, cvConfig),
      '/measuredquantityunits/'
    )
    this._actionTypeApi = new ActionTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/actiontypes/'
    )
    this._softwareTypeApi = new SoftwareTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/softwaretypes/'
    )
    this._cvContactRoleApi = new CvContactRoleApi(
      createAxios(cvBaseUrl, cvConfig),
      '/contactroles/'
    )

    this._elevationDatumApi = new ElevationDatumApi()
    this._epsgCodeApi = new EpsgCodeApi()

    this._userInfoApi = new UserInfoApi(createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/user-info'
    )
    this._permissionGroupApi = new PermissionGroupApi(createAxios(smsBaseUrl, smsConfig, getIdToken), '/permission-groups')
  }

  get devices (): DeviceApi {
    return this._deviceApi
  }

  get platforms (): PlatformApi {
    return this._platformApi
  }

  get configurations (): ConfigurationApi {
    return this._configurationApi
  }

  get configurationStates (): ConfigurationStatusApi {
    return this._configurationStatesApi
  }

  get customfields (): CustomfieldsApi {
    return this._customfieldsApi
  }

  get deviceAttachments (): DeviceAttachmentApi {
    return this._deviceAttachmentApi
  }

  get platformAttachments (): PlatformAttachmentApi {
    return this._platformAttachmentApi
  }

  get deviceProperties (): DevicePropertyApi {
    return this._devicePropertyApi
  }

  get genericDeviceActions (): GenericDeviceActionApi {
    return this._genericDeviceActionApi
  }

  get genericPlatformActions (): GenericPlatformActionApi {
    return this._genericPlatformActionApi
  }

  get genericDeviceActionAttachments (): GenericDeviceActionAttachmentApi {
    return this._genericDeviceActionAttachmentApi
  }

  get deviceSoftwareUpdateActions (): DeviceSoftwareUpdateActionApi {
    return this._deviceSoftwareUpdateActionApi
  }

  get deviceSoftwareUpdateActionAttachments (): DeviceSoftwareUpdateActionAttachmentApi {
    return this._deviceSoftwareUpdateActionAttachmentApi
  }

  get platformSoftwareUpdateActions (): PlatformSoftwareUpdateActionApi {
    return this._platformSoftwareUpdateActionApi
  }

  get platformSoftwareUpdateActionAttachments (): PlatformSoftwareUpdateActionAttachmentApi {
    return this._platformSoftwareUpdateActionAttachmentApi
  }

  get deviceCalibrationActions (): DeviceCalibrationActionApi {
    return this._deviceCalibrationActionApi
  }

  get contacts (): ContactApi {
    return this._contactApi
  }

  get upload (): UploadApi {
    return this._uploadApi
  }

  get manufacturer (): ManufacturerApi {
    return this._manufacturerApi
  }

  get platformTypes (): PlatformTypeApi {
    return this._platformTypeApi
  }

  get states (): StatusApi {
    return this._statusApi
  }

  get deviceTypes (): DeviceTypeApi {
    return this._deviceTypeApi
  }

  get compartments (): CompartmentApi {
    return this._compartmentApi
  }

  get samplingMedia (): SamplingMediaApi {
    return this._samplingMediaApi
  }

  get properties (): PropertyApi {
    return this._propertyApi
  }

  get units (): UnitApi {
    return this._unitApi
  }

  get measuredQuantityUnits (): MeasuredQuantityUnitApi {
    return this._measuredQuantityUnitApi
  }

  get actionTypes (): ActionTypeApi {
    return this._actionTypeApi
  }

  get softwareTypes (): SoftwareTypeApi {
    return this._softwareTypeApi
  }

  get cvContactRoles (): CvContactRoleApi {
    return this._cvContactRoleApi
  }

  get elevationData (): ElevationDatumApi {
    return this._elevationDatumApi
  }

  get epsgCodes (): EpsgCodeApi {
    return this._epsgCodeApi
  }

  get userInfoApi (): UserInfoApi {
    return this._userInfoApi
  }

  get permissionGroupApi (): PermissionGroupApi {
    return this._permissionGroupApi
  }

  get statisticsApi (): StatisticsApi {
    return this._statisticsApi
  }
}

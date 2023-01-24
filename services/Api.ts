/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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

import { SiteTypeApi } from './cv/SiteTypeApi'
import { createAxios } from '@/utils/axiosHelper'

import { PermissionGroup } from '@/models/PermissionGroup'

import { ContactApi } from '@/services/sms/ContactApi'
import { DeviceApi } from '@/services/sms/DeviceApi'
import { DevicePropertyApi } from '@/services/sms/DevicePropertyApi'
import { PlatformApi } from '@/services/sms/PlatformApi'
import { ConfigurationApi } from '@/services/sms/ConfigurationApi'
import { ConfigurationStatusApi } from '@/services/sms/ConfigurationStatusApi'
import { DeviceCustomfieldsApi } from '@/services/sms/DeviceCustomfieldsApi'
import { DeviceAttachmentApi } from '@/services/sms/DeviceAttachmentApi'
import { DeviceCalibrationActionApi } from '@/services/sms/DeviceCalibrationActionApi'
import { PlatformAttachmentApi } from '@/services/sms/PlatformAttachmentApi'
import { ConfigurationAttachmentApi } from '@/services/sms/ConfigurationAttachmentApi'
import { ConfigurationCustomfieldsApi } from '@/services/sms/ConfigurationCustomfieldsApi'
import { GenericDeviceActionApi } from '@/services/sms/GenericDeviceActionApi'
import { GenericConfigurationActionApi } from '@/services/sms/GenericConfigurationActionApi'
import { GenericDeviceActionAttachmentApi, GenericPlatformActionAttachmentApi, GenericConfigurationActionAttachmentApi } from '@/services/sms/GenericActionAttachmentApi'
import { DeviceSoftwareUpdateActionApi } from '@/services/sms/DeviceSoftwareUpdateActionApi'
import { PlatformSoftwareUpdateActionApi } from '@/services/sms/PlatformSoftwareUpdateActionApi'
import { DeviceSoftwareUpdateActionAttachmentApi, PlatformSoftwareUpdateActionAttachmentApi } from '@/services/sms/SoftwareUpdateActionAttachmentApi'
import { StaticLocationActionApi } from '@/services/sms/StaticLocationActionApi'
import { DynamicLocationActionApi } from '@/services/sms/DynamicLocationActionApi'
import { UploadApi } from '@/services/sms/UploadApi'
import { PermissionGroupApi } from '@/services/sms/PermissionGroupApi'
import { PidApi } from '@/services/sms/PidApi'

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
import { GlobalProvenanceApi } from '@/services/cv/GlobalProvenanceApi'
import { AggregationTypeApi } from '@/services/cv/AggregationTypeApi'
import { ActionCategoryApi } from '@/services/cv/ActionCategoryApi'
import { SiteUsageApi } from '@/services/cv/SiteUsageApi'

import { DeviceMountActionApi } from '@/services/sms/DeviceMountActionApi'
import { PlatformMountActionApi } from '@/services/sms/PlatformMountActionApi'
import { GenericPlatformActionApi } from '@/services/sms/GenericPlatformActionApi'
import { DeviceCalibrationActionAttachmentApi } from '@/services/sms/DeviceCalibrationActionAttachmentApi'
import { DeviceCalibrationDevicePropertyApi } from '@/services/sms/DeviceCalibrationDevicePropertyApi'
import { MountingActionsControllerApi } from '@/services/sms/MountingActionsControllerApi'
import { StatisticsApi } from '@/services/sms/StatisticsApi'
import { AutocompleteApi } from '@/services/sms/AutocompleteApi'

import { ElevationDatumApi } from '@/services/cv/ElevationDatumApi'
import { EpsgCodeApi } from '@/services/cv/EpsgCodeApi'
import { UserInfoApi } from '@/services/sms/UserInfoApi'
import { LocationActionTimepointControllerApi } from '@/services/sms/LocationActionTimepointControllerApi'

import { SiteApi } from '@/services/sms/SiteApi'
import { SiteConfigurationsApi } from '@/services/sms/SiteConfigurationsApi'

const SMS_BASE_URL = process.env.smsBackendUrl
const CV_BASE_URL = process.env.cvBackendUrl

export class Api {
  private readonly _contactApi: ContactApi
  private readonly _deviceApi: DeviceApi
  private readonly _platformApi: PlatformApi
  private readonly _configurationApi: ConfigurationApi
  private readonly _siteApi: SiteApi
  private readonly _configurationStatesApi: ConfigurationStatusApi
  private readonly _deviceCustomfieldsApi: DeviceCustomfieldsApi
  private readonly _deviceAttachmentApi: DeviceAttachmentApi
  private readonly _platformAttachmentApi: PlatformAttachmentApi
  private readonly _configurationAttachmentApi: ConfigurationAttachmentApi
  private readonly _devicePropertyApi: DevicePropertyApi
  private readonly _genericDeviceActionApi: GenericDeviceActionApi
  private readonly _genericConfigurationActionApi: GenericConfigurationActionApi
  private readonly _genericPlatformActionApi: GenericPlatformActionApi
  private readonly _genericDeviceActionAttachmentApi: GenericDeviceActionAttachmentApi
  private readonly _genericPlatformActionAttachmentApi: GenericPlatformActionAttachmentApi
  private readonly _genericConfigurationActionAttachmentApi: GenericConfigurationActionAttachmentApi
  private readonly _configurationCustomfieldsApi: ConfigurationCustomfieldsApi

  private readonly _deviceSoftwareUpdateActionApi: DeviceSoftwareUpdateActionApi
  private readonly _deviceSoftwareUpdateActionAttachmentApi: DeviceSoftwareUpdateActionAttachmentApi
  private readonly _platformSoftwareUpdateActionApi: PlatformSoftwareUpdateActionApi
  private readonly _platformSoftwareUpdateActionAttachmentApi: PlatformSoftwareUpdateActionAttachmentApi
  private readonly _deviceCalibrationActionAttachmentApi: DeviceCalibrationActionAttachmentApi
  private readonly _devicePropertyCalibrationApi: DeviceCalibrationDevicePropertyApi
  private readonly _deviceCalibrationActionApi: DeviceCalibrationActionApi
  private readonly _mountingActionsControllerApi: MountingActionsControllerApi
  private readonly _staticLocationActionApi: StaticLocationActionApi
  private readonly _dynamicLocationActionApi: DynamicLocationActionApi
  private readonly _locationActionTimepointControllerApi: LocationActionTimepointControllerApi
  private readonly _uploadApi: UploadApi
  private readonly _statisticsApi: StatisticsApi
  private readonly _pidApi: PidApi

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
  private readonly _globalProvenanceApi: GlobalProvenanceApi
  private readonly _aggregationTypeApi: AggregationTypeApi
  private readonly _actionCategoryApi: ActionCategoryApi
  private readonly _autocompleteApi: AutocompleteApi
  private readonly _siteUsageApi: SiteUsageApi
  private readonly _siteTypeApi: SiteTypeApi

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

    const siteConfigurationsApi = new SiteConfigurationsApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/configurations',
      // callback function to fetch permission groups
      async (): Promise<PermissionGroup[]> => {
        const api = new PermissionGroupApi(
          createAxios(smsBaseUrl, smsConfig, getIdToken),
          '/permission-groups'
        )
        return await api.findAll(true)
      }
    )

    this._siteApi = new SiteApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/sites',
      siteConfigurationsApi,
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
    this._staticLocationActionApi = new StaticLocationActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/static-location-actions'
    )
    this._dynamicLocationActionApi = new DynamicLocationActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/dynamic-location-actions'
    )
    this._locationActionTimepointControllerApi = new LocationActionTimepointControllerApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/controller/configurations'
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
      this._staticLocationActionApi,
      this._dynamicLocationActionApi,
      this._locationActionTimepointControllerApi,
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

    this._deviceCustomfieldsApi = new DeviceCustomfieldsApi(
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

    this._configurationAttachmentApi = new ConfigurationAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/configuration-attachments'
    )

    this._configurationCustomfieldsApi = new ConfigurationCustomfieldsApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/configuration-customfields'
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

    this._genericConfigurationActionAttachmentApi = new GenericConfigurationActionAttachmentApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-configuration-action-attachments'
    )
    this._genericConfigurationActionApi = new GenericConfigurationActionApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/generic-configuration-actions',
      this._genericConfigurationActionAttachmentApi
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

    this._statisticsApi = new StatisticsApi(createAxios(smsBaseUrl, smsConfig), '')

    this._pidApi = new PidApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/pids'
    )

    this._autocompleteApi = new AutocompleteApi(
      createAxios(smsBaseUrl, smsConfig, getIdToken),
      '/controller'
    )

    // and here we can set settings for all the cv api calls
    const cvConfig: AxiosRequestConfig = {
      headers: {
        Accept: 'application/vnd.api+json'
      }
    }

    this._compartmentApi = new CompartmentApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/compartments/'
    )
    this._deviceTypeApi = new DeviceTypeApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/equipmenttypes/'
    )
    this._manufacturerApi = new ManufacturerApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/manufacturers/'
    )
    this._platformTypeApi = new PlatformTypeApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/platformtypes/'
    )
    this._propertyApi = new PropertyApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/measuredquantities/'
    )
    this._samplingMediaApi = new SamplingMediaApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/samplingmedia/'
    )
    this._statusApi = new StatusApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/equipmentstatus/'
    )
    this._unitApi = new UnitApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/units/'
    )
    this._measuredQuantityUnitApi = new MeasuredQuantityUnitApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/measuredquantityunits/'
    )
    this._actionTypeApi = new ActionTypeApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/actiontypes/'
    )
    this._softwareTypeApi = new SoftwareTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/softwaretypes/'
    )
    this._cvContactRoleApi = new CvContactRoleApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/contactroles/'
    )
    this._globalProvenanceApi = new GlobalProvenanceApi(
      createAxios(cvBaseUrl, cvConfig),
      '/globalprovenances/'
    )
    this._aggregationTypeApi = new AggregationTypeApi(
      createAxios(cvBaseUrl, cvConfig),
      '/aggregationtypes/'
    )
    this._actionCategoryApi = new ActionCategoryApi(
      createAxios(cvBaseUrl, cvConfig),
      '/actioncategories/'
    )
    this._siteUsageApi = new SiteUsageApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/siteusages/'
    )
    this._siteTypeApi = new SiteTypeApi(
      createAxios(cvBaseUrl, cvConfig, getIdToken),
      '/sitetypes/'
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

  get sites (): SiteApi {
    return this._siteApi
  }

  get configurationStates (): ConfigurationStatusApi {
    return this._configurationStatesApi
  }

  get deviceCustomfields (): DeviceCustomfieldsApi {
    return this._deviceCustomfieldsApi
  }

  get deviceAttachments (): DeviceAttachmentApi {
    return this._deviceAttachmentApi
  }

  get platformAttachments (): PlatformAttachmentApi {
    return this._platformAttachmentApi
  }

  get configurationAttachments (): ConfigurationAttachmentApi {
    return this._configurationAttachmentApi
  }

  get configurationCustomfields (): ConfigurationCustomfieldsApi {
    return this._configurationCustomfieldsApi
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

  get genericConfigurationActions (): GenericConfigurationActionApi {
    return this._genericConfigurationActionApi
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

  get pids (): PidApi {
    return this._pidApi
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

  get actionCategories (): ActionCategoryApi {
    return this._actionCategoryApi
  }

  get softwareTypes (): SoftwareTypeApi {
    return this._softwareTypeApi
  }

  get autocomplete (): AutocompleteApi {
    return this._autocompleteApi
  }

  get cvContactRoles (): CvContactRoleApi {
    return this._cvContactRoleApi
  }

  get globalProvenances (): GlobalProvenanceApi {
    return this._globalProvenanceApi
  }

  get aggregationTypes (): AggregationTypeApi {
    return this._aggregationTypeApi
  }

  get elevationData (): ElevationDatumApi {
    return this._elevationDatumApi
  }

  get epsgCodes (): EpsgCodeApi {
    return this._epsgCodeApi
  }

  get siteUsages (): SiteUsageApi {
    return this._siteUsageApi
  }

  get siteTypes (): SiteTypeApi {
    return this._siteTypeApi
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

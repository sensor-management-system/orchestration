/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

import ContactApi from '@/services/sms/ContactApi'
import DeviceApi from '@/services/sms/DeviceApi'
import PlatformApi from '@/services/sms/PlatformApi'
import ConfigurationApi from '@/services/sms/ConfigurationApi'

import CompartmentApi from '@/services/cv/CompartmentApi'
import DeviceTypeApi from '@/services/cv/DeviceTypeApi'
import ManufacturerApi from '@/services/cv/ManufacturerApi'
import PlatformTypeApi from '@/services/cv/PlatformTypeApi'
import PropertyApi from '@/services/cv/PropertyApi'
import SamplingMediaApi from '@/services/cv/SamplingMediaApi'
import StatusApi from '@/services/cv/StatusApi'
import UnitApi from '@/services/cv/UnitApi'

const SMS_BASE_URL = process.env.smsBackendUrl
const CV_BASE_URL = process.env.cvBackendUrl

export default class Api {
  private readonly _contactApi: ContactApi
  private readonly _deviceApi: DeviceApi
  private readonly _platformApi: PlatformApi
  private readonly _configurationApi: ConfigurationApi

  private readonly _manufacturerApi: ManufacturerApi
  private readonly _platformTypeApi: PlatformTypeApi
  private readonly _statusApi: StatusApi
  private readonly _deviceTypeApi: DeviceTypeApi
  private readonly _comparmentApi: CompartmentApi
  private readonly _samplingMediaApi: SamplingMediaApi
  private readonly _propertyApi: PropertyApi
  private readonly _unitApi: UnitApi

  constructor (smsBaseUrl: string | undefined = SMS_BASE_URL, cvBaseUrl: string | undefined = CV_BASE_URL) {
    // here we can set settings for all the sms api calls
    const smsConfig: AxiosRequestConfig = {
    }

    this._contactApi = new ContactApi(
      this.createAxios(smsBaseUrl, '/contacts', smsConfig)
    )
    this._platformApi = new PlatformApi(
      this.createAxios(smsBaseUrl, '/platforms', smsConfig)
    )
    this._deviceApi = new DeviceApi(
      this.createAxios(smsBaseUrl, '/devices', smsConfig)
    )
    this._configurationApi = new ConfigurationApi(
      this.createAxios(smsBaseUrl, '/configurations', smsConfig)
    )

    // and here we can set settings for all the cv api calls
    const cvConfig: AxiosRequestConfig = {
    }

    this._comparmentApi = new CompartmentApi(
      this.createAxios(cvBaseUrl, '/variabletype', cvConfig),
      cvBaseUrl
    )
    this._deviceTypeApi = new DeviceTypeApi(
      this.createAxios(cvBaseUrl, '/equipmenttype', cvConfig),
      cvBaseUrl
    )
    this._manufacturerApi = new ManufacturerApi(
      this.createAxios(cvBaseUrl, '/manufacturer', cvConfig),
      cvBaseUrl
    )
    this._platformTypeApi = new PlatformTypeApi(
      this.createAxios(cvBaseUrl, '/platformtype', cvConfig),
      cvBaseUrl
    )
    this._propertyApi = new PropertyApi(
      this.createAxios(cvBaseUrl, '/variablename', cvConfig),
      cvBaseUrl
    )
    this._samplingMediaApi = new SamplingMediaApi(
      this.createAxios(cvBaseUrl, '/medium', cvConfig),
      cvBaseUrl
    )
    this._statusApi = new StatusApi(
      this.createAxios(cvBaseUrl, '/equipmentstatus', cvConfig),
      cvBaseUrl
    )
    this._unitApi = new UnitApi(
      this.createAxios(cvBaseUrl, '/unit', cvConfig),
      cvBaseUrl
    )
  }

  private createAxios (baseUrl: string | undefined, path: string, baseConfig: AxiosRequestConfig): AxiosInstance {
    const config = {
      ...baseConfig,
      baseURL: baseUrl + path
    }
    return axios.create(config)
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

  get contacts (): ContactApi {
    return this._contactApi
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
    return this._comparmentApi
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
}

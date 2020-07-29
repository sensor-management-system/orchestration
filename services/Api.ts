import ContactApi from '@/services/sms/ContactApi'
import DeviceApi from '@/services/sms/DeviceApi'
import PlatformApi from '@/services/sms/PlatformApi'

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

  private readonly _manufacturerApi: ManufacturerApi
  private readonly _platformTypeApi: PlatformTypeApi
  private readonly _statusApi: StatusApi
  private readonly _deviceTypeApi: DeviceTypeApi
  private readonly _comparmentApi: CompartmentApi
  private readonly _samplingMediaApi: SamplingMediaApi
  private readonly _propertyApi: PropertyApi
  private readonly _unitApi: UnitApi

  constructor (smsBaseUrl: string | undefined = SMS_BASE_URL, cvBaseUrl: string | undefined = CV_BASE_URL) {
    this._contactApi = new ContactApi(smsBaseUrl + '/contacts')
    this._platformApi = new PlatformApi(smsBaseUrl + '/platforms')
    this._deviceApi = new DeviceApi(smsBaseUrl + '/devices')

    this._comparmentApi = new CompartmentApi(cvBaseUrl + '/variabletype')
    this._deviceTypeApi = new DeviceTypeApi(cvBaseUrl + '/equipmenttype')
    this._manufacturerApi = new ManufacturerApi(cvBaseUrl + '/manufacturer')
    this._platformTypeApi = new PlatformTypeApi(cvBaseUrl + '/platformtype')
    this._propertyApi = new PropertyApi(cvBaseUrl + '/variablename')
    this._samplingMediaApi = new SamplingMediaApi(cvBaseUrl + '/medium')
    this._statusApi = new StatusApi(cvBaseUrl + '/equipmentstatus')
    this._unitApi = new UnitApi(cvBaseUrl + '/unit')
  }

  get devices (): DeviceApi {
    return this._deviceApi
  }

  get platforms (): PlatformApi {
    return this._platformApi
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

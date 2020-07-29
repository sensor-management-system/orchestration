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

export class SmsApi {
  private _deviceApi: DeviceApi = new DeviceApi()
  private _platformApi: PlatformApi = new PlatformApi()
  private _contactApi: ContactApi = new ContactApi()

  get devices (): DeviceApi {
    return this._deviceApi
  }

  get platforms (): PlatformApi {
    return this._platformApi
  }

  get contacts (): ContactApi {
    return this._contactApi
  }
}

export class CvApi {
  private _manufacturerApi: ManufacturerApi = new ManufacturerApi()
  private _platformTypeApi: PlatformTypeApi = new PlatformTypeApi()
  private _statusApi: StatusApi = new StatusApi()
  private _deviceTypeApi: DeviceTypeApi = new DeviceTypeApi()
  private _comparmentApi: CompartmentApi = new CompartmentApi()
  private _samplingMediaApi: SamplingMediaApi = new SamplingMediaApi()
  private _propertyApi: PropertyApi = new PropertyApi()
  private _unitApi: UnitApi = new UnitApi()

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

export default class Api {
  private _smsApi: SmsApi = new SmsApi()
  private _cvApi: CvApi = new CvApi()

  get sms (): SmsApi {
    return this._smsApi
  }

  get cv (): CvApi {
    return this._cvApi
  }
}

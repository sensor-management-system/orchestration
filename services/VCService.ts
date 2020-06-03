import Manufacturer from '../models/Manufacturer'

export default class VCService {
  static findAllManufacturers (): Promise<Manufacturer[]> {
    return new Promise<Manufacturer[]>((resolve) => {
      resolve([
        Manufacturer.createWithData(1, 'Manufacturer 01', 'http://helmholtz/sms/manfucturer/1'),
        Manufacturer.createWithData(2, 'Manufacturer 02', 'http://helmholtz/sms/manfucturer/2'),
      ])
    })
  }

  static findAllPlatformTypes (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'Station',
        'Drone',
        'Vessel',
        'Vehicle',
        'Satellite'
      ])
    })
  }

  static findAllTypes (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'test type'
      ])
    })
  }

  static findAllStates (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'in warehouse',
        'in use',
        'under construction',
        'blocked',
        'scrapped'
      ])
    })
  }

  static findAllDeviceTypes (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'Einzelsensor',
        'Multiparameter Sonde'
      ])
    })
  }
}

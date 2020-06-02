import Institute from './../models/Institute'

export default class MasterDataService {
  static findAllManufacturers (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'Manufacturer 01',
        'Manufacturer 02'
      ])
    })
  }

  static findAllInstitutes (): Promise<Institute[]> {
    return new Promise<Institute[]>((resolve) => {
      resolve([
        Institute.createWithIdAndName(1, 'UFZ'),
        Institute.createWithIdAndName(2, 'GFZ')
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

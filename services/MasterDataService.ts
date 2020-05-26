import Institute from './../models/Institute'

export default class MasterDataService {
  static findAllManufacturers (): Promise<String[]> {
    return new Promise<String[]>((resolve) => {
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

  static findAllPlatformTypes (): Promise<String[]> {
    return new Promise<String[]>((resolve) => {
      resolve([
        'Station',
        'Drone',
        'Vessel',
        'Vehicle',
        'Satellite'
      ])
    })
  }

  static findAllTypes (): Promise<String[]> {
    return new Promise<String[]>((resolve) => {
      resolve([
        'test type'
      ])
    })
  }

  static findAllStates (): Promise<String[]> {
    return new Promise<String[]>((resolve) => {
      resolve([
        'in warehouse',
        'in use',
        'under construction',
        'blocked',
        'scrapped'
      ])
    })
  }

  static findAllDeviceTypes (): Promise<String[]> {
    return new Promise<String[]>((resolve) => {
      resolve([
        'Einzelsensor',
        'Multiparameter Sonde'
      ])
    })
  }
}

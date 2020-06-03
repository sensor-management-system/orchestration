export default class MasterDataService {
  static findAllManufacturers (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve([
        'Manufacturer 01',
        'Manufacturer 02'
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

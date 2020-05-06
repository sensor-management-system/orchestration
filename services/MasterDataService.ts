import Manufacture from './../models/Manufacture'
import Institute from './../models/Institute'
import PlatformType from './../models/PlatformType'

export default class MasterDataService {
  static findAllManufactures (): Promise<Manufacture[]> {
    return new Promise<Manufacture[]>((resolve) => {
      resolve([
        Manufacture.createWithIdAndName(1, 'Manufacture 01'),
        Manufacture.createWithIdAndName(2, 'Manufacture 02')
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

  static findAllParameter (): Promise<Array<object>> {
    return new Promise((resolve) => {
      resolve([
        {
          id: 1,
          name: 'Parameter 01'
        }
      ])
    })
  }

  static findAllPlatformTypes (): Promise<PlatformType[]> {
    return new Promise<PlatformType[]>((resolve) => {
      resolve([
        PlatformType.createWithIdAndName(1, 'Station'),
        PlatformType.createWithIdAndName(2, 'Drone'),
        PlatformType.createWithIdAndName(3, 'Vessel'),
        PlatformType.createWithIdAndName(4, 'Vehicle'),
        PlatformType.createWithIdAndName(5, 'Satellite')
      ])
    })
  }
}

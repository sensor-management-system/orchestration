import Manufacturer from '../models/Manufacturer'
import PlatformType from '~/models/PlatformType'
import PlatformStatus from '~/models/PlatformStatus'

export default class VCService {
  static findAllManufacturers (): Promise<Manufacturer[]> {
    return new Promise<Manufacturer[]>((resolve) => {
      resolve([
        Manufacturer.createWithData(1, 'Manufacturer 01', 'http://helmholtz/smsvc/manfucturer/1'),
        Manufacturer.createWithData(2, 'Manufacturer 02', 'http://helmholtz/smsvs/manfucturer/2')
      ])
    })
  }

  static findAllPlatformTypes (): Promise<PlatformType[]> {
    return new Promise<PlatformType[]>((resolve) => {
      resolve([
        PlatformType.createWithData(1, 'Station', 'http://helmholtz/smsvc/platformtype/1'),
        PlatformType.createWithData(2, 'Drone', 'http://helmholtz/smsvc/platformtype/2'),
        PlatformType.createWithData(3, 'Vessel', 'http://helmholtz/smsvc/platformtype/3'),
        PlatformType.createWithData(4, 'Vehicle', 'http://helmholtz/smsvc/platformtype/4'),
        PlatformType.createWithData(5, 'Satellite', 'http://helmholtz/smsvc/platformtype/5')
      ])
    })
  }

  static findAllPlatformStates (): Promise<PlatformStatus[]> {
    return new Promise<PlatformStatus[]>((resolve) => {
      resolve([
        PlatformStatus.createWithData(1, 'in warehouse', 'https//helmholtz/smsvc/platformstatus/1'),
        PlatformStatus.createWithData(2, 'in use', 'https//helmholtz/smsvc/platformstatus/2'),
        PlatformStatus.createWithData(3, 'under construction', 'https//helmholtz/smsvc/platformstatus/3'),
        PlatformStatus.createWithData(4, 'blocked', 'https//helmholtz/smsvc/platformstatus/4'),
        PlatformStatus.createWithData(5, 'scrapped', 'https//helmholtz/smsvc/platformstatus/5')
      ])
    })
  }

  static findAllDeviceStates (): Promise<string[]> {
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

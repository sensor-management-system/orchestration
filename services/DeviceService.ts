import Platform from '../models/Platform'
import PlatformType from '../models/PlatformType'
import Person from '../models/Person'

import MasterDataService from './MasterDataService'

const fakeDb = {
  platforms: [
    Platform.createWithIdAndData(1, 1, 'Boeken', 'Boeken', 'The Boeken station', 1, '', [Person.createWithIdAndName(1, 'Person 1')]),
    Platform.createWithIdAndData(2, 3, 'Polarstern', 'Polarsterrn', 'The icebreaker', 1, '', [Person.createWithIdAndName(1, 'Person 1'), Person.createWithIdAndName(2, 'Person 2')])
  ]
}

export default class DeviceService {
  static findPlatformById (id: string): Promise<Platform> {
    const searchId = Number.parseInt(id)
    return new Promise((resolve, reject) => {
      for (const platform of fakeDb.platforms) {
        if (platform.id === searchId) {
          resolve(platform)
          break
        }
      }
      reject(Error('Not found'))
    })
  }

  static savePlatform (platform: Platform) {
    return new Promise((resolve) => {
      if (!platform.id) {
        let highestPlatformId = 0
        for (const dbPlatform of fakeDb.platforms) {
          const dbPlatformId = dbPlatform.id
          if (dbPlatformId != null) {
            if (highestPlatformId < dbPlatformId) {
              highestPlatformId = dbPlatformId
            }
          }
        }
        platform.id = highestPlatformId += 1
        fakeDb.platforms.push(platform)
        resolve(platform)
      } else {
        let idxToSet = null
        let idx = 0
        for (const dbPlatform of fakeDb.platforms) {
          if (dbPlatform.id === platform.id) {
            idxToSet = idx
            break
          }
          idx += 1
        }
        if (idxToSet != null) {
          fakeDb.platforms[idxToSet] = platform
          resolve(platform)
        }
      }
    })
  }

  static findPlatformsAndSensors (text: string | null): Promise<Array<object>> {
    return new Promise((resolve) => {
      MasterDataService.findAllPlatformTypes().then((platformTypes) => {
        const result = []

        let filterFunc = (_platform: any): boolean => { return true }

        if (text) {
          filterFunc = (platform: any): boolean => {
            return platform.shortName.includes(text)
          }
        }

        const platformTypeLookup: {[id: number] : PlatformType} = {}
        for (const platformType of platformTypes) {
          const platformTypeId: number | null = platformType.id
          if (platformTypeId != null) {
            const platformTypeIdNotNull: number = platformTypeId
            platformTypeLookup[platformTypeIdNotNull] = platformType
          }
        }

        for (const platform of fakeDb.platforms) {
          if (filterFunc(platform)) {
            let plType: string | null = 'null'
            if (platform.platformTypeId != null) {
              const platformTypeId: number = platform.platformTypeId
              if (platformTypeLookup[platformTypeId]) {
                plType = platformTypeLookup[platformTypeId].name
              }
            }
            result.push(
              {
                id: platform.id,
                name: platform.shortName,
                project: '...',
                type: plType,
                state: 'shipping',
                devicetype: 'platform'
              }
            )
          }
        }
        resolve(result)
      })
    })
  }
}

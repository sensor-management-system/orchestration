import masterdataservice from './masterdataservice'

const fakeDb = {
  platforms: [
    {
      id: 1,
      shortName: 'Boeken',
      longName: 'Boeken',
      description: 'The Boeken station',
      platformType: 1,
      responsiblePersons: [1]
    },
    {
      id: 2,
      shortName: 'Polarstern',
      longName: 'Polarstern',
      description: 'The icebreaker',
      platformType: 3,
      responsiblePersons: [2, 1]
    }
  ]
}

const findPlatformById = (id) => {
  const searchId = Number.parseInt(id)
  return new Promise((resolve, reject) => {
    for (const platform of fakeDb.platforms) {
      if (platform.id === searchId) {
        resolve(platform)
        break
      }
    }
    reject('Not found')
  })
}

const savePlatform = (platform) => {
  return new Promise((resolve) => {
    if (!platform.id) {
      let highestPlatformId = 0;
      for (const dbPlatform of fakeDb.platforms) {
        if (highestPlatformId < dbPlatform.id) {
          highestPlatformId = dbPlatform.id
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

const findPlatformsAndSensors = (text) => {
  return new Promise((resolve) => {
    masterdataservice.findAllPlatformTypes().then((platformTypes) => {

      const result = []

      let filterFunc = (platform) => { return true }

      if (text) {
        filterFunc = (platform) => {
          return platform.shortName.includes(text)
        }
      }

      const platformTypeLookup = {}
      for (const platformType of platformTypes) {
        platformTypeLookup[platformType.id] = platformType
      }

      for (const platform of fakeDb.platforms) {
        if (filterFunc(platform)) {
          result.push(
            {
              id: platform.id,
              name: platform.shortName,
              project: '...',
              type: platformTypeLookup[platform.platformType].name,
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

export default {
  findPlatformsAndSensors,
  findPlatformById,
  savePlatform
}

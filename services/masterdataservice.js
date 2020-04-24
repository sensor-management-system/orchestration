const findAllManufactures = () => {
  return new Promise((resolve) => {
    resolve([
      {
        id: 1,
        name: 'Manufacture 01'
      },
      {
        id: 2,
        name: 'Manufacture 02'
      }
    ])
  })
}

const findAllInstitutes = () => {
  return new Promise((resolve) => {
    resolve([
      {
        id: 1,
        name: 'UFZ'
      },
      {
        id: 2,
        name: 'GFZ'
      }
    ])
  })
}

const findAllParameter = () => {
  return new Promise((resolve) => {
    resolve([
      {
        id: 1,
        name: 'Parameter 01'
      }
    ])
  })
}

const findAllPlatformTypes = () => {
  return new Promise((resolve) => {
    resolve([
      {
        id: 1,
        name: 'Station'
      },
      {
        id: 2,
        name: 'Drone'
      },
      {
        id: 3,
        name: 'Vessel'
      },
      {
        id: 4,
        name: 'Vehicle'
      },
      {
        id: 5,
        name: 'Satellite'
      }
    ])
  })
}

export default {
  findAllManufactures,
  findAllInstitutes,
  findAllParameter,
  findAllPlatformTypes
}

// must be replaced by something that filters the
// persons that are part of a given project
const findAllPersons = () => {
  return new Promise((resolve) => {
    resolve([
      {
        id: 1,
        name: 'Person 1'
      },
      {
        id: 2,
        name: 'Person 2'
      }
    ])
  })
}

export default {
  findAllPersons
}
import Person from '../models/Person'

// must be replaced by something that filters the
// persons that are part of a given project
export default class PersonService {
  static findAllPersons (): Promise<Person[]> {
    return new Promise((resolve) => {
      resolve([
        Person.createWithIdAndName(1, 'Person 1'),
        Person.createWithIdAndName(2, 'Person 2')
      ])
    })
  }
}

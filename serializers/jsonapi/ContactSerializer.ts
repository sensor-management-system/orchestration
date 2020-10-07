import Contact from '@/models/Contact'

export default class ContactSerializer {
  convertJsonApiObjectToModel (jsonApiObject: any): Contact {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: any): Contact {
    const attributes = jsonApiData.attributes

    const newEntry = Contact.createEmpty()

    newEntry.id = jsonApiData.id
    newEntry.givenName = attributes.given_name || ''
    newEntry.familyName = attributes.family_name || ''
    newEntry.website = attributes.website || ''
    newEntry.email = attributes.email

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Contact[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }
}

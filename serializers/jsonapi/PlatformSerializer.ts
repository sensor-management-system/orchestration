import Contact from '@/models/Contact'
import Platform from '@/models/Platform'

import AttachmentSerializer from '@/serializers/jsonapi/AttachmentSerializer'
import ContactSerializer from '@/serializers/jsonapi/ContactSerializer'

export default class PlatformSerializer {
  convertJsonApiObjectToModel (jsonApiObject: any): Platform {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: any, included: any[]): Platform {
    const result: Platform = Platform.createEmpty()

    const contactSerializer = new ContactSerializer()
    const attachmentSerializer = new AttachmentSerializer()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships

    result.id = jsonApiData.id

    result.description = attributes.description || ''
    result.shortName = attributes.short_name || ''
    result.longName = attributes.long_name || ''
    result.manufacturerUri = attributes.manufacturer_uri || ''
    result.manufacturerName = attributes.manufacturer_name || ''
    result.model = attributes.model || ''
    result.platformTypeUri = attributes.platform_type_uri || ''
    result.platformTypeName = attributes.platform_type_name || ''
    result.statusUri = attributes.status_uri || ''
    result.statusName = attributes.status_name || ''
    result.website = attributes.website || ''
    result.createdAt = new Date(attributes.created_at)
    result.updatedAt = new Date(attributes.updated_at)

    // TODO
    // result.createdBy = attributes.created_by
    // result.updatedBy = attributes.updated_by

    result.inventoryNumber = attributes.inventory_number || ''
    result.serialNumber = attributes.serial_number || ''
    result.persistentIdentifier = attributes.persistent_identifier || ''

    // TODO
    // result.events = []

    result.attachments = attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)

    const contactIds = []
    if (relationships.contacts && relationships.contacts.data && relationships.contacts.data.length > 0) {
      for (const relationShipContactData of relationships.contacts.data) {
        const contactId = relationShipContactData.id
        contactIds.push(contactId)
      }
    }

    const possibleContacts: {[key: string]: Contact} = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'contact') {
          const contactId = includedEntry.id
          if (contactIds.includes(contactId)) {
            const contact = contactSerializer.convertJsonApiDataToModel(includedEntry)
            possibleContacts[contactId] = contact
          }
        }
      }
    }

    const contacts = []

    for (const contactId of contactIds) {
      if (possibleContacts[contactId]) {
        contacts.push(possibleContacts[contactId])
      } else {
        const contact = new Contact()
        contact.id = contactId
        contacts.push(contact)
      }
    }

    result.contacts = contacts

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Platform[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: any) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }
}

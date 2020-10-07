import Device from '@/models/Device'

import { Attachment } from '@/models/Attachment'
import Contact from '@/models/Contact'

import ContactSerializer from '@/serializers/jsonapi/ContactSerializer'
import CustomTextFieldSerializer from '@/serializers/jsonapi/CustomTextFieldSerializer'
import DevicePropertySerializer from '@/serializers/jsonapi/DevicePropertySerializer'

export class AttachmentSerializer {
  convertJsonApiElementToModel (attachment: any): Attachment {
    const result = new Attachment()
    result.id = attachment.id
    result.label = attachment.label || ''
    result.url = attachment.url || ''

    return result
  }

  convertNestedJsonApiToModelList (attachments: any[]): Attachment[] {
    return attachments.map(this.convertJsonApiElementToModel)
  }
}

export default class DeviceSerializer {
  convertJsonApiObjectToModel (jsonApiObject: any): Device {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: any, included: any[]): Device {
    const result: Device = new Device()

    const contactSerializer = new ContactSerializer()
    const devicePropertySerializer = new DevicePropertySerializer()
    const customTextFieldSerializer = new CustomTextFieldSerializer()
    const attachmentSerializer = new AttachmentSerializer()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships

    result.id = jsonApiData.id

    result.description = attributes.description || ''
    result.shortName = attributes.short_name || ''
    result.longName = attributes.long_name || ''
    result.serialNumber = attributes.serial_number || ''
    result.manufacturerUri = attributes.manufacturer_uri || ''
    result.manufacturerName = attributes.manufacturer_name || ''
    result.deviceTypeUri = attributes.device_type_uri || ''
    result.deviceTypeName = attributes.device_type_name || ''
    result.statusUri = attributes.status_uri || ''
    result.statusName = attributes.status_name || ''
    result.model = attributes.model || ''
    result.dualUse = attributes.dual_use || false
    result.inventoryNumber = attributes.inventory_number || ''
    result.persistentIdentifier = attributes.persistent_identifier || ''
    result.website = attributes.website || ''
    result.createdAt = new Date(attributes.created_at)
    result.updatedAt = new Date(attributes.updated_at)
    // TODO
    // result.createdBy = attributes.created_by
    // result.updatedBy = attributes.updated_by
    // result.events = []
    result.attachments = []
    result.contacts = []

    result.properties = devicePropertySerializer.convertNestedJsonApiToModelList(attributes.properties)
    result.customFields = customTextFieldSerializer.convertNestedJsonApiToModelList(attributes.customfields)
    result.attachments = attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)

    const contactIds = []
    if (relationships.contacts && relationships.contacts.data && relationships.contacts.data.length > 0) {
      for (const relationShipContactData of relationships.contacts.data) {
        const contactId = relationShipContactData.id
        contactIds.push(contactId)
      }
    }

    const possibleContacts: {
      [key: string]: Contact
    } = {}
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

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Device[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: any) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }
}

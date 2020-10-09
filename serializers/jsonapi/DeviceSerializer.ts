import Contact from '@/models/Contact'
import Device from '@/models/Device'

import AttachmentSerializer from '@/serializers/jsonapi/AttachmentSerializer'
import ContactSerializer from '@/serializers/jsonapi/ContactSerializer'
import CustomTextFieldSerializer from '@/serializers/jsonapi/CustomTextFieldSerializer'
import DevicePropertySerializer from '@/serializers/jsonapi/DevicePropertySerializer'

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

  convertModelToJsonApiData (device: Device): any {
    const properties = []

    for (const property of device.properties) {
      const propertyToSave: any = {}
      if (property.id != null) {
        // currently it seems that the id is always set to a higher value
        // I can set it to 8, but it will be saved with a new id (9)
        // there is already an issue for the backend, so hopefully it will be fixed there
        propertyToSave.id = property.id
      }

      propertyToSave.measuring_range_min = property.measuringRange.min
      propertyToSave.measuring_range_max = property.measuringRange.max
      propertyToSave.failure_value = property.failureValue
      propertyToSave.accuracy = property.accuracy
      propertyToSave.label = property.label
      propertyToSave.unit_uri = property.unitUri
      propertyToSave.unit_name = property.unitName
      propertyToSave.compartment_uri = property.compartmentUri
      propertyToSave.compartment_name = property.compartmentName
      propertyToSave.property_uri = property.propertyUri
      propertyToSave.property_name = property.propertyName
      propertyToSave.sampling_media_uri = property.samplingMediaUri
      propertyToSave.sampling_media_name = property.samplingMediaName

      properties.push(propertyToSave)
    }

    const customfields = []
    for (const customField of device.customFields) {
      const customFieldToSave: any = {}

      if (customField.id != null) {
        customFieldToSave.id = customField.id
      }

      customFieldToSave.key = customField.key
      customFieldToSave.value = customField.value

      customfields.push(customFieldToSave)
    }

    const attachments = []
    for (const attachment of device.attachments) {
      const attachmentToSave: any = {}
      if (attachment.id != null) {
        attachmentToSave.id = attachment.id
      }
      attachmentToSave.label = attachment.label
      attachmentToSave.url = attachment.url

      attachments.push(attachmentToSave)
    }

    const contacts = []
    for (const contact of device.contacts) {
      contacts.push({
        id: contact.id,
        type: 'contact'
      })
    }

    const data: any = {
      type: 'device',
      attributes: {
        description: device.description,
        short_name: device.shortName,
        long_name: device.longName,
        serial_number: device.serialNumber,
        inventory_number: device.inventoryNumber,
        manufacturer_uri: device.manufacturerUri,
        manufacturer_name: device.manufacturerName,
        device_type_uri: device.deviceTypeUri,
        device_type_name: device.deviceTypeName,
        status_uri: device.statusUri,
        status_name: device.statusName,
        model: device.model,
        persistent_identifier: device.persistentIdentifier === '' ? null : device.persistentIdentifier,
        website: device.website,
        dual_use: device.dualUse,
        // those two time slots are set by the db, no matter what we deliver here
        created_at: device.createdAt?.toISOString(),
        updated_at: device.updatedAt?.toISOString(),
        // TODO
        // created_by: device.createdBy,
        // updated_by: device.updatedBy,

        customfields,
        properties,
        attachments
      },
      relationships: {
        contacts: {
          data: contacts
        }
        // TODO: events
      }
    }

    if (device.id !== null) {
      data.id = device.id
    }

    return data
  }
}

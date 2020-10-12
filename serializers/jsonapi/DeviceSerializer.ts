import Device from '@/models/Device'

import AttachmentSerializer from '@/serializers/jsonapi/AttachmentSerializer'
import ContactSerializer from '@/serializers/jsonapi/ContactSerializer'
import CustomTextFieldSerializer from '@/serializers/jsonapi/CustomTextFieldSerializer'
import DevicePropertySerializer from '@/serializers/jsonapi/DevicePropertySerializer'

export default class DeviceSerializer {
  private attachmentSerializer: AttachmentSerializer = new AttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private customTextFieldSerializer: CustomTextFieldSerializer = new CustomTextFieldSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()

  convertJsonApiObjectToModel (jsonApiObject: any): Device {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: any, included: any[]): Device {
    const result: Device = new Device()

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

    result.attachments = this.attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)
    result.customFields = this.customTextFieldSerializer.convertNestedJsonApiToModelList(attributes.customfields)
    result.properties = this.devicePropertySerializer.convertNestedJsonApiToModelList(attributes.properties)
    result.contacts = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Device[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: any) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (device: Device): any {
    const properties = this.devicePropertySerializer.convertModelListToNestedJsonApiArray(device.properties)
    const customfields = this.customTextFieldSerializer.convertModelListToNestedJsonApiArray(device.customFields)
    const attachments = this.attachmentSerializer.convertModelListToNestedJsonApiArray(device.attachments)
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(device.contacts)

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
        ...contacts
        // TODO: events
      }
    }

    if (device.id !== null) {
      data.id = device.id
    }

    return data
  }
}

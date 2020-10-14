import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiDataWithId, IJsonApiDataWithOptionalId, IJsonApiTypeIdAttributes } from '@/serializers/jsonapi/JsonApiTypes'

import { AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { CustomTextFieldSerializer } from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

export interface IDeviceMissingData {
  contacts: IMissingContactData
}

export interface IDeviceWithMeta {
  device: Device
  missing: IDeviceMissingData
}

export class DeviceSerializer {
  private attachmentSerializer: AttachmentSerializer = new AttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private customTextFieldSerializer: CustomTextFieldSerializer = new CustomTextFieldSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): IDeviceWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId, included: IJsonApiTypeIdAttributes[]): IDeviceWithMeta {
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
    result.createdAt = attributes.created_at != null ? new Date(attributes.created_at) : null
    result.updatedAt = attributes.updated_at != null ? new Date(attributes.updated_at) : null
    // TODO
    // result.createdBy = attributes.created_by
    // result.updatedBy = attributes.updated_by
    // result.events = []

    result.attachments = this.attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)
    result.customFields = this.customTextFieldSerializer.convertNestedJsonApiToModelList(attributes.customfields)
    result.properties = this.devicePropertySerializer.convertNestedJsonApiToModelList(attributes.properties)

    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

    return {
      device: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): IDeviceWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiDataWithId) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (device: Device): IJsonApiDataWithOptionalId {
    const properties = this.devicePropertySerializer.convertModelListToNestedJsonApiArray(device.properties)
    const customfields = this.customTextFieldSerializer.convertModelListToNestedJsonApiArray(device.customFields)
    const attachments = this.attachmentSerializer.convertModelListToNestedJsonApiArray(device.attachments)
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(device.contacts)

    const data: IJsonApiDataWithOptionalId = {
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
        created_at: device.createdAt != null ? device.createdAt.toISOString() : null,
        updated_at: device.updatedAt != null ? device.updatedAt.toISOString() : null,
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

export const deviceWithMetaToDeviceByThrowingErrorOnMissing = (deviceWitHMeta: IDeviceWithMeta) : Device => {
  const device = deviceWitHMeta.device

  if (deviceWitHMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return device
}

export const deviceWithMetaToDeviceByAddingDummyObjects = (deviceWithMeta: IDeviceWithMeta) : Device => {
  const device = deviceWithMeta.device

  for (const missingContactId of deviceWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    device.contacts.push(contact)
  }

  return device
}

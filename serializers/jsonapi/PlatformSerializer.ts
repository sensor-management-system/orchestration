import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiDataWithId, IJsonApiTypeIdAttributes, IJsonApiDataWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

import { AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'

export interface IPlatformMissingData {
  contacts: IMissingContactData
}

export interface IPlatformWithMeta {
  platform: Platform
  missing: IPlatformMissingData
}

export class PlatformSerializer {
  private attachmentSerializer: AttachmentSerializer = new AttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): IPlatformWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId, included: IJsonApiTypeIdAttributes[]): IPlatformWithMeta {
    const result: Platform = Platform.createEmpty()

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
    result.createdAt = attributes.created_at != null ? new Date(attributes.created_at) : null
    result.updatedAt = attributes.updated_at != null ? new Date(attributes.updated_at) : null

    // TODO
    // result.createdBy = attributes.created_by
    // result.updatedBy = attributes.updated_by

    result.inventoryNumber = attributes.inventory_number || ''
    result.serialNumber = attributes.serial_number || ''
    result.persistentIdentifier = attributes.persistent_identifier || ''

    // TODO
    // result.events = []

    result.attachments = this.attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)
    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

    return {
      platform: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): IPlatformWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiDataWithId) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (platform: Platform): IJsonApiDataWithOptionalId {
    const attachments = this.attachmentSerializer.convertModelListToNestedJsonApiArray(platform.attachments)
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(platform.contacts)

    const data: IJsonApiDataWithOptionalId = {
      type: 'platform',
      attributes: {
        description: platform.description,
        short_name: platform.shortName,
        long_name: platform.longName,
        manufacturer_uri: platform.manufacturerUri,
        manufacturer_name: platform.manufacturerName,
        model: platform.model,
        platform_type_uri: platform.platformTypeUri,
        platform_type_name: platform.platformTypeName,
        status_uri: platform.statusUri,
        status_name: platform.statusName,
        website: platform.website,
        // those two time slots are set by the db, no matter what we deliver here
        created_at: platform.createdAt != null ? platform.createdAt.toISOString() : null,
        updated_at: platform.updatedAt != null ? platform.updatedAt.toISOString() : null,
        // TODO
        // created_by: platform.createdBy,
        // updated_by: platform.updatedBy,
        inventory_number: platform.inventoryNumber,
        serial_number: platform.serialNumber,
        // as the persistent_identifier must be unique, we sent null in case
        // that we don't have an identifier here
        persistent_identifier: platform.persistentIdentifier === '' ? null : platform.persistentIdentifier,
        attachments
      },
      relationships: {
        ...contacts
        // TODO: events
      }
    }

    if (platform.id !== null) {
      data.id = platform.id
    }

    return data
  }
}

export const platformWithMetaToPlatformByThrowingErrorOnMissing = (platformWithMeta: IPlatformWithMeta) : Platform => {
  const platform = platformWithMeta.platform

  if (platformWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return platform
}

export const platformWithMetaToPlatformByAddingDummyObjects = (platformWithMeta: IPlatformWithMeta) : Platform => {
  const platform = platformWithMeta.platform

  for (const missingContactId of platformWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    platform.contacts.push(contact)
  }

  return platform
}

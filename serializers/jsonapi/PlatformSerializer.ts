import Platform from '@/models/Platform'

import { AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

export class PlatformSerializer {
  private attachmentSerializer: AttachmentSerializer = new AttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()

  convertJsonApiObjectToModel (jsonApiObject: any): Platform {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: any, included: any[]): Platform {
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
    result.contacts = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Platform[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: any) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (platform: Platform): any {
    const attachments = this.attachmentSerializer.convertModelListToNestedJsonApiArray(platform.attachments)
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(platform.contacts)

    const data: any = {
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

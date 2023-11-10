/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PermissionGroup } from '@/models/PermissionGroup'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

import { IMissingAttachmentData } from '@/serializers/jsonapi/AttachmentSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'
import { ParameterSerializer, ParameterEntityType } from '@/serializers/jsonapi/ParameterSerializer'
import { Visibility } from '@/models/Visibility'

export interface IPlatformMissingData {
  contacts: IMissingContactData
  platformAttachments: IMissingAttachmentData
}

export interface IPlatformWithMeta {
  platform: Platform
  missing: IPlatformMissingData
}

export class PlatformSerializer {
  private attachmentSerializer: PlatformAttachmentSerializer = new PlatformAttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private parameterSerializer: ParameterSerializer = new ParameterSerializer(ParameterEntityType.PLATFORM)
  private _permissionGroups: PermissionGroup[] = []

  set permissionGroups (groups: PermissionGroup[]) {
    this._permissionGroups = groups
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): IPlatformWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): IPlatformWithMeta {
    const result: Platform = Platform.createEmpty()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    result.id = jsonApiData.id.toString()

    if (attributes) {
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
      result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
      result.updateDescription = attributes.update_description || ''

      result.inventoryNumber = attributes.inventory_number || ''
      result.serialNumber = attributes.serial_number || ''
      result.persistentIdentifier = attributes.persistent_identifier || ''
      result.country = attributes.country || ''

      if (attributes.is_private) {
        result.visibility = Visibility.Private
      }
      if (attributes.is_internal) {
        result.visibility = Visibility.Internal
      }
      if (attributes.is_public) {
        result.visibility = Visibility.Public
      }
      result.archived = attributes.archived || false
    }

    const attachmentsWithMissing = this.attachmentSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.attachments = attachmentsWithMissing.attachments
    const missingDataForAttachmentIds = attachmentsWithMissing.missing.ids

    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

    result.parameters = this.parameterSerializer.convertJsonApiRelationshipsModelList(relationships, included)

    if (attributes?.keywords) {
      result.keywords = [...attributes.keywords]
    }

    // just pick the contact from the relationships that is referenced by the created_by user
    if (relationships.created_by?.data && 'id' in relationships.created_by?.data) {
      const userId = (relationships.created_by.data as IJsonApiEntityWithoutDetails).id
      result.createdByUserId = userId
      const createdBy = this.contactSerializer.getContactFromIncludedByUserId(userId, included)
      if (createdBy) {
        result.createdBy = createdBy
      }
    }

    // just pick the contact from the relationships that is referenced by the updated_by user
    if (relationships.updated_by?.data && 'id' in relationships.updated_by?.data) {
      const userId = (relationships.updated_by.data as IJsonApiEntityWithoutDetails).id
      const updatedBy = this.contactSerializer.getContactFromIncludedByUserId(userId, included)
      if (updatedBy) {
        result.updatedBy = updatedBy
      }
    }

    if (attributes?.group_ids) {
      // look up the group in the provided permission group array. if it was
      // found, push the found group into the device's permissionGroups property
      // otherwise create a plain permission group object with just an ID
      const permissionGroups: PermissionGroup[] = attributes.group_ids.map((id: string) => {
        let group = this.permissionGroups.find(group => group.id === id)
        if (!group) {
          group = PermissionGroup.createFromObject({
            id
          })
        }
        return group
      })
      result.permissionGroups = permissionGroups
    }

    return {
      platform: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        },
        platformAttachments: {
          ids: missingDataForAttachmentIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): IPlatformWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiRelationshipsModelList (included: IJsonApiEntityWithOptionalAttributes[]): Platform[] {
    // it takes all the platforms, as those are the only ones included in the query per configuration.
    // if you want to use it in a broader scope, you may have to change several things
    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'platform') {
          const platform = this.convertJsonApiDataToModel(includedEntry, []).platform
          result.push(platform)
        }
      }
    }
    return result
  }

  convertModelToJsonApiData (platform: Platform, includeRelationships: boolean = false): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
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
        // these properties are set by the db, so we wont send anything related here:
        // modifiedAt
        // modifiedBy
        // created_by: platform.createdBy,
        // updated_by: platform.updatedBy,
        // update_description: platform.updateDescription,
        inventory_number: platform.inventoryNumber,
        serial_number: platform.serialNumber,
        // as the persistent_identifier must be unique, we sent null in case
        // that we don't have an identifier here
        persistent_identifier: platform.persistentIdentifier === '' ? null : platform.persistentIdentifier,
        is_private: platform.isPrivate,
        is_internal: platform.isInternal,
        is_public: platform.isPublic,
        group_ids: platform.permissionGroups.filter(i => i.id !== null).map(i => i.id),
        keywords: platform.keywords,
        country: platform.country
      }
    }

    if (includeRelationships) {
      const attachments = this.attachmentSerializer.convertModelListToJsonApiRelationshipObject(platform.attachments)
      const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(platform.contacts)
      const parameters = this.parameterSerializer.convertModelListToJsonApiRelationshipObject(platform.parameters)
      data.relationships = {
        ...contacts,
        ...attachments,
        ...parameters
      }
    }

    if (platform.id !== null) {
      data.id = platform.id
    }

    return data
  }
}

export const platformWithMetaToPlatformByThrowingErrorOnMissing = (platformWithMeta: { missing: { contacts: { ids: any[] } }; platform: Platform }): Platform => {
  const platform = platformWithMeta.platform

  if (platformWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return platform
}

export const platformWithMetaToPlatformByAddingDummyObjects = (platformWithMeta: { missing: { contacts: { ids: string[] } }; platform: Platform }): Platform => {
  const platform = platformWithMeta.platform

  for (const missingContactId of platformWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    platform.contacts.push(contact)
  }

  return platform
}
export const platformWithMetaToPlatformThrowingNoErrorOnMissing = (platformWithMeta: { missing: { contacts: { ids: any[] } }; platform: Platform }): Platform => {
  const platform = platformWithMeta.platform
  return platform
}

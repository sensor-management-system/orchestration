/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
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
import { DeviceImageSerializer } from '@/serializers/jsonapi/ImageSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import {
  CustomTextFieldSerializer,
  IMissingCustomTextFieldData
} from '@/serializers/jsonapi/CustomTextFieldSerializer'
import {
  DevicePropertySerializer,
  IMissingDevicePropertyData
} from '@/serializers/jsonapi/DevicePropertySerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'
import { ParameterSerializer, ParameterEntityType } from '@/serializers/jsonapi/ParameterSerializer'
import { Visibility } from '@/models/Visibility'

export interface IDeviceMissingData {
  contacts: IMissingContactData
  deviceAttachments: IMissingAttachmentData
  customfields: IMissingCustomTextFieldData
  properties: IMissingDevicePropertyData
}

export interface IDeviceWithMeta {
  device: Device
  missing: IDeviceMissingData
}

export class DeviceSerializer {
  private imageSerializer: DeviceImageSerializer = new DeviceImageSerializer()
  private attachmentSerializer: DeviceAttachmentSerializer = new DeviceAttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private customTextFieldSerializer: CustomTextFieldSerializer = new CustomTextFieldSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()
  private parameterSerializer: ParameterSerializer = new ParameterSerializer(ParameterEntityType.DEVICE)
  private _permissionGroups: PermissionGroup[] = []

  set permissionGroups (groups: PermissionGroup[]) {
    this._permissionGroups = groups
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): IDeviceWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): IDeviceWithMeta {
    const result: Device = new Device()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    result.id = jsonApiData.id.toString()

    if (attributes) {
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
      result.inventoryNumber = attributes.inventory_number || ''
      result.persistentIdentifier = attributes.persistent_identifier || ''
      result.website = attributes.website || ''
      result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
      result.updateDescription = attributes.update_description || ''
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

    const images = this.imageSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.images = images

    const attachmentsWithMissing = this.attachmentSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.attachments = attachmentsWithMissing.attachments
    const missingDataForAttachmentIds = attachmentsWithMissing.missing.ids

    const customFieldsWithMissing = this.customTextFieldSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.customFields = customFieldsWithMissing.customFields
    const missingDataForCustomFieldIds = customFieldsWithMissing.missing.ids

    const propertiesWithMissing = this.devicePropertySerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.properties = propertiesWithMissing.properties
    const missingDataForDevicePropertyIds = propertiesWithMissing.missing.ids

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
      device: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        },
        deviceAttachments: {
          ids: missingDataForAttachmentIds
        },
        customfields: {
          ids: missingDataForCustomFieldIds
        },
        properties: {
          ids: missingDataForDevicePropertyIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): IDeviceWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiRelationshipsModelList (included: IJsonApiEntityWithOptionalAttributes[]): Device[] {
    // it takes all the devices, as those are the only ones included in the query per configuration.
    // if you want to use it in a broader scope, you may have to change several things
    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device') {
          const device = this.convertJsonApiDataToModel(includedEntry, []).device
          result.push(device)
        }
      }
    }
    return result
  }

  convertModelToJsonApiData (device: Device, includeRelationships: boolean = false): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
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
        is_private: device.isPrivate,
        is_internal: device.isInternal,
        is_public: device.isPublic,
        group_ids: device.permissionGroups.filter(i => i.id !== null).map(i => i.id),
        keywords: device.keywords,
        country: device.country
        // these properties are set by the db, so we wont send anything related here:
        // createdAt
        // createdBy
        // modifiedAt
        // modifiedBy
        // updateDescription
      }
    }

    /*
      There are two use cases for this. One is that all the data is included in the model
      and that we send them togehter with the payload, so that the relationships are saved.
      This would be ok, if we also query & integrate them.
      When we don't include them & have no element for their existing relationship, adding the
      data here will mean to delete those elements.

      So in case we just want to save the basic entries of a device - and save, update & delete
      all the related elements seperatly, then we don't want to include tje relationships here.
    */
    if (includeRelationships) {
      const properties = this.devicePropertySerializer.convertModelListToJsonApiRelationshipObject(device.properties)
      const customfields = this.customTextFieldSerializer.convertModelListToJsonApiRelationshipObject(device.customFields)
      const attachments = this.attachmentSerializer.convertModelListToJsonApiRelationshipObject(device.attachments)
      const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(device.contacts)
      const parameters = this.parameterSerializer.convertModelListToJsonApiRelationshipObject(device.parameters)
      const images = this.imageSerializer.convertModelListToJsonApiRelationshipObject(device.images)
      data.relationships = {
        ...contacts,
        ...properties,
        ...attachments,
        ...customfields,
        ...parameters,
        ...images
      }
    }

    if (device.id !== null) {
      data.id = device.id
    }

    return data
  }
}

export const deviceWithMetaToDeviceByThrowingErrorOnMissing = (deviceWithMeta: { missing: { contacts: { ids: any[] } }; device: Device }): Device => {
  const device = deviceWithMeta.device

  if (deviceWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return device
}

export const deviceWithMetaToDeviceByAddingDummyObjects = (deviceWithMeta: { missing: { contacts: { ids: string[] } }; device: Device }): Device => {
  const device = deviceWithMeta.device

  for (const missingContactId of deviceWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    device.contacts.push(contact)
  }

  return device
}

export const deviceWithMetaToDeviceThrowingNoErrorOnMissing = (deviceWithMeta: { missing: { contacts: { ids: any[] } }; device: Device }): Device => {
  const device = deviceWithMeta.device
  return device
}

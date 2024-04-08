/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { SiteSerializer } from '@/serializers/jsonapi/SiteSerializer'
import { ParameterSerializer, ParameterEntityType } from '@/serializers/jsonapi/ParameterSerializer'
import { ConfigurationImageSerializer } from '@/serializers/jsonapi/ImageSerializer'

import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'

export interface IConfigurationMissingData {
  contacts: IMissingContactData
}

export interface IConfigurationWithMeta {
  configuration: Configuration
  missing: IConfigurationMissingData
}

export class ConfigurationSerializer {
  private imageSerializer: ConfigurationImageSerializer = new ConfigurationImageSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private siteSerializer: SiteSerializer = new SiteSerializer()
  private parameterSerializer: ParameterSerializer = new ParameterSerializer(ParameterEntityType.CONFIGURATION)
  private _permissionGroups: PermissionGroup[] = []

  set permissionGroups (groups: PermissionGroup[]) {
    this._permissionGroups = groups
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): IConfigurationWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): IConfigurationWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): IConfigurationWithMeta {
    const configuration = new Configuration()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    configuration.id = jsonApiData.id.toString()
    if (attributes) {
      configuration.label = attributes.label || ''
      configuration.description = attributes.description || ''
      configuration.project = attributes.project || ''
      configuration.campaign = attributes.campaign || ''
      configuration.status = attributes.status || ''
      configuration.archived = attributes.archived || false
      configuration.persistentIdentifier = attributes.persistent_identifier || ''

      configuration.startDate = attributes.start_date ? DateTime.fromISO(attributes.start_date, { zone: 'UTC' }) : null
      configuration.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null

      configuration.createdAt = attributes.created_at ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      configuration.updatedAt = attributes.updated_at ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
      configuration.updateDescription = attributes.update_description || ''

      if (attributes.is_internal) {
        configuration.visibility = Visibility.Internal
      }
      if (attributes.is_public) {
        configuration.visibility = Visibility.Public
      }

      if (attributes.keywords) {
        configuration.keywords = [...attributes.keywords]
      }
    }

    const images = this.imageSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    configuration.images = images

    let missingDataForContactIds: string[] = []
    if (relationships) {
      const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
      configuration.contacts = contactsWithMissing.contacts
      missingDataForContactIds = contactsWithMissing.missing.ids
    }

    const allPossibleContacts: {[key: string]: Contact} = {}

    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'contact') {
          const contactId = includedEntry.id
          const contact = this.contactSerializer.convertJsonApiDataToModel(includedEntry)
          allPossibleContacts[contactId] = contact
        }
      }
    }

    if (relationships.site) {
      configuration.siteId = this.siteSerializer.convertJsonApiRelationshipToId(relationships.site)
    }

    configuration.parameters = this.parameterSerializer.convertJsonApiRelationshipsModelList(relationships, included)

    // just pick the contact from the relationships that is referenced by the created_by user
    if (relationships.created_by?.data && 'id' in relationships.created_by?.data) {
      const userId = (relationships.created_by.data as IJsonApiEntityWithoutDetails).id
      configuration.createdByUserId = userId
      const createdBy = this.contactSerializer.getContactFromIncludedByUserId(userId, included)
      if (createdBy) {
        configuration.createdBy = createdBy
      }
    }

    // just pick the contact from the relationships that is referenced by the updated_by user
    if (relationships.updated_by?.data && 'id' in relationships.updated_by?.data) {
      const userId = (relationships.updated_by.data as IJsonApiEntityWithoutDetails).id
      const updatedBy = this.contactSerializer.getContactFromIncludedByUserId(userId, included)
      if (updatedBy) {
        configuration.updatedBy = updatedBy
      }
    }

    if (attributes?.cfg_permission_group != null) {
      const id = attributes.cfg_permission_group
      let permissionGroup = this.permissionGroups.find(group => group.id === id)

      if (!permissionGroup) {
        permissionGroup = PermissionGroup.createFromObject({
          id
        })
      }
      configuration.permissionGroup = permissionGroup
    }

    return {
      configuration,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertModelToJsonApiData (configuration: Configuration): IJsonApiEntityWithOptionalId {
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(configuration.contacts)
    const sites = this.siteSerializer.convertIdToJsonApiRelationshipObject(configuration.siteId)
    const parameters = this.parameterSerializer.convertModelListToJsonApiRelationshipObject(configuration.parameters)
    const images = this.imageSerializer.convertModelListToJsonApiRelationshipObject(configuration.images)

    const result: IJsonApiEntityWithOptionalId = {
      attributes: {
        label: configuration.label,
        description: configuration.description,
        project: configuration.project,
        campaign: configuration.campaign,
        status: configuration.status,
        start_date: configuration.startDate != null ? configuration.startDate.setZone('UTC').toISO() : null,
        end_date: configuration.endDate != null ? configuration.endDate.setZone('UTC').toISO() : null,
        is_internal: configuration.isInternal,
        is_public: configuration.isPublic,
        cfg_permission_group: configuration.permissionGroup?.id,
        persistent_identifier: configuration.persistentIdentifier === '' ? null : configuration.persistentIdentifier,
        keywords: configuration.keywords
      },
      relationships: {
        ...contacts,
        ...sites,
        ...parameters,
        ...images
      },
      type: 'configuration'
    }
    if (configuration.id) {
      result.id = configuration.id
    }
    return result
  }
}

export const configurationWithMetaToConfigurationByThrowingErrorOnMissing = (configurationWithMeta: IConfigurationWithMeta): Configuration => {
  const configuration = configurationWithMeta.configuration
  if (configurationWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }
  return configuration
}
export const configurationWithMetaToConfigurationByThrowingNoErrorOnMissing = (configurationWithMeta: IConfigurationWithMeta): Configuration => {
  return configurationWithMeta.configuration
}

export const configurationWithMetaToConfigurationByAddingDummyObjects = (configurationWithMeta: IConfigurationWithMeta): Configuration => {
  const configuration = configurationWithMeta.configuration

  for (const missingContactId of configurationWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    configuration.contacts.push(contact)
  }
  return configuration
}

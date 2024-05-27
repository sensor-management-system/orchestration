/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { IAddress, ILatLng, Site } from '@/models/Site'
import { PermissionGroup } from '@/models/PermissionGroup'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalId,

  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiRelationshipsData, IJsonApiTypedEntityWithoutDetailsDataNullable
} from '@/serializers/jsonapi/JsonApiTypes'

import { SiteImageSerializer } from '@/serializers/jsonapi/ImageSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { Visibility } from '@/models/Visibility'

export interface ISiteMissingData {
  contacts: IMissingContactData
}

export interface ISiteWithMeta {
  site: Site
  missing: ISiteMissingData
}

export class SiteSerializer {
  private imageSerializer: SiteImageSerializer = new SiteImageSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private _permissionGroups: PermissionGroup[] = []

  set permissionGroups (groups: PermissionGroup[]) {
    this._permissionGroups = groups
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  convertGeomToWKT (geom: ILatLng[]) {
    if (geom.length > 2) {
      const closedGeom = [...geom, geom[0]]
      const coordinateString = closedGeom.map((x) => {
        return `${x.lng} ${x.lat}`
      }).join(',')
      const wktString = `POLYGON((${coordinateString}))`
      return wktString
    } else {
      return null
    }
  }

  convertWKTToGeom (wktString: string): ILatLng[] {
    if (wktString && wktString.startsWith('POLYGON')) {
      const coords = wktString.split('((')[1].split('))')[0].split(',')
      const latLngs = coords.map((coord) => {
        if (coord.startsWith(' ')) {
          coord = coord.substring(1)
        }
        return {
          lat: parseFloat(coord.split(' ')[1]),
          lng: parseFloat(coord.split(' ')[0])
        }
      })
      latLngs.pop()
      return latLngs
    } else {
      return []
    }
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): ISiteWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): ISiteWithMeta {
    const result: Site = new Site()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    result.id = jsonApiData.id.toString()

    if (attributes) {
      const address: IAddress = {
        street: attributes.street || '',
        streetNumber: attributes.street_number || '',
        city: attributes.city || '',
        zipCode: attributes.zip_code || '',
        country: attributes.country || '',
        building: attributes.building || '',
        room: attributes.room || ''
      }
      result.label = attributes.label || ''
      result.geometry = this.convertWKTToGeom(attributes.geometry)
      result.description = attributes.description || ''
      result.epsgCode = attributes.epsg_code || ''
      result.address = address
      result.siteTypeName = attributes.site_type_name || ''
      result.siteTypeUri = attributes.site_type_uri || ''
      result.siteUsageName = attributes.site_usage_name || ''
      result.siteUsageUri = attributes.site_usage_uri || ''
      result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
      result.updateDescription = attributes.update_description || ''
      result.website = attributes.website || ''

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

    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

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

    if (attributes?.keywords) {
      result.keywords = [...attributes.keywords]
    }

    if (attributes?.group_ids) {
      // look up the group in the provided permission group array. if it was
      // found, push the found group into the site's permissionGroups property
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
    if (relationships.outer_site?.data && 'id' in relationships.outer_site?.data) {
      result.outerSiteId = (relationships.outer_site.data as IJsonApiEntityWithoutDetails).id
    }

    return {
      site: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ISiteWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (site: Site, includeRelationships: boolean = false): IJsonApiEntityWithOptionalId {
    const geometry = this.convertGeomToWKT(site.geometry)

    const data: IJsonApiEntityWithOptionalId = {
      type: 'site',
      attributes: {
        label: site.label,
        description: site.description,
        geometry,
        epsg_code: site.epsgCode,
        is_internal: site.isInternal,
        is_public: site.isPublic,
        group_ids: site.permissionGroups.filter(i => i.id !== null).map(i => i.id),
        city: site.address.city,
        street: site.address.street,
        street_number: site.address.streetNumber,
        zip_code: site.address.zipCode,
        country: site.address.country,
        building: site.address.building,
        room: site.address.room,
        site_usage_name: site.siteUsageName,
        site_usage_uri: site.siteUsageUri,
        site_type_name: site.siteTypeName,
        site_type_uri: site.siteTypeUri,
        website: site.website,
        keywords: site.keywords

        // these properties are set by the db, so we wont send anything related here:
        // archived
        // createdAt
        // createdBy
        // modifiedAt
        // modifiedBy
        // updateDescription
      },
      relationships: {
        outer_site: {
          data: null
        }
      }
    }

    if (site.outerSiteId) {
      data.relationships!.outer_site.data = {
        id: site.outerSiteId,
        type: 'site'
      }
    }

    if (includeRelationships) {
      const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(site.contacts)
      const images = this.imageSerializer.convertModelListToJsonApiRelationshipObject(site.images)
      data.relationships = {
        ...contacts,
        ...images
      }
    }

    if (site.id !== '') {
      data.id = site.id
    }

    return data
  }

  convertIdToTupleWithIdAndType (id: string): IJsonApiEntityWithoutDetails |null {
    if (id) {
      return {
        id,
        type: 'site'
      }
    }

    return null
  }

  convertIdToJsonApiRelationshipObject (id: string): IJsonApiTypedEntityWithoutDetailsDataNullable {
    return {
      site: {
        data: this.convertIdToTupleWithIdAndType(id)
      }
    }
  }

  convertJsonApiRelationshipToId (relationship: IJsonApiRelationshipsData): string {
    if (relationship.data) {
      return (relationship.data as IJsonApiEntityWithoutDetails).id
    }
    return ''
  }
}

export const siteWithMetaToSiteByThrowingErrorOnMissing = (siteWithMeta: { missing: { contacts: { ids: any[] } }; site: Site }): Site => {
  const site = siteWithMeta.site

  if (siteWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return site
}

export const siteWithMetaToSiteByAddingDummyObjects = (siteWithMeta: { missing: { contacts: { ids: string[] } }; site: Site }): Site => {
  const site = siteWithMeta.site

  for (const missingContactId of siteWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    site.contacts.push(contact)
  }

  return site
}

export const siteWithMetaToSiteThrowingNoErrorOnMissing = (siteWithMeta: { missing: { contacts: { ids: any[] } }; site: Site }): Site => {
  const site = siteWithMeta.site
  return site
}

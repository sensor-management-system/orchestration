/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { SiteType } from '@/models/SiteType'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class SiteTypeSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): SiteType[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): SiteType {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const url = jsonApiData.links?.self || ''
    const definition = jsonApiData.attributes.definition
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''

    const siteUsageId = (jsonApiData.relationships && jsonApiData.relationships.site_usage && (jsonApiData.relationships.site_usage as IJsonApiEntityWithoutDetailsDataDict).data.id) || null

    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return SiteType.createFromObject({
      id,
      name,
      definition,
      provenance,
      provenanceUri,
      category,
      note,
      uri: url,
      globalProvenanceId,
      siteUsageId
    })
  }

  convertModelToJsonApiData (siteType: SiteType) {
    const attributes = {
      term: siteType.name,
      definition: siteType.definition,
      provenance: siteType.provenance,
      provenance_uri: siteType.provenanceUri,
      category: siteType.category,
      note: siteType.note
    }

    const relationships: any = {}

    if (siteType.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: siteType.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    if (siteType.siteUsageId) {
      relationships.site_usage = {
        data: {
          id: siteType.siteUsageId,
          type: 'SiteUsage'
        }
      }
    }

    const wrapper: any = {
      type: 'SiteType',
      attributes,
      relationships
    }

    if (siteType.id) {
      wrapper.id = siteType.id
    }

    return wrapper
  }
}

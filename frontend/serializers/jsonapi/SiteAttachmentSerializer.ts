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

import { Attachment, IAttachment } from '@/models/Attachment'
import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiRelationships,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

import { IAttachmentsAndMissing, IAttachmentSerializer, AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'

export class SiteAttachmentSerializer implements IAttachmentSerializer {
  // Delegate to a generalized serializer.
  private serializer = new AttachmentSerializer('site_attachment', 'site')

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Attachment {
    return this.serializer.convertJsonApiObjectToModel(jsonApiObject)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): Attachment {
    return this.serializer.convertJsonApiDataToModel(jsonApiData)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Attachment[] {
    return this.serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IAttachmentsAndMissing {
    return this.serializer.convertJsonApiRelationshipsModelList(relationships, included)
  }

  convertJsonApiRelationshipsSingleModel (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Attachment | null {
    return this.serializer.convertJsonApiRelationshipsSingleModel(relationships, included)
  }

  convertModelListToJsonApiRelationshipObject (attachments: IAttachment[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    return this.serializer.convertModelListToJsonApiRelationshipObject(attachments)
  }

  convertModelListToTupleListWithIdAndType (attachments: IAttachment[]): IJsonApiEntityWithoutDetails[] {
    return this.serializer.convertModelListToTupleListWithIdAndType(attachments)
  }

  convertModelToJsonApiData (attachment: Attachment, siteId: string): IJsonApiEntityWithOptionalId {
    return this.serializer.convertModelToJsonApiData(attachment, siteId)
  }
}

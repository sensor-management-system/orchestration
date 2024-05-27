/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'
import { ConfigurationAttachmentSerializer } from '@/serializers/jsonapi/ConfigurationAttachmentSerializer'
import { SiteAttachmentSerializer } from '@/serializers/jsonapi/SiteAttachmentSerializer'
import { IAttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'
import
{
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiTypedEntityWithoutDetailsDataDictList
}
  from
  '@/serializers/jsonapi/JsonApiTypes'
import { Image, IImage } from '@/models/Image'

export interface IImageSerializer {
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Image[]
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Image
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): Image

  attachmentSerializer: IAttachmentSerializer
  getImageTypeName (): string
  getAttachmentTypeName (): string
  convertModelToJsonApiData (entityImage: IImage, relationId: string): IJsonApiEntityWithOptionalId
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Image[]

}

abstract class AbstractImageSerializer implements IImageSerializer {
  abstract get attachmentSerializer (): IAttachmentSerializer
  abstract getRelationTypeName (): string

  getImageTypeName (): string {
    return this.getRelationTypeName() + '_image'
  }

  getAttachmentTypeName (): string {
    return this.getRelationTypeName() + '_attachment'
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Image {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): Image {
    const newEntry = new Image()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.orderIndex = attributes.order_index
    }

    // serializer expects relationship named '[entity]_attachment' so we copy and rename the included attachment
    relationships[this.getAttachmentTypeName()] = relationships.attachment
    newEntry.attachment = this.attachmentSerializer.convertJsonApiRelationshipsSingleModel(relationships, included)

    return newEntry
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Image[] {
    const entityType = this.getImageTypeName()

    const imageIds = []
    const typePlural = entityType + 's'
    if (relationships[typePlural]) {
      const imageObject = relationships[typePlural]
      if (imageObject.data && (imageObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipAttachmentData of (imageObject.data as IJsonApiEntityWithoutDetails[])) {
          const imageId = relationShipAttachmentData.id
          imageIds.push(imageId)
        }
      }
    }

    const possibleImages: { [key: string]: Image } = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === entityType) {
          const imageId = includedEntry.id
          if (imageIds.includes(imageId)) {
            const image = this.convertJsonApiDataToModel(includedEntry, included)
            possibleImages[imageId] = image
          }
        }
      }
    }

    const images = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === entityType) {
          const image = this.convertJsonApiDataToModel(includedEntry, included)
          images.push(image)
        }
      }
    }

    const orderedImages = images.sort((a, b) => a.orderIndex < b.orderIndex ? -1 : 1)

    return orderedImages
  }

  convertModelToJsonApiData (entityImage: IImage, relationId: string): IJsonApiEntityWithOptionalId {
    const entityType = this.getImageTypeName()
    const relationType = this.getRelationTypeName()
    const attachmentType = this.getAttachmentTypeName()

    const data: IJsonApiEntityWithOptionalId = {
      type: entityType,
      attributes: {
        order_index: entityImage.orderIndex
      },
      relationships: {
        [relationType]: {
          data: {
            type: relationType,
            id: relationId || ''
          }
        },
        attachment: {
          data: {
            type: attachmentType,
            id: entityImage.attachment!.id || ''
          }
        }
      }
    }

    if (entityImage.id) {
      data.id = entityImage.id
    }

    return data
  }

  convertModelListToJsonApiRelationshipObject (images: IImage[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    const entityType = this.getImageTypeName() + 's'
    return {
      [entityType]: {
        data: this.convertModelListToTupleListWithIdAndType(images)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (images: IImage[]): IJsonApiEntityWithoutDetails[] {
    const entityType = this.getImageTypeName()
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const image of images) {
      if (image.id !== null) {
        result.push({
          id: image.id,
          type: entityType
        })
      }
    }
    return result
  }
}

export class DeviceImageSerializer extends AbstractImageSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceAttachmentSerializer()
  }

  getRelationTypeName (): string {
    return 'device'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class PlatformImageSerializer extends AbstractImageSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new PlatformAttachmentSerializer()
  }

  getRelationTypeName (): string {
    return 'platform'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class ConfigurationImageSerializer extends AbstractImageSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new ConfigurationAttachmentSerializer()
  }

  getRelationTypeName (): string {
    return 'configuration'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class SiteImageSerializer extends AbstractImageSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new SiteAttachmentSerializer()
  }

  getRelationTypeName (): string {
    return 'site'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}

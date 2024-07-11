/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Image } from '@/models/Image'
import { IImageSerializer, ConfigurationImageSerializer, DeviceImageSerializer, PlatformImageSerializer, SiteImageSerializer } from '@/serializers/jsonapi/ImageSerializer'
import { IJsonApiEntityWithoutDetails, IJsonApiLinkDict } from '@/serializers/jsonapi/JsonApiTypes'
import { capitalize } from '@/utils/stringHelpers'

const entityTypesThatHaveImages = ['device', 'platform', 'configuration', 'site']
entityTypesThatHaveImages.forEach(type => executeTestsForType(type))

function executeTestsForType (type: string) {
  if (!entityTypesThatHaveImages.includes(type)) { return }

  const typePlural = type + 's'
  const imageType = type + '_image'
  const imageTypePlural = imageType + 's'
  const attachmentType = type + '_attachment'
  const imageSerializerType = capitalize('')
  const imageApiPath = `${type}-images`

  let imageSerializer: IImageSerializer
  switch (type) {
    case 'device': imageSerializer = new DeviceImageSerializer(); break
    case 'platform': imageSerializer = new PlatformImageSerializer(); break
    case 'configuration': imageSerializer = new ConfigurationImageSerializer(); break
    case 'site': imageSerializer = new SiteImageSerializer(); break
  }

  describe(imageSerializerType, () => {
    describe('#convertJsonApiRelationshipsModelList', () => {
      it('should sort images by orderIndex ascending', () => {
        const relatedImages = getListOfRelatedImages(5)
        const models = imageSerializer.convertJsonApiRelationshipsModelList(relatedImages.relationships, relatedImages.included)

        expect(models.length).toEqual(5)

        const orderIndices = models.map(i => i.orderIndex)
        expect(orderIndices.sort((a, b) => a < b ? -1 : 1)).toEqual(orderIndices)
      })

      it(`should create an ordered list of related ${imageTypePlural}`, () => {
        const relatedImages = getListOfRelatedImages(5)
        const models = imageSerializer.convertJsonApiRelationshipsModelList(relatedImages.relationships, relatedImages.included)

        expect(models.length).toEqual(5)
        for (const image of models) {
          const id = image.id
          const relationshipModel = relatedImages.included.find(i => i.id === id && i.type === imageType)
          expect(image.orderIndex).toEqual(relationshipModel?.attributes.order_index)
          expect(image.attachment?.id).toEqual(relationshipModel?.relationships.attachment?.data.id)
        }
      })
    })

    describe('#convertJsonApiObjectToModel', () => {
      it('should create the model from the json:api object', () => {
        const relatedAttachmentData = {
          id: '1',
          type: attachmentType,
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            is_upload: false,
            created_at: null
          },
          relationships: {}
        }

        const data = {
          data: {
            id: '123',
            type: imageType,
            attributes: {
              order_index: 1
            },
            relationships: {
              attachment: {
                links: {
                  related: '/backend/api/v1/device-attachments/1'
                },
                data: {
                  type: attachmentType,
                  id: '1'
                }
              }
            }
          },
          included: [relatedAttachmentData]
        }

        const model = imageSerializer.convertJsonApiObjectToModel(data)

        expect(model.id).toEqual('123')
        expect(model.orderIndex).toEqual(1)
        expect(model.attachment?.url).toEqual('https://www.gfz-potsdam.de')
        expect(model.attachment?.label).toEqual('GFZ Homepage')
      })
    })

    describe('#convertModelToJsonApiData', () => {
      it('should convert an image to a json:api payload', () => {
        const attachment = {
          id: '123',
          url: 'https://www.ufz.de',
          label: 'UFZ Homepage',
          description: 'The UFZ homepage',
          isUpload: false,
          createdAt: null
        }
        const image = Image.createFromObject({
          id: '123',
          orderIndex: 1,
          attachment
        })
        const entityId = '456'

        const jsonApiPayload = imageSerializer.convertModelToJsonApiData(image, entityId)

        expect(jsonApiPayload).toHaveProperty('id')
        expect(jsonApiPayload.id).toEqual('123')
        expect(jsonApiPayload).toHaveProperty('type')
        expect(jsonApiPayload.type).toEqual(imageType)
        expect(jsonApiPayload).toHaveProperty('attributes')
        expect(jsonApiPayload.attributes).toHaveProperty('order_index')
        expect(jsonApiPayload.attributes.order_index).toEqual(1)
        expect(jsonApiPayload).toHaveProperty('relationships')
        expect(jsonApiPayload.relationships).toHaveProperty('attachment')
        expect(jsonApiPayload.relationships?.attachment).toHaveProperty('data')
        const attachmentData: any = jsonApiPayload.relationships?.attachment.data
        expect(attachmentData).toHaveProperty('id')
        expect(attachmentData.id).toEqual('123')
        expect(attachmentData).toHaveProperty('type')
        expect(attachmentData.type).toEqual(attachmentType)
      })
      it('should also work if we don\'t have an id yet', () => {
        const attachment = {
          id: '123',
          url: 'https://www.ufz.de',
          label: 'UFZ Homepage',
          description: 'The UFZ homepage',
          isUpload: false,
          createdAt: null
        }
        const image = Image.createFromObject({
          id: '',
          orderIndex: 1,
          attachment
        })
        const deviceId = '456'

        const jsonApiPayload = imageSerializer.convertModelToJsonApiData(image, deviceId)

        expect(jsonApiPayload).not.toHaveProperty('id')
        expect(jsonApiPayload).toHaveProperty('type')
        expect(jsonApiPayload.type).toEqual(imageType)
        expect(jsonApiPayload).toHaveProperty('attributes')
        expect(jsonApiPayload.attributes).toHaveProperty('order_index')
        expect(jsonApiPayload.attributes.order_index).toEqual(1)
        expect(jsonApiPayload).toHaveProperty('relationships')
        expect(jsonApiPayload.relationships).toHaveProperty('attachment')
        expect(jsonApiPayload.relationships?.attachment).toHaveProperty('data')
        const attachmentData: any = jsonApiPayload.relationships?.attachment.data
        expect(attachmentData).toHaveProperty('id')
        expect(attachmentData.id).toEqual('123')
        expect(attachmentData).toHaveProperty('type')
        expect(attachmentData.type).toEqual(attachmentType)
      })
    })
  })

  function getListOfRelatedImages (amount: number) {
    const relationships: {[idx: string]: {links: IJsonApiLinkDict, data: IJsonApiEntityWithoutDetails[]}} = {}
    relationships[imageTypePlural] = { links: {}, data: [] }
    const included = []

    let i = amount
    while (i--) {
      // include image
      included.push({
        id: i.toString(),
        type: imageType,
        attributes: {
          order_index: amount - i
        },
        relationships: {
          attachment: {
            links: {
              related: `/backend/api/v1/${imageApiPath}/${i}`
            },
            data: { type: 'device_attachment', id: i.toString() }
          },
          device: {
            links: {
              related: `/backend/api/v1/${typePlural}/${i}`
            },
            data: { type: 'device', id: i.toString() }
          }
        },
        links: {
          self: `/backend/api/v1/${type}-attachments/${i}`
        }
      })

      // include attachment for image
      included.push({
        id: i.toString(),
        type: attachmentType,
        attributes: {
          id: i.toString()
        },
        relationships: {
          [typePlural + 's']: {
            links: {
              related: `/backend/api/v1/${imageApiPath}/${i}`
            },
            data: { type: typePlural, id: i.toString() }
          }
        },
        links: {
          self: `/backend/api/v1/${imageApiPath}/${i}`
        }
      })

      relationships[imageTypePlural].data.push({ type: imageType, id: i.toString() })
    }

    return { relationships, included }
  }
}

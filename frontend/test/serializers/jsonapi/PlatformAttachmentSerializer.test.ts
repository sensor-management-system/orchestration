/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2023
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
import { Attachment } from '@/models/Attachment'
import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'

describe('PlatformAttachmentSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should create a list of attachments', () => {
      const data = {
        data: [{
          id: '123',
          type: 'platform_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            is_upload: false,
            created_at: null
          },
          relationships: {}
        }, {
          id: '456',
          type: 'platform_attachment',
          attributes: {
            url: 'https://www.ufz.de',
            label: 'UFZ Homepage',
            is_upload: true,
            created_at: '2022-08-16T12:00:00+00:00'
          },
          relationships: {}
        }],
        included: []
      }
      const serializer = new PlatformAttachmentSerializer()
      const models = serializer.convertJsonApiObjectListToModelList(data)

      expect(models.length).toEqual(2)
      expect(models[0].id).toEqual('123')
      expect(models[0].url).toEqual('https://www.gfz-potsdam.de')
      expect(models[0].label).toEqual('GFZ Homepage')
      expect(models[0].isUpload).not.toBeTruthy()
      expect(models[0].createdAt).toBeNull()
      expect(models[1].id).toEqual('456')
      expect(models[1].url).toEqual('https://www.ufz.de')
      expect(models[1].label).toEqual('UFZ Homepage')
      expect(models[1].isUpload).toBeTruthy()
      expect(models[1].createdAt).toEqual(DateTime.utc(2022, 8, 16, 12, 0, 0))
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should create the model from the json:api object', () => {
      const data = {
        data: {
          id: '123',
          type: 'platform_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            is_upload: true
          },
          relationships: {}
        },
        included: []
      }

      const serializer = new PlatformAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('https://www.gfz-potsdam.de')
      expect(model.label).toEqual('GFZ Homepage')
      expect(model.isUpload).toBeTruthy()
    })
    it('should also fill the attributes with empty strings if missing', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_attachment',
          attributes: {},
          relationships: {}
        },
        included: []
      }

      const serializer = new PlatformAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('')
      expect(model.label).toEqual('')
      expect(model.isUpload).not.toBeTruthy()
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert an attachment to a json:api payload', () => {
      const attachment = Attachment.createFromObject({
        id: '123',
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        isUpload: false,
        createdAt: null
      })
      const serializer = new PlatformAttachmentSerializer()
      const platformId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, platformId)

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('platform_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('platform')
      expect(jsonApiPayload.relationships?.platform).toHaveProperty('data')
      const platformData: any = jsonApiPayload.relationships?.platform.data
      expect(platformData).toHaveProperty('id')
      expect(platformData.id).toEqual('456')
      expect(platformData).toHaveProperty('type')
      expect(platformData.type).toEqual('platform')
    })
    it('should also work if we don\'t have an id yet', () => {
      const attachment = Attachment.createFromObject({
        id: null,
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        isUpload: true,
        createdAt: DateTime.utc(2022, 8, 16, 12, 0, 0)
      })
      const serializer = new PlatformAttachmentSerializer()
      const platformId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, platformId)

      expect(jsonApiPayload).not.toHaveProperty('id')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('platform_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('platform')
      expect(jsonApiPayload.relationships?.platform).toHaveProperty('data')
      const platformData: any = jsonApiPayload.relationships?.platform.data
      expect(platformData).toHaveProperty('id')
      expect(platformData.id).toEqual('456')
      expect(platformData).toHaveProperty('type')
      expect(platformData.type).toEqual('platform')
    })
  })
})

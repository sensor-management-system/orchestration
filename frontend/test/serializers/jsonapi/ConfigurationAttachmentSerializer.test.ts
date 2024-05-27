/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { ConfigurationAttachmentSerializer } from '@/serializers/jsonapi/ConfigurationAttachmentSerializer'

describe('ConfigurationAttachmentSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should create a list of attachments', () => {
      const data = {
        data: [{
          id: '123',
          type: 'configuration_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            description: 'The GFZ homepage',
            is_upload: false,
            created_at: null
          },
          relationships: {}
        }, {
          id: '456',
          type: 'configuration_attachment',
          attributes: {
            url: 'https://www.ufz.de',
            label: 'UFZ Homepage',
            is_upload: true,
            created_at: '2024-02-28T23:59:59+00:00'
          },
          relationships: {}
        }],
        included: []
      }
      const serializer = new ConfigurationAttachmentSerializer()
      const models = serializer.convertJsonApiObjectListToModelList(data)

      expect(models.length).toEqual(2)
      expect(models[0].id).toEqual('123')
      expect(models[0].url).toEqual('https://www.gfz-potsdam.de')
      expect(models[0].label).toEqual('GFZ Homepage')
      expect(models[0].description).toEqual('The GFZ homepage')
      expect(models[0].isUpload).not.toBeTruthy()
      expect(models[0].createdAt).toBeNull()

      expect(models[1].id).toEqual('456')
      expect(models[1].url).toEqual('https://www.ufz.de')
      expect(models[1].label).toEqual('UFZ Homepage')
      expect(models[1].description).toEqual('')
      expect(models[1].isUpload).toBeTruthy()
      expect(models[1].createdAt).toEqual(DateTime.utc(2024, 2, 28, 23, 59, 59))
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should create the model from the json:api object', () => {
      const data = {
        data: {
          id: '123',
          type: 'configuration_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            description: 'gfz',
            is_upload: true
          },
          relationships: {}
        },
        included: []
      }

      const serializer = new ConfigurationAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('https://www.gfz-potsdam.de')
      expect(model.label).toEqual('GFZ Homepage')
      expect(model.description).toEqual('gfz')
      expect(model.isUpload).toBeTruthy()
    })
    it('should also fill the attributes with empty strings if missing', () => {
      const data = {
        data: {
          id: '123',
          type: 'configuration_attachment',
          attributes: {},
          relationships: {}
        },
        included: []
      }

      const serializer = new ConfigurationAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('')
      expect(model.label).toEqual('')
      expect(model.description).toEqual('')
      expect(model.isUpload).not.toBeTruthy()
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert an attachment to a json:api payload', () => {
      const attachment = Attachment.createFromObject({
        id: '123',
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        description: 'The UFZ homepage',
        isUpload: false,
        createdAt: null
      })
      const serializer = new ConfigurationAttachmentSerializer()
      const configurationId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, configurationId)

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('configuration_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('The UFZ homepage')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('configuration')
      expect(jsonApiPayload.relationships?.configuration).toHaveProperty('data')
      const configurationData: any = jsonApiPayload.relationships?.configuration.data
      expect(configurationData).toHaveProperty('id')
      expect(configurationData.id).toEqual('456')
      expect(configurationData).toHaveProperty('type')
      expect(configurationData.type).toEqual('configuration')
    })
    it('should also work if we don\'t have an id yet', () => {
      const attachment = Attachment.createFromObject({
        id: null,
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        description: 'ufz',
        isUpload: true,
        createdAt: null
      })
      const serializer = new ConfigurationAttachmentSerializer()
      const configurationId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, configurationId)

      expect(jsonApiPayload).not.toHaveProperty('id')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('configuration_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('ufz')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('configuration')
      expect(jsonApiPayload.relationships?.configuration).toHaveProperty('data')
      const configurationData: any = jsonApiPayload.relationships?.configuration.data
      expect(configurationData).toHaveProperty('id')
      expect(configurationData.id).toEqual('456')
      expect(configurationData).toHaveProperty('type')
      expect(configurationData.type).toEqual('configuration')
    })
  })
})

/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { ExportControlAttachment } from '@/models/ExportControlAttachment'
import { ExportControlAttachmentSerializer } from '@/serializers/jsonapi/ExportControlAttachmentSerializer'

describe('ExportControlAttachmentSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should create a list of attachments', () => {
      const data = {
        data: [{
          id: '123',
          type: 'export_control_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            is_upload: false,
            is_export_control_only: false,
            created_at: null
          },
          relationships: {}
        }, {
          id: '456',
          type: 'export_control_attachment',
          attributes: {
            url: 'https://www.ufz.de',
            label: 'UFZ Homepage',
            is_upload: true,
            is_export_control_only: true,
            created_at: '2023-08-16T12:00:00+00:00'
          },
          relationships: {}
        }],
        included: []
      }
      const serializer = new ExportControlAttachmentSerializer()
      const models = serializer.convertJsonApiObjectListToModelList(data)

      expect(models.length).toEqual(2)
      expect(models[0].id).toEqual('123')
      expect(models[0].url).toEqual('https://www.gfz-potsdam.de')
      expect(models[0].label).toEqual('GFZ Homepage')
      expect(models[0].isUpload).not.toBeTruthy()
      expect(models[0].isExportControlOnly).not.toBeTruthy()
      expect(models[0].createdAt).toBeNull()

      expect(models[1].id).toEqual('456')
      expect(models[1].url).toEqual('https://www.ufz.de')
      expect(models[1].label).toEqual('UFZ Homepage')
      expect(models[1].isUpload).toBeTruthy()
      expect(models[1].isExportControlOnly).toBeTruthy()
      expect(models[1].createdAt).toEqual(DateTime.utc(2023, 8, 16, 12, 0, 0))
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should create the model from the json:api object', () => {
      const data = {
        data: {
          id: '123',
          type: 'export_control_attachment',
          attributes: {
            url: 'https://www.gfz-potsdam.de',
            label: 'GFZ Homepage',
            is_upload: true,
            is_export_control_only: true
          },
          relationships: {}
        },
        included: []
      }

      const serializer = new ExportControlAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('https://www.gfz-potsdam.de')
      expect(model.label).toEqual('GFZ Homepage')
      expect(model.isUpload).toBeTruthy()
      expect(model.isExportControlOnly).toBeTruthy()
    })
    it('should also fill the attributes with empty strings if missing', () => {
      const data = {
        data: {
          id: '123',
          type: 'export_control_attachment',
          attributes: {},
          relationships: {}
        },
        included: []
      }

      const serializer = new ExportControlAttachmentSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.url).toEqual('')
      expect(model.label).toEqual('')
      expect(model.isUpload).not.toBeTruthy()
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert an attachment to a json:api payload', () => {
      const attachment = ExportControlAttachment.createFromObject({
        id: '123',
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        description: 'The UFZ homepage',
        isUpload: false,
        isExportControlOnly: true,
        createdAt: null
      })
      const serializer = new ExportControlAttachmentSerializer()
      const manufacturerModelId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, manufacturerModelId)

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('export_control_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('The UFZ homepage')
      expect(jsonApiPayload.attributes).toHaveProperty('is_export_control_only', true)
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('manufacturer_model')
      expect(jsonApiPayload.relationships?.manufacturer_model).toHaveProperty('data')
      const manufacturerModelData: any = jsonApiPayload.relationships?.manufacturer_model.data
      expect(manufacturerModelData).toHaveProperty('id')
      expect(manufacturerModelData.id).toEqual('456')
      expect(manufacturerModelData).toHaveProperty('type')
      expect(manufacturerModelData.type).toEqual('manufacturer_model')
    })
    it('should also work if we don\'t have an id yet', () => {
      const attachment = ExportControlAttachment.createFromObject({
        id: null,
        url: 'https://www.ufz.de',
        label: 'UFZ Homepage',
        isUpload: true,
        isExportControlOnly: true,
        description: 'ufz',
        createdAt: null
      })
      const serializer = new ExportControlAttachmentSerializer()
      const manufacturerModelId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(attachment, manufacturerModelId)

      expect(jsonApiPayload).not.toHaveProperty('id')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('export_control_attachment')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('url')
      expect(jsonApiPayload.attributes.url).toEqual('https://www.ufz.de')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('UFZ Homepage')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('ufz')
      expect(jsonApiPayload.attributes).toHaveProperty('is_export_control_only', true)
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('manufacturer_model')
      expect(jsonApiPayload.relationships?.manufacturer_model).toHaveProperty('data')
      const manufacturerModelData: any = jsonApiPayload.relationships?.manufacturer_model.data
      expect(manufacturerModelData).toHaveProperty('id')
      expect(manufacturerModelData.id).toEqual('456')
      expect(manufacturerModelData).toHaveProperty('type')
      expect(manufacturerModelData.type).toEqual('manufacturer_model')
    })
  })
})

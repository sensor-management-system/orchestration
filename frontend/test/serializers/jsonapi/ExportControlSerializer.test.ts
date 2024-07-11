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
import { ExportControl } from '@/models/ExportControl'
import { ExportControlSerializer } from '@/serializers/jsonapi/ExportControlSerializer'

describe('ExportControlSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should transform a mostly empty export control data object', () => {
      const model = ExportControl.createFromObject({
        id: '',
        dualUse: null,
        exportControlClassificationNumber: '',
        customsTariffNumber: '',
        additionalInformation: '',
        internalNote: '',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null,
        updatedByUserId: null,
        manufacturerModelId: null
      })

      const serializer = new ExportControlSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(model)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData).toHaveProperty('type', 'export_control')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('dual_use', null)
      expect(attributes).toHaveProperty('export_control_classification_number', '')
      expect(attributes).toHaveProperty('customs_tariff_number', '')
      expect(attributes).toHaveProperty('additional_information', '')
      expect(attributes).toHaveProperty('internal_note', '')

      expect(jsonApiData).toHaveProperty('relationships')
      const relationships = jsonApiData.relationships
      expect(relationships).toHaveProperty('manufacturer_model', {
        data: null
      })
    })
    it('should transform a filled export control data object', () => {
      const model = ExportControl.createFromObject({
        id: '123',
        dualUse: true,
        exportControlClassificationNumber: '999',
        customsTariffNumber: '777',
        additionalInformation: 'DANGEROUS',
        internalNote: 'very dangerous',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null,
        updatedByUserId: null,
        manufacturerModelId: '567'
      })

      const serializer = new ExportControlSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(model)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('id', '123')
      expect(jsonApiData).toHaveProperty('type', 'export_control')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('dual_use', true)
      expect(attributes).toHaveProperty('export_control_classification_number', '999')
      expect(attributes).toHaveProperty('customs_tariff_number', '777')
      expect(attributes).toHaveProperty('additional_information', 'DANGEROUS')
      expect(attributes).toHaveProperty('internal_note', 'very dangerous')

      expect(jsonApiData).toHaveProperty('relationships')
      const relationships = jsonApiData.relationships
      expect(relationships).toHaveProperty('manufacturer_model', {
        data: {
          type: 'manufacturer_model', id: '567'
        }
      })
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should create an empty export control data object', () => {
      const jsonApiObject = {
        data: {
          id: '',
          type: 'export_control',
          attributes: {
          },
          relationships: {
            manufacturer_model: {
              data: null
            }
          }
        }
      }

      const serializer = new ExportControlSerializer()
      const model = serializer.convertJsonApiObjectToModel(jsonApiObject)

      const expectedModel = ExportControl.createFromObject({
        id: '',
        dualUse: null,
        exportControlClassificationNumber: '',
        customsTariffNumber: '',
        additionalInformation: '',
        internalNote: '',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null,
        updatedByUserId: null,
        manufacturerModelId: null
      })
      expect(model).toStrictEqual(expectedModel)
    })
    it('should create a filled export control data object', () => {
      const jsonApiObject = {
        data: {
          id: '123',
          type: 'export_control',
          attributes: {
            dual_use: true,
            export_control_classification_number: '456',
            customs_tariff_number: '789',
            additional_information: 'careful',
            internal_note: 'not sure',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            updated_at: '2021-08-28T13:00:46.295058+00:00'
          },
          relationships: {
            manufacturer_model: {
              data: {
                type: 'manufacturer_model',
                id: '999'
              }
            },
            created_by: {
              data: {
                type: 'user',
                id: '111'
              }
            },
            updated_by: {
              data: {
                type: 'user',
                id: '222'
              }
            }
          }
        }
      }

      const serializer = new ExportControlSerializer()
      const model = serializer.convertJsonApiObjectToModel(jsonApiObject)

      const expectedModel = ExportControl.createFromObject({
        id: '123',
        dualUse: true,
        exportControlClassificationNumber: '456',
        customsTariffNumber: '789',
        additionalInformation: 'careful',
        internalNote: 'not sure',
        createdAt: DateTime.utc(2020, 8, 28, 13, 0, 46, 295),
        updatedAt: DateTime.utc(2021, 8, 28, 13, 0, 46, 295),
        createdByUserId: '111',
        updatedByUserId: '222',
        manufacturerModelId: '999'
      })
      expect(model).toStrictEqual(expectedModel)
    })
  })
})

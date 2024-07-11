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
import { ManufacturerModel } from '@/models/ManufacturerModel'
import { ManufacturerModelSerializer } from '@/serializers/jsonapi/ManufacturerModelSerializer'

describe('ManufacturerModelSerializer', () => {
  describe('#convertJsonApiObjectToModel', () => {
    it('should transform the payload without export control information', () => {
      const jsonApiObject = {
        data: {
          id: '123',
          type: 'manufacturer_model',
          attributes: {
            manufacturer_name: 'TRUEBENER GmbH',
            model: 'SMT 100',
            external_system_name: null,
            external_system_url: null
          }
        }
      }
      const serializer = new ManufacturerModelSerializer()

      const model = serializer.convertJsonApiObjectToModel(jsonApiObject)

      const expectedModel = ManufacturerModel.createFromObject({
        id: '123',
        manufacturerName: 'TRUEBENER GmbH',
        model: 'SMT 100',
        externalSystemName: '',
        externalSystemUrl: '',
        exportControl: null
      })

      expect(model).toStrictEqual(expectedModel)
    })
    it('should handle included export control information', () => {
      const jsonApiObject = {
        data: {
          id: '123',
          type: 'manufacturer_model',
          attributes: {
            manufacturer_name: 'TRUEBENER GmbH',
            model: 'SMT 100',
            external_system_name: 'Hydro Equipment',
            external_system_url: 'https://hydro.gfz-potsdam.de/fictonal/system/SMT100'
          },
          relationships: {
            export_control: {
              data: {
                id: '124',
                type: 'export_control'
              }
            }
          }
        },
        included: [
          {
            id: '124',
            type: 'export_control',
            attributes: {
              dual_use: false,
              export_control_classification_number: '',
              customs_tariff_number: '',
              additional_information: 'Nothing to be worried about',
              internal_note: 'Maybe something to be worried about...',
              created_at: '2020-08-28T13:00:46.295058+00:00',
              updated_at: '2021-08-28T13:00:46.295058+00:00'
            },
            relationships: {
              manufacturer_model: {
                data: {
                  id: '123',
                  type: 'manufacturer_model'
                }
              },
              created_by: {
                data: {
                  id: '125',
                  type: 'user'
                }
              },
              updated_by: {
                data: {
                  id: '126',
                  type: 'user'
                }
              }
            }
          }
        ]
      }
      const serializer = new ManufacturerModelSerializer()

      const model = serializer.convertJsonApiObjectToModel(jsonApiObject)

      const expectedModel = ManufacturerModel.createFromObject({
        id: '123',
        manufacturerName: 'TRUEBENER GmbH',
        model: 'SMT 100',
        externalSystemName: 'Hydro Equipment',
        externalSystemUrl: 'https://hydro.gfz-potsdam.de/fictonal/system/SMT100',
        exportControl: ExportControl.createFromObject({
          id: '124',
          dualUse: false,
          exportControlClassificationNumber: '',
          customsTariffNumber: '',
          additionalInformation: 'Nothing to be worried about',
          internalNote: 'Maybe something to be worried about...',
          createdAt: DateTime.utc(2020, 8, 28, 13, 0, 46, 295),
          updatedAt: DateTime.utc(2021, 8, 28, 13, 0, 46, 295),
          createdByUserId: '125',
          updatedByUserId: '126',
          manufacturerModelId: '123'
        })
      })

      expect(model).toStrictEqual(expectedModel)
    })
  })
})

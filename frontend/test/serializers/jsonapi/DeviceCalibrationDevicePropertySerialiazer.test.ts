/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DeviceProperty } from '@/models/DeviceProperty'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'
import { DeviceCalibrationDevicePropertySerializer } from '@/serializers/jsonapi/DeviceCalibrationDevicePropertySerializer'

describe('DeviceCalibrationDevicePropertySerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should return a json api payload that can be saved on the server later', () => {
      const measuredQuantity1 = DeviceProperty.createFromObject({
        id: '111',
        label: 'MQ 1',
        compartmentName: 'C1',
        compartmentUri: 'C/1',
        samplingMediaName: 'S1',
        samplingMediaUri: 'S/1',
        propertyName: 'P1',
        propertyUri: 'P/1',
        unitName: 'U1',
        unitUri: 'U/1',
        failureValue: -999,
        accuracy: 0.1,
        accuracyUnitUri: 'http://foo/unit/2',
        accuracyUnitName: 'cm',
        measuringRange: {
          min: -1,
          max: 1
        },
        resolution: 0.5,
        resolutionUnitName: 'RU1',
        resolutionUnitUri: 'RU/1',
        aggregationTypeUri: 'http://foo/aggregationtypes/1',
        aggregationTypeName: 'Average',
        description: 'desc'
      })
      const actionId = '2'

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_property_calibration',
        attributes: {},
        relationships: {
          device_property: {
            data: {
              type: 'device_property',
              id: '111'
            }
          },
          calibration_action: {
            data: {
              type: 'device_calibration_action',
              id: '2'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationDevicePropertySerializer()
      const apiModel = serializer.convertModelToJsonApiData(measuredQuantity1, actionId)

      expect(apiModel).toEqual(expectedApiModel)
    })
  })
})

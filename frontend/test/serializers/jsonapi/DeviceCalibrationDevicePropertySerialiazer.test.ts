/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021 - 2023
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

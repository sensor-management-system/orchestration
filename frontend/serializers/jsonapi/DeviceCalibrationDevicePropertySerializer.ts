/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
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
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'
import {
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiEntityWithOptionalId
} from '@/serializers/jsonapi/JsonApiTypes'
export class DeviceCalibrationDevicePropertySerializer {
  private devicePropertySerializer: DevicePropertySerializer

  constructor () {
    this.devicePropertySerializer = new DevicePropertySerializer()
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): DeviceProperty[] {
    const devicePropertyCalibrationIds = []
    if (relationships.device_property_calibrations) {
      const devicePropertyCalibrationsObject = relationships.device_property_calibrations as IJsonApiEntityWithoutDetailsDataDictList
      if (devicePropertyCalibrationsObject.data && (devicePropertyCalibrationsObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipAttachmentData of devicePropertyCalibrationsObject.data as IJsonApiEntityWithoutDetails[]) {
          const devicePropertyCalibrationId = relationShipAttachmentData.id
          devicePropertyCalibrationIds.push(devicePropertyCalibrationId)
        }
      }
    }

    const devicePropertyIds = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_property_calibration') {
          const devicePropertyCalibrationId = includedEntry.id
          if (devicePropertyCalibrationIds.includes(devicePropertyCalibrationId)) {
            if ((includedEntry.relationships?.device_property?.data as IJsonApiEntityWithoutDetails | undefined)?.id) {
              devicePropertyIds.push((includedEntry.relationships?.device_property?.data as IJsonApiEntityWithoutDetails).id)
            }
          }
        }
      }
    }

    const deviceProperties: DeviceProperty[] = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_property') {
          const devicePropertyId = includedEntry.id
          if (devicePropertyIds.includes(devicePropertyId)) {
            const deviceProperty = this.devicePropertySerializer.convertJsonApiDataToModel(includedEntry)
            deviceProperties.push(deviceProperty)
          }
        }
      }
    }

    return deviceProperties
  }

  convertModelToJsonApiData (deviceProperty: DeviceProperty, actionId: string): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: 'device_property_calibration',
      attributes: {},
      relationships: {
        calibration_action: {
          data: {
            type: 'device_calibration_action',
            id: actionId
          }
        },
        device_property: {
          data: {
            type: 'device_property',
            id: deviceProperty.id || ''
          }
        }
      }
    }
    return data
  }
}

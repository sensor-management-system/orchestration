/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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

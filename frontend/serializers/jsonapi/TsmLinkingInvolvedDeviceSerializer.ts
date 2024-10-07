/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'
import { IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithOptionalId, IJsonApiEntityWithoutDetails } from '@/serializers/jsonapi/JsonApiTypes'

export class TsmLinkingInvolvedDeviceSerializer {
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): TsmLinkingInvolvedDevice {
    const relationships = jsonApiData.relationships!
    const deviceRelationships = relationships.device!
    const deviceData = deviceRelationships.data as IJsonApiEntityWithoutDetails
    const deviceId = deviceData.id

    const attributes = jsonApiData.attributes!
    return TsmLinkingInvolvedDevice.createFromObject({
      id: jsonApiData.id,
      deviceId,
      orderIndex: attributes.order_index
    })
  }

  convertModelToJsonApiData (involvedDevice: TsmLinkingInvolvedDevice, datastreamLinkId: string): IJsonApiEntityWithOptionalId {
    const result: IJsonApiEntityWithOptionalId = {
      type: 'involved_device_for_datastream_link',
      attributes: {
        order_index: involvedDevice.orderIndex
      },
      relationships: {
        device: {
          data: {
            id: involvedDevice.deviceId!,
            type: 'device'
          }
        },
        datastream_link: {
          data: {
            id: datastreamLinkId,
            type: 'datastream_link'
          }
        }
      }
    }
    if (involvedDevice.id) {
      result.id = involvedDevice.id
    }
    return result
  }
}

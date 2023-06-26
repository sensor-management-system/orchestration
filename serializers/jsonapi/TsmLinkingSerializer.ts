/**
 * @license
 * Web client of the Sensor Management System software developed within the
 * Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'
import { DeviceMountActionSerializer } from '@/serializers/jsonapi/DeviceMountActionSerializer'
import { TsmEndpointSerializer } from '@/serializers/jsonapi/TsmEndpointSerializer'

import {
  IJsonApiEntity,
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'
import { TsmLinking } from '@/models/TsmLinking'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export class TsmLinkingSerializer {
  private deviceMountActionSerializer: DeviceMountActionSerializer = new DeviceMountActionSerializer()
  private deviceSerializer: DeviceSerializer = new DeviceSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()
  private tsmEndpointSerializer: TsmEndpointSerializer = new TsmEndpointSerializer()

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): TsmLinking {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): TsmLinking[] {
    const included = jsonApiObjectList.included || []

    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity, included: IJsonApiEntityWithOptionalAttributes[]): TsmLinking {
    const tsmLinking = new TsmLinking()

    const deviceLookup: { [idx: string]: Device } = {}
    const deviceMountActionLookup: { [idx: string]: DeviceMountAction } = {}
    const devicePropertyLookup: { [idx: string]: DeviceProperty } = {}
    const tsmEndpointLookup: { [idx: string]: TsmEndpoint } = {}

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    tsmLinking.id = jsonApiData.id.toString()

    if (attributes) {
      tsmLinking.startDate = attributes.begin_date ? DateTime.fromISO(attributes.begin_date, { zone: 'UTC' }) : null
      tsmLinking.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null

      const datastream = new TsmdlDatastream(attributes.datastream_id.toString())
      datastream.name = attributes.datastream_name
      const datasource = new TsmdlDatasource(attributes.datasource_id.toString())
      datasource.name = attributes.datasource_name
      const thing = new TsmdlThing(attributes.thing_id.toString())
      thing.name = attributes.thing_name

      tsmLinking.datastream = datastream
      tsmLinking.thing = thing
      tsmLinking.datasource = datasource
    }

    for (const includedEntry of included) {
      if (includedEntry.type === 'device') {
        const deviceWithMeta = this.deviceSerializer.convertJsonApiDataToModel(includedEntry, included)
        if (deviceWithMeta.device.id !== null) {
          deviceLookup[deviceWithMeta.device.id] = deviceWithMeta.device
        }
      }
      if (includedEntry.type === 'device_mount_action') {
        const deviceMountAction = this.deviceMountActionSerializer.convertJsonApiDataToModel(includedEntry, included)
        if (deviceMountAction.id !== null) {
          deviceMountActionLookup[deviceMountAction.id] = deviceMountAction
        }
      }
      if (includedEntry.type === 'device_property') {
        const deviceProperty = this.devicePropertySerializer.convertJsonApiDataToModel(includedEntry)
        if (deviceProperty.id !== null) {
          devicePropertyLookup[deviceProperty.id] = deviceProperty
        }
      }
      if (includedEntry.type === 'tsm_endpoint') {
        const tsmEndpoint = this.tsmEndpointSerializer.convertJsonApiEntityToModel(includedEntry)
        if (tsmEndpoint.id !== null) {
          tsmEndpointLookup[tsmEndpoint.id] = tsmEndpoint
        }
      }
    }

    const deviceMountActionRelationship = relationships.device_mount_action as IJsonApiRelationships
    const deviceMountActionData = deviceMountActionRelationship.data as IJsonApiEntityWithoutDetails
    const deviceMountActionId = deviceMountActionData.id
    const deviceMountAction = deviceMountActionLookup[deviceMountActionId]

    const devicePropertyRelationship = relationships.device_property as IJsonApiRelationships
    const devicePropertyData = devicePropertyRelationship.data as IJsonApiEntityWithoutDetails
    const devicePropertyId = devicePropertyData.id
    const deviceProperty = devicePropertyLookup[devicePropertyId]

    const tsmEndpointRelationship = relationships.tsm_endpoint as IJsonApiRelationships
    const tsmEndpointData = tsmEndpointRelationship.data as IJsonApiEntityWithoutDetails
    const tsmEndpointId = tsmEndpointData.id
    const tsmEndpoint = tsmEndpointLookup[tsmEndpointId]

    const includedDevices: Device[] = Object.values(deviceLookup)
    const device = includedDevices.find(
      (includedDevice) => {
        return includedDevice.properties.find(
          property => property.id === devicePropertyId
        )
      }
    )

    tsmLinking.device = device ?? null
    tsmLinking.deviceMountAction = deviceMountAction
    tsmLinking.deviceProperty = deviceProperty
    tsmLinking.tsmEndpoint = tsmEndpoint

    return tsmLinking
  }

  convertModelToJsonApiData (tsmLinking: TsmLinking): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'datastream_link',
      attributes: {
        begin_date: tsmLinking.startDate!.setZone('UTC').toISO(),
        end_date: tsmLinking.endDate?.setZone('UTC').toISO() ?? null,
        datasource_id: tsmLinking.datasource!.id,
        datastream_id: tsmLinking.datastream!.id,
        thing_id: tsmLinking.thing!.id,
        datasource_name: tsmLinking.datasource!.name,
        datastream_name: tsmLinking.datastream!.name,
        thing_name: tsmLinking.thing!.name,
        tsm_endpoint: tsmLinking.tsmEndpoint!.url
      },
      relationships: {
        device_mount_action: {
          data: {
            type: 'device_mount_action',
            id: tsmLinking.deviceMountAction!.id
          }
        },
        device_property: {
          data: {
            type: 'device_property',
            id: tsmLinking.deviceProperty!.id
          }
        },
        tsm_endpoint: {
          data: {
            type: 'tsm_endpoint',
            id: tsmLinking.tsmEndpoint!.id
          }
        }
      }
    }
    if (tsmLinking.id) {
      data.id = tsmLinking.id
    }
    return data
  }
}

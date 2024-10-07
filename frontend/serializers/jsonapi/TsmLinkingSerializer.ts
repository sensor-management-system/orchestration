/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'
import { DeviceMountActionSerializer } from '@/serializers/jsonapi/DeviceMountActionSerializer'
import { TsmEndpointSerializer } from '@/serializers/jsonapi/TsmEndpointSerializer'
import { TsmLinkingInvolvedDeviceSerializer } from '@/serializers/jsonapi/TsmLinkingInvolvedDeviceSerializer'

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
import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'

export class TsmLinkingSerializer {
  private deviceMountActionSerializer: DeviceMountActionSerializer = new DeviceMountActionSerializer()
  private deviceSerializer: DeviceSerializer = new DeviceSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()
  private tsmEndpointSerializer: TsmEndpointSerializer = new TsmEndpointSerializer()
  private tsmLinkingInvolvedDeviceSerializer: TsmLinkingInvolvedDeviceSerializer = new TsmLinkingInvolvedDeviceSerializer()

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
    const involvedDevicesLookup: { [idx: string]: TsmLinkingInvolvedDevice } = {}

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    tsmLinking.id = jsonApiData.id.toString()

    if (attributes) {
      tsmLinking.startDate = attributes.begin_date ? DateTime.fromISO(attributes.begin_date, { zone: 'UTC' }) : null
      tsmLinking.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null

      const datastream = new TsmdlDatastream(attributes.datastream_id.toString())
      datastream.name = attributes.datastream_name || ''
      const datasource = new TsmdlDatasource(attributes.datasource_id.toString())
      datasource.name = attributes.datasource_name || ''
      const thing = new TsmdlThing(attributes.thing_id.toString())
      thing.name = attributes.thing_name || ''

      tsmLinking.datastream = datastream
      tsmLinking.thing = thing
      tsmLinking.datasource = datasource

      tsmLinking.licenseName = attributes.license_name || ''
      tsmLinking.licenseUri = attributes.license_uri || ''
      tsmLinking.aggregationPeriod = !isNaN(attributes.aggregation_period) ? attributes.aggregation_period : null
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
      if (includedEntry.type === 'involved_device_for_datastream_link') {
        const involvedDevice = this.tsmLinkingInvolvedDeviceSerializer.convertJsonApiDataToModel(includedEntry)
        involvedDevicesLookup[includedEntry.id] = involvedDevice
      }
    }

    const deviceMountActionRelationship = relationships.device_mount_action as IJsonApiRelationships
    const deviceMountActionData = deviceMountActionRelationship.data as IJsonApiEntityWithoutDetails
    const deviceMountActionId = deviceMountActionData.id
    const deviceMountAction = deviceMountActionLookup[deviceMountActionId] || null

    const devicePropertyRelationship = relationships.device_property as IJsonApiRelationships
    const devicePropertyData = devicePropertyRelationship.data as IJsonApiEntityWithoutDetails
    const devicePropertyId = devicePropertyData.id
    const deviceProperty = devicePropertyLookup[devicePropertyId] || null

    const tsmEndpointRelationship = relationships.tsm_endpoint as IJsonApiRelationships
    const tsmEndpointData = tsmEndpointRelationship.data as IJsonApiEntityWithoutDetails
    const tsmEndpointId = tsmEndpointData.id
    const tsmEndpoint = tsmEndpointLookup[tsmEndpointId] || null

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

    const involvedDevices = []
    if (relationships.involved_devices && relationships.involved_devices.data) {
      for (const entry of (relationships.involved_devices.data as IJsonApiEntityWithoutDetails[])) {
        const involvedDevice = involvedDevicesLookup[entry.id]
        involvedDevices.push(involvedDevice)
      }
    }
    tsmLinking.involvedDevices = involvedDevices

    return tsmLinking
  }

  convertModelToJsonApiData (tsmLinking: TsmLinking): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'datastream_link',
      attributes: {
        begin_date: tsmLinking.startDate?.setZone('UTC').toISO() ?? null,
        end_date: tsmLinking.endDate?.setZone('UTC').toISO() ?? null,
        datasource_id: tsmLinking.datasource!.id,
        datastream_id: tsmLinking.datastream!.id,
        thing_id: tsmLinking.thing!.id,
        datasource_name: tsmLinking.datasource!.name,
        datastream_name: tsmLinking.datastream!.name,
        thing_name: tsmLinking.thing!.name,
        license_name: tsmLinking.licenseName,
        license_uri: tsmLinking.licenseUri,
        aggregation_period: tsmLinking.aggregationPeriod
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

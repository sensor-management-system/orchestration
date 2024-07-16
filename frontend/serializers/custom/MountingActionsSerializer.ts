/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Contact } from '@/models/Contact'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'

import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { PlatformSerializer } from '@/serializers/jsonapi/PlatformSerializer'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceMountActionBasicDataSerializer'
import { PlatformMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformMountActionBasicDataSerializer'

import { stringToDate } from '@/utils/dateHelper'
import { ConfigurationMountingAction } from '@/models/ConfigurationMountingAction'
import { Device } from '@/models/Device'

export class MountingActionsSerializer {
  private deviceSerializer: DeviceSerializer = new DeviceSerializer()
  private platformSerializer: PlatformSerializer = new PlatformSerializer()
  private deviceMountActionBasicDataSerializer: DeviceMountActionBasicDataSerializer = new DeviceMountActionBasicDataSerializer()
  private platformMountActionBasicDataSerializer: PlatformMountActionBasicDataSerializer = new PlatformMountActionBasicDataSerializer()

  convertApiObjectToTree (apiResponse: any[], contacts: Contact[]): ConfigurationsTree {
    const contactsLookup: { [idx: string]: Contact } = {}
    for (const contact of contacts) {
      if (contact.id) {
        contactsLookup[contact.id] = contact
      }
    }

    const convertElementToTreeNode = (apiElement: any, parentPlatform: Platform | null, parentDevice: Device | null): ConfigurationsTreeNode => {
      const entity = apiElement.entity
      const action = apiElement.action
      let endContact = null

      if (action.data.relationships.end_contact?.data?.id) {
        endContact = contactsLookup[action.data.relationships.end_contact.data.id]
      }
      if (entity.data.type === 'device') {
        const device = this.deviceSerializer.convertJsonApiDataToModel(entity.data, []).device
        const children = apiElement.children.map((c: any) => convertElementToTreeNode(c, null, device))
        // const deviceMountActionBasicData = this.deviceMountActionBasicDataSerializer.convertJsonApiDataToModel(action.data)
        const mountAction = DeviceMountAction.createFromObject({
          id: action.data.id,
          offsetX: action.data.attributes.offset_x,
          offsetY: action.data.attributes.offset_y,
          offsetZ: action.data.attributes.offset_z,
          epsgCode: action.data.attributes.epsg_code || '',
          x: !isNaN(action.data.attributes.x) ? action.data.attributes.x : null,
          y: !isNaN(action.data.attributes.y) ? action.data.attributes.y : null,
          z: !isNaN(action.data.attributes.z) ? action.data.attributes.z : null,
          elevationDatumName: action.data.attributes.elevation_datum_name || '',
          elevationDatumUri: action.data.attributes.elevation_datum_uri || '',
          beginDescription: action.data.attributes.begin_description,
          endDescription: action.data.attributes.end_description ?? '',
          beginDate: stringToDate(action.data.attributes.begin_date),
          endDate: action.data.attributes.end_date ? stringToDate(action.data.attributes.end_date) : null,
          device,
          parentPlatform,
          parentDevice,
          beginContact: contactsLookup[action.data.relationships.begin_contact.data.id],
          endContact: endContact ?? null,
          label: action.data.attributes.label || ''

        })
        const node = new DeviceNode(mountAction)
        node.children = children
        return node
      } else if (entity.data.type === 'platform') {
        const platform = this.platformSerializer.convertJsonApiDataToModel(entity.data, []).platform
        const children = apiElement.children.map((c: any) => convertElementToTreeNode(c, platform, null))
        // const platformMountActionBasicData = this.platformMountActionBasicDataSerializer.convertJsonApiDataToModel(action.data)
        const mountAction = PlatformMountAction.createFromObject({
          id: action.data.id,
          offsetX: action.data.attributes.offset_x,
          offsetY: action.data.attributes.offset_y,
          offsetZ: action.data.attributes.offset_z,
          epsgCode: action.data.attributes.epsg_code || '',
          x: !isNaN(action.data.attributes.x) ? action.data.attributes.x : null,
          y: !isNaN(action.data.attributes.y) ? action.data.attributes.y : null,
          z: !isNaN(action.data.attributes.z) ? action.data.attributes.z : null,
          elevationDatumName: action.data.attributes.elevation_datum_name || '',
          elevationDatumUri: action.data.attributes.elevation_datum_uri || '',
          beginDescription: action.data.attributes.begin_description,
          endDescription: action.data.attributes.end_description ?? '',
          beginDate: stringToDate(action.data.attributes.begin_date),
          endDate: action.data.attributes.end_date ? stringToDate(action.data.attributes.end_date) : null,
          platform,
          parentPlatform,
          beginContact: contactsLookup[action.data.relationships.begin_contact.data.id],
          endContact: endContact ?? null,
          label: action.data.attributes.label || ''
        })
        const node = new PlatformNode(mountAction)
        node.children = children
        return node
      } else {
        throw new Error('Can only handle devices or platforms')
      }
    }
    const nodes = apiResponse.map((x: any) => convertElementToTreeNode(x, null, null))
    return ConfigurationsTree.fromArray(nodes)
  }

  convertApiTimepointsToObject (apiResponse: any[]): ConfigurationMountingAction[] {
    const newMountingActions: ConfigurationMountingAction[] = []
    apiResponse.forEach((action) => {
      const newTimePoint = stringToDate(action.timepoint)
      if (action.type.startsWith('device')) {
        const device = new Device()
        device.shortName = action.attributes.short_name
        newMountingActions.push(new ConfigurationMountingAction(device, newTimePoint, action.type))
        return new ConfigurationMountingAction(device, newTimePoint, action.type)
      } else if (action.type.startsWith('platform')) {
        const platform = new Platform()
        platform.shortName = action.attributes.short_name
        newMountingActions.push(new ConfigurationMountingAction(platform, newTimePoint, action.type))
      }
    })
    return newMountingActions
  }
}

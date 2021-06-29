<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <v-treeview
      :items="items"
      :activatable="false"
      :hoverable="false"
      rounded
      open-all
    >
      <template #prepend="{ item }">
        <v-icon v-if="item.isPlatform()">
          mdi-rocket-outline
        </v-icon>
        <v-icon v-else>
          mdi-network-outline
        </v-icon>
      </template>
    </v-treeview>
    <p
      class="font-italic text--secondary"
    >
      This is a demo hierarchy. Replace it with your own platform and devices.
    </p>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select platforms and devices for a configuration
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { buildConfigurationTree } from '@/modelUtils/mountHelpers'

/**
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsDemoTreeView extends Vue {
  createPlatform (id: string) {
    const p = new Platform()
    p.id = id
    p.shortName = 'Platform ' + id
    return p
  }

  createDevice (id: string) {
    const d = new Device()
    d.id = id
    d.shortName = 'Device ' + id
    return d
  }

  private platforms: Platform[] = [
    this.createPlatform('1'),
    this.createPlatform('2'),
    this.createPlatform('3')
  ]

  private devices: Device[] = [
    this.createDevice('1'),
    this.createDevice('2'),
    this.createDevice('3')
  ]

  /**
   * returns a demo tree
   *
   * @return {ConfigurationsTreeNode[]} a demo tree
   */
  get items (): ConfigurationsTreeNode[] {
    const demoContact = new Contact()
    demoContact.givenName = 'Max'
    demoContact.familyName = 'Mustermann'
    demoContact.email = 'max.mustermann@mail.org'

    const platformMountActions = [
      PlatformMountAction.createFromObject({
        id: '',
        platform: this.platforms[0],
        parentPlatform: null,
        date: DateTime.utc(2020, 10, 11),
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact: demoContact,
        description: 'Mounted platform 1'
      }),
      PlatformMountAction.createFromObject({
        id: '',
        platform: this.platforms[1],
        parentPlatform: this.platforms[0],
        date: DateTime.utc(2020, 10, 13),
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact: demoContact,
        description: 'Mounted platform 2 on platform 1'
      })
    ]
    const platformUnmountActions = [
      PlatformUnmountAction.createFromObject({
        id: '',
        platform: this.platforms[1],
        date: DateTime.utc(2020, 10, 19),
        contact: demoContact,
        description: 'Unmounted platform 2'
      })
    ]
    const deviceMountActions = [
      DeviceMountAction.createFromObject({
        id: '',
        device: this.devices[0],
        parentPlatform: this.platforms[0],
        date: DateTime.utc(2020, 10, 12),
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact: demoContact,
        description: 'Mounted device 1 on platform 1'
      }),
      DeviceMountAction.createFromObject({
        id: '',
        device: this.devices[1],
        parentPlatform: this.platforms[1],
        date: DateTime.utc(2020, 10, 15),
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact: demoContact,
        description: 'Mounted device 2 on platform 2'
      }),
      DeviceMountAction.createFromObject({
        id: '',
        device: this.devices[2],
        parentPlatform: null,
        date: DateTime.utc(2020, 10, 17),
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact: demoContact,
        description: 'Mounted device 3'
      })
    ]
    const deviceUnmountActions = [
      DeviceUnmountAction.createFromObject({
        id: '',
        device: this.devices[1],
        date: DateTime.utc(2020, 10, 16),
        contact: demoContact,
        description: 'Unmounted device 2'
      })
    ]

    const tree = buildConfigurationTree({
      platformMountActions,
      platformUnmountActions,
      deviceMountActions,
      deviceUnmountActions
    }, DateTime.utc(2020, 10, 17))

    return tree.toArray()
  }
}
</script>

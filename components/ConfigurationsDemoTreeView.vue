<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
      <template v-slot:prepend="{ item }">
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

import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { PlatformNode } from '@/models/PlatformNode'
import { DeviceNode } from '@/models/DeviceNode'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'

/**
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsDemoTreeView extends Vue {
  /**
   * returns a demo tree
   *
   * @return {ConfigurationsTreeNode[]} a demo tree
   */
  get items (): ConfigurationsTreeNode[] {
    return ConfigurationsTree.fromArray(
      [
        ((): PlatformNode => {
          const n = new PlatformNode(
            ((): Platform => {
              const o = new Platform()
              o.id = '-1'
              o.shortName = 'Platform 01'
              return o
            })()
          )
          n.disabled = true
          n.setTree(
            ConfigurationsTree.fromArray(
              [
                ((): PlatformNode => {
                  const n = new PlatformNode(
                    ((): Platform => {
                      const o = new Platform()
                      o.id = '-2'
                      o.shortName = 'Platform 02'
                      return o
                    })()
                  )
                  n.disabled = true
                  n.setTree(
                    ConfigurationsTree.fromArray(
                      [
                        new DeviceNode(
                          ((): Device => {
                            const o = new Device()
                            o.id = '-3'
                            o.shortName = 'Device 01'
                            return o
                          })()
                        ),
                        new DeviceNode(
                          ((): Device => {
                            const o = new Device()
                            o.id = '-4'
                            o.shortName = 'Device 02'
                            return o
                          })()
                        ),
                        new DeviceNode(
                          ((): Device => {
                            const o = new Device()
                            o.id = '-5'
                            o.shortName = 'Device 03'
                            return o
                          })()
                        )
                      ]
                    )
                  )
                  return n
                })()
              ]
            )
          )
          return n
        })(),
        (() => {
          const n = new PlatformNode(
            ((): Platform => {
              const o = new Platform()
              o.id = '-6'
              o.shortName = 'Platform 03'
              return o
            })()
          )
          n.disabled = true
          return n
        })()
      ]
    ).toArray()
  }
}
</script>

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
import Platform from '@/models/Platform'
import Device from '@/models/Device'

/**
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsDemoTreeView extends Vue {
  get items (): ConfigurationsTreeNode[] {
    return ConfigurationsTree.fromArray(
      [
        ((): PlatformNode => {
          const n = new PlatformNode(
            ((): Platform => {
              const o = new Platform()
              o.id = '-1'
              o.shortName = 'Platform 01'
              o.longName = 'Platform 01 Bla blub'
              o.description = 'A platform on which various light instruments can be mounted. Consists of wood, dry and rotten wood.'
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

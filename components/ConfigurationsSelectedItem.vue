<template>
  <v-card
    v-if="value"
    outlined
  >
    <v-breadcrumbs :items="breadcrumbs" divider=">" />
    <v-card-text>
      <v-row>
        <v-col cols="12" md="9">
          <template v-if="description">
            {{ description }}
          </template>
          <template v-else-if="isPlatform">
            The selected platform has no description.
          </template>
          <template v-else-if="isDevice">
            The selected device has no description.
          </template>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        v-if="value"
        color="red"
        text
        data-role="remove-node"
        @click="remove"
      >
        remove
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
/**
* @file provides a component to select platforms and devices for a configuration
* @author <marc.hanisch@gfz-potsdam.de>
*/
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { PlatformNode } from '@/models/PlatformNode'
import { DeviceNode } from '@/models/DeviceNode'

/**
* A class component to select platforms and devices for a configuration
* @extends Vue
*/
@Component
// @ts-ignore
export default class ConfigurationsSelectedItem extends Vue {
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value: ConfigurationsTreeNode | null

  @Prop({
    default: () => [],
    type: Array
  })
  // @ts-ignore
  readonly breadcrumbs: string[]

  /**
   * returns whether a node is a PlatformNode or not
   *
   * @return {boolean} true if the node is a PlatformNode
   */
  get isPlatform (): boolean {
    return this.value instanceof PlatformNode
  }

  /**
   * returns whether a node is a DeviceNode or not
   *
   * @return {boolean} true if the node is a DeviceNode
   */
  get isDevice (): boolean {
    return this.value instanceof DeviceNode
  }

  get description (): string {
    if (!this.value) {
      return ''
    }
    return this.value.unpack().description
  }

  remove () {
    this.$emit('remove', this.value)
  }
}
</script>

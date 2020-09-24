<template>
  <v-card
    v-if="value"
    outlined
  >
    <v-breadcrumbs :items="breadcrumbs" divider=">" />
    <v-card-text>
      <template v-if="description">
        {{ description }}
      </template>
      <template v-else-if="value.isPlatform()">
        <span class="text--disabled">The selected platform has no description.</span>
      </template>
      <template v-else-if="value.isDevice()">
        <span class="text--disabled">The selected device has no description.</span>
      </template>
    </v-card-text>
    <v-card-actions
      v-if="!readonly"
    >
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

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

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

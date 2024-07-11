<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-list-item
    :disabled="readonly"
    dense
    @click.prevent="triggerOuterClick"
  >
    <v-list-item-content>
      <v-list-item-title
        :class="readonly ? 'grey-text':'text'"
      >
        <v-icon
          left
          small
          :color="readonly ? 'grey':'black'"
        >
          mdi-file-xml-box
        </v-icon>
        SensorML
      </v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>
<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
@Component
export default class DotMenuSensorML extends Vue {
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  triggerOuterClick () {
    this.$emit('click')
  }
}
</script>

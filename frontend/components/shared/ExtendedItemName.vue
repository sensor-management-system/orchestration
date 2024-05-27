<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div class="d-inline-block">
    <span>{{ shortenedName }}</span>
    <template
      v-if="extended"
    >
      <v-tooltip v-if="$vuetify.breakpoint.smAndUp" bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="!skipManufacturerName && value.manufacturerName !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ value.manufacturerName | shortenMiddle }}</span>
        </template>
        <span>Manufacturer</span>
      </v-tooltip>
      <v-tooltip v-if="$vuetify.breakpoint.smAndUp" bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="!skipModel && value.model !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ value.model | shortenMiddle }}</span>
        </template>
        <span>Model number</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="value.serialNumber !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ value.serialNumber | shortenMiddle }}</span>
        </template>
        <span>Serial number</span>
      </v-tooltip>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

@Component
export default class ExtendedItemName extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private value!: Platform | Device

  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  private extended!: boolean

  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  private shorten!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private skipManufacturerName!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private skipModel!: boolean

  get shortenedName (): string {
    if (this.shorten) {
      return this.$options.filters!.shortenMiddle(this.value.shortName)
    }
    return this.value.shortName
  }
}

</script>

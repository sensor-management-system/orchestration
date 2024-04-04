<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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

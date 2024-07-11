<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <label>Manufacturer</label>
        {{ value.manufacturerName | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Model</label>
        {{ value.model | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>External system</label>
        {{ value.externalSystemName | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>External system URL</label>
        {{ value.externalSystemUrl | orDefault }}
        <a v-if="value.externalSystemUrl.length > 0" :href="value.externalSystemUrl" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { ManufacturerModel } from '@/models/ManufacturerModel'

@Component({})
export default class ManufacturerModelBasicData extends Vue {
  @Prop({
    default: () => new ManufacturerModel(),
    type: ManufacturerModel
  })
  readonly value!: ManufacturerModel
}
</script>

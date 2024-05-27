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
        <label>Dual use<span v-if="visibiltyMarkerPublic"> {{ visibiltyMarkerPublic }}</span></label>
        {{ dualUseText }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>Export control classification number<span v-if="visibiltyMarkerPublic"> {{ visibiltyMarkerPublic }}</span></label>
        {{ value.exportControlClassificationNumber | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Customs tariff number<span v-if="visibiltyMarkerPublic"> {{ visibiltyMarkerPublic }}</span></label>
        {{ value.customsTariffNumber | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Additional information<span v-if="visibiltyMarkerPublic"> {{ visibiltyMarkerPublic }}</span></label>
        {{ value.additionalInformation | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="showInternalNote">
      <v-col cols="12" md="9">
        <label>Internal note<span v-if="visibiltyMarkerInternal"> {{ visibiltyMarkerInternal }}</span></label>
        {{ value.internalNote | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { ExportControl } from '@/models/ExportControl'

@Component({

})
export default class ExportControlBasicData extends Vue {
  @Prop({
    default: () => new ExportControl(),
    required: true,
    type: ExportControl
  })
  readonly value!: ExportControl

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly showInternalNote!: boolean

  @Prop({
    default: () => '',
    type: String
  })
  readonly visibiltyMarkerPublic!: string

  @Prop({
    default: () => '',
    type: String
  })
  readonly visibiltyMarkerInternal!: string

  get dualUseText (): string {
    if (this.value.dualUse === true) {
      return 'Yes'
    } else if (this.value.dualUse === false) {
      return 'No'
    }
    return 'Not yet specified'
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
    <v-row>
      <v-col cols="12" md="6">
        <label>Dual use</label>
        {{ dualUseText }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>Export control classification number</label>
        {{ value.exportControlClassificationNumber | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Customs tariff number</label>
        {{ value.customsTariffNumber | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Additional information</label>
        {{ value.additionalInformation | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="showInternalNote">
      <v-col cols="12" md="9">
        <label>Internal note</label>
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

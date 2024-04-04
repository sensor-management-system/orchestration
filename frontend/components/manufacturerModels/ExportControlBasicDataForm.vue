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
  <v-form
    ref="basicForm"
    @submit.prevent
  >
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          :value="value.dualUse"
          label="Dual use"
          hint="can be used for military aims"
          :persistent-hint="true"
          color="red darken-3"
          :items="exportControlOptions"
          @change="update('dualUse', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.exportControlClassificationNumber"
          label="Export control classification number"
          @input="update('exportControlClassificationNumber', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.customsTariffNumber"
          label="Customs tariff number"
          @input="update('customsTariffNumber', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-textarea
          :value="value.additionalInformation"
          label="Additional information"
          rows="3"
          @input="update('additionalInformation', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-textarea
          :value="value.internalNote"
          label="Internal note"
          rows="3"
          @input="update('internalNote', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { ExportControl } from '@/models/ExportControl'

interface IExportControlOption {
  text: string
  value: boolean | null
}

@Component({})
export default class ExportControlBasicDataForm extends Vue {
  @Prop({
    required: true,
    type: ExportControl
  })
  readonly value!: ExportControl

  update (key: string, value: any) {
    const newObj = ExportControl.createFromObject(this.value)

    switch (key) {
      case 'dualUse':
        newObj.dualUse = value
        break
      case 'exportControlClassificationNumber':
        newObj.exportControlClassificationNumber = value as string
        break
      case 'customsTariffNumber':
        newObj.customsTariffNumber = value as string
        break
      case 'additionalInformation':
        newObj.additionalInformation = value as string
        break
      case 'internalNote':
        newObj.internalNote = value as string
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', newObj)
  }

  get exportControlOptions (): IExportControlOption[] {
    return [
      {
        text: 'Not yet specified',
        value: null
      },
      {
        text: 'Yes',
        value: true
      },
      {
        text: 'No',
        value: false
      }
    ]
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>

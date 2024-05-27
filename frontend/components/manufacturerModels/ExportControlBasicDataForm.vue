<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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

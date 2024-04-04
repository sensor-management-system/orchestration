<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
  <base-expandable-list-item expandable-color="grey lighten-5" background-color="white">
    <template v-if="!hideHeader" #header>
      <export-control-chip :value="exportControlStatus" />
      {{ manufacturerModel.manufacturerName }}
    </template>
    <template #actions>
      <v-btn
        :to="detailLink"
        color="primary"
        text
        small
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #default>
      {{ manufacturerModel.model }}
    </template>
    <template #expandable>
      <v-row no-gutters>
        <v-col
          cols="3"
          md="3"
          class="font-weight-medium"
        >
          Export control classification number:
        </v-col>
        <v-col
          cols="3"
          md="3"
          class="nowrap-truncate"
        >
          {{ manufacturerModel.exportControl?.exportControlClassificationNumber | orDefault }}
        </v-col>
        <v-col
          cols="3"
          md="3"
          class="font-weight-medium"
        >
          Customs tariff number:
        </v-col>
        <v-col
          cols="3"
          md="3"
          class="nowrap-truncate"
        >
          {{ manufacturerModel.exportControl?.customsTariffNumber | orDefault }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { ManufacturerModel } from '@/models/ManufacturerModel'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExportControlChip from '@/components/manufacturerModels/ExportControlChip.vue'

@Component({
  components: {
    BaseExpandableListItem,
    ExportControlChip
  }
})
export default class ManufacturerModelsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private manufacturerModel!: ManufacturerModel

  @Prop({
    type: Boolean,
    default: false
  })
  private hideHeader!: boolean

  @Prop({
    default: '',
    type: String
  })
  private from!: string

  get detailLink (): string {
    let params = ''
    if (this.from) {
      params = '?' + (new URLSearchParams({ from: this.from })).toString()
    }
    return `/manufacturer-models/${this.manufacturerModel.id}${params}`
  }

  openLink () {
    this.$router.push(this.detailLink)
  }

  get exportControlStatus (): boolean | null {
    let result: boolean | null = null
    if (this.manufacturerModel.exportControl) {
      const exportControl = this.manufacturerModel.exportControl
      if (exportControl.dualUse === true || exportControl.dualUse === false) {
        result = this.manufacturerModel.exportControl.dualUse
      }
    }
    return result
  }
}
</script>

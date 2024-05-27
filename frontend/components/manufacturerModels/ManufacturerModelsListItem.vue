<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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

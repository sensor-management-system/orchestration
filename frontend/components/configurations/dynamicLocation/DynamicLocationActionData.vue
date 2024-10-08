<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-card>
    <v-card-title>
      Begin of the dynamic location
      <v-spacer />
      <slot name="dot-menu" />
    </v-card-title>
    <v-card-text class="text--primary">
      <v-row>
        <v-col cols="12" md="6">
          <label>Begin date</label>
          {{ value.beginDate | dateToDateTimeStringHHMM }}
          <span class="text-caption text--secondary">(UTC)</span>
        </v-col>
        <v-col cols="12" md="6">
          <label>Label</label>
          {{ value.label | orDefault }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="3">
          <device-property-hierarchy-select
            v-model="value.x"
            :devices="devices"
            device-select-label="Device that measures x"
            property-select-label="Measured quantity for x"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <device-property-hierarchy-select
            v-model="value.y"
            :devices="devices"
            device-select-label="Device that measures y"
            property-select-label="Measured quantity for y"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <device-property-hierarchy-select
            v-model="value.z"
            :devices="devices"
            device-select-label="Device that measures z"
            property-select-label="Measured quantity for z"
            readonly
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="3">
          <label>EPSG Code</label>
          {{ epsgCode | orDefault }}
        </v-col>
        <v-col cols="12" md="3">
          <label>Elevation Datum</label>
          {{ elevationDatum | orDefault }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <label>Description</label>
          {{ value.beginDescription | orDefault }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <label>Contact</label>
          {{ value.beginContact?.toString() }}
        </v-col>
      </v-row>
    </v-card-text>
    <v-divider class="mx-4 mt-4" />
    <v-card-title>
      End of the dynamic location
    </v-card-title>
    <v-card-text class="text--primary">
      <v-row>
        <v-col>
          <label>End date</label>
          {{ value.endDate | dateToDateTimeStringHHMM }}
          <span class="text-caption text--secondary">(UTC)</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <label>Description</label>
          {{ value.endDescription | orDefault }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <label>Contact</label>
          {{ endContact | orDefault }}
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { Device } from '@/models/Device'
import { VocabularyState } from '@/store/vocabulary'
import { EpsgCode } from '@/models/EpsgCode'
import { ElevationDatum } from '@/models/ElevationDatum'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
@Component({
  components: { DevicePropertyHierarchySelect },
  filters: {
    dateToDateTimeStringHHMM
  },
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData'])
  }
})
export default class DynamicLocationActionData extends Vue {
  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: Object
  })
  readonly value!: DynamicLocationAction

  @Prop({
    default: () => [],
    type: Array
  })
  readonly devices!: Device[]

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']

  get epsgCode (): string {
    const epsgCodeIndex = this.epsgCodes.findIndex((e: EpsgCode) => e.code === this.value.epsgCode)
    if (epsgCodeIndex > -1) {
      return this.epsgCodes[epsgCodeIndex].text
    }
    return this.value.epsgCode
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  get endContact () {
    if (this.value.endContact) {
      return this.value.endContact.toString()
    }
    return ''
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>

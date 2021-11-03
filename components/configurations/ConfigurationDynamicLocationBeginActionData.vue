<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
      <v-col>
        <label>Begin date</label>
        {{ value.beginDate | dateToDateTimeStringHHMM }}
        <span class="text-caption text--secondary">(UTC)</span>
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
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>Contact</label>
        {{ value.contact.toString() }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'

import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

@Component({
  components: {
    DevicePropertyHierarchySelect
  },
  filters: {
    dateToDateTimeStringHHMM
  }
})
export default class ConfigurationDynamicLocationBeginActionData extends Vue {
  @Prop({
    default: () => new DynamicLocationBeginAction(),
    required: true,
    type: Object
  })
  readonly value!: DynamicLocationBeginAction

  @Prop({
    default: () => [],
    type: Array
  })
  readonly devices!: Device[]

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly epsgCodes!: EpsgCode[]

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly elevationData!: ElevationDatum[]

  get epsgCode (): string {
    const epsgCodeIndex = this.epsgCodes.findIndex(e => e.code === this.value.epsgCode)
    if (epsgCodeIndex > -1) {
      return this.epsgCodes[epsgCodeIndex].text
    }
    return this.value.epsgCode
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>

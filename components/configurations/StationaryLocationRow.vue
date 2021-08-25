<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-row v-if="!readonly">
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number.lazy="configuration.location.latitude"
          label="Latitude (WGS84)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number.lazy="configuration.location.longitude"
          label="Longitude (WGS84)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number="configuration.location.elevation"
          label="Elevation (m asl)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12" md="3">
        <label>Latitude (WGS84)</label>
        {{ configuration.location.latitude }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Longitude (WGS84)</label>
        {{ configuration.location.longitude }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Elevation (m asl)</label>
        {{ configuration.location.elevation }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

@Component
export default class StationaryLocationRow extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({ default: false, type: Configuration }) configuration!: Configuration
}
</script>

<style scoped>

</style>

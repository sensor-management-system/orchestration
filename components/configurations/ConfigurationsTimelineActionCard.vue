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
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-header class="py-0 pl-0">
        <v-container class="pa-0">
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-subtitle class="pb-0">
                {{ action.date | dateToDateTimeString }}
              </v-card-subtitle>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-title class="pt-0 pb-0">
                {{ action.title }}
              </v-card-title>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-subtitle class="pt-0">
                {{ action.contact.toString() }}
              </v-card-subtitle>
            </v-col>
          </v-row>
        </v-container>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-card-text
          class="text--primary"
        >
          <v-row
            v-if="action.mountInfo && action.mountInfo.parentPlatform"
            dense
          >
            <v-col cols="12" md="4">
              <label>Mounted on</label>
              {{ action.mountInfo.parentPlatform.shortName }}
            </v-col>
          </v-row>
          <v-row
            v-if="action.mountInfo"
            dense
          >
            <v-col cols="12" md="3">
              <label>Offset x</label>
              {{ action.mountInfo.offsetX }}
            </v-col>
            <v-col cols="12" md="3">
              <label>Offset y</label>
              {{ action.mountInfo.offsetY }}
            </v-col>
            <v-col cols="12" md="3">
              <label>Offset z</label>
              {{ action.mountInfo.offsetZ }}
            </v-col>
          </v-row>
          <v-row dense>
            <v-col>
              <label>Description</label>
              {{ action.description }}
            </v-col>
          </v-row>
        </v-card-text>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { ITimelineAction } from '@/utils/configurationInterfaces'
import { dateToDateTimeString } from '@/utils/dateHelper'

@Component({
  filters: {
    dateToDateTimeString
  }
})
export default class ConfigurationsTimelineActionCard extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly action!: ITimelineAction
}
</script>

<style scoped>

</style>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
  <v-card>
    <v-card-subtitle class="pb-0">
      <v-row no-gutters>
        <v-col>
          {{ value.basicData.beginDate | toUtcDate }}
          <span class="text-caption text--secondary">(UTC)</span>
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="menu" />
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-title class="pt-0">
      Mounted on {{ value.configuration.label }}
    </v-card-title>
    <v-card-subtitle class="pb-1">
      <v-row
        no-gutters
      >
        <v-col>
          {{ value.beginContact.toString() }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="actions" />
          <v-btn
            :to="'/configurations/' + value.configuration.id"
            color="primary"
            text
            @click.stop.prevent
          >
            View
          </v-btn>
          <v-btn
            icon
            @click.stop.prevent="show =!show"
          >
            <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-expand-transition>
      <div
        v-show="show"
      >
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <div v-if="value.parentPlatform !== null">
            <label>Parent platform</label>{{ value.parentPlatform.shortName }}
          </div>
          <v-row dense>
            <v-col cols="12" md="4">
              <label>Offset x</label>{{ value.basicData.offsetX }} m
            </v-col>
            <v-col cols="12" md="4">
              <label>Offset y</label>{{ value.basicData.offsetY }} m
            </v-col>
            <v-col cols="12" md="4">
              <label>Offset z</label>{{ value.basicData.offsetZ }} m
            </v-col>
          </v-row>
          <label>Description</label>
          {{ value.basicData.beginDescription }}
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a Device Mount Action card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'

/**
 * A class component for Device Mount Action card
 * @extends Vue
 */
@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  }
})
// @ts-ignore
export default class DeviceMountActionCard extends Vue {
  private show: boolean = false

  /**
   * a DeviceMountAction
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: DeviceMountAction
}
</script>

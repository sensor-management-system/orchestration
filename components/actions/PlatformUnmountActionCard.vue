<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
          {{ value.basicData.endDate | dateToDateTimeString }}
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
      Unmounted on {{ value.configuration.label }}
    </v-card-title>
    <v-card-subtitle class="pb-1">
      <v-row
        no-gutters
      >
        <v-col>
          {{ value.endContact.toString() }}
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
            @click.stop.prevent="show = !show"
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
          <label>Description</label>
          {{ value.basicData.endDescription }}
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a Platform Unmount Action card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'

/**
 * A class component for Platform Unmount Action card
 * @extends Vue
 */
@Component({
  filters: {
    dateToDateTimeString
  }
})
// @ts-ignore
export default class PlatformUnmountActionCard extends Vue {
  private show: boolean = false

  /**
   * a PlatformMountAction
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: PlatformMountAction
}
</script>

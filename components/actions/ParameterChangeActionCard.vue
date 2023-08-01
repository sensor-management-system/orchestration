<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
          {{ value.date | toUtcDate }}
          <span class="text-caption text--secondary">(UTC)</span>
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <DotMenu>
            <template #actions>
              <slot name="dot-menu-items" />
            </template>
          </DotMenu>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-title class="pt-0">
      {{ title }}
    </v-card-title>
    <v-card-subtitle class="pb-1">
      <v-row
        no-gutters
      >
        <v-col>
          {{ value.contact.toString() }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="actions" />
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
      <div v-show="show">
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <div>
            <label>
              Value
            </label>
            {{ value.value | orDefault }}
          </div>
          <div>
            <label>
              Unit
            </label>
            {{ value.parameter.unitName | orDefault }}
          </div>
          <div>
            <label>Description</label>
            {{ value.description | orDefault }}
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a parameter change action card
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { dateToDateTimeString } from '@/utils/dateHelper'

import DotMenu from '@/components/DotMenu.vue'

@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  },
  components: {
    DotMenu
  }
})
export default class ParameterChangeActionCard extends Vue {
  private show: boolean = false

  @Prop({
    default: () => new ParameterChangeAction(),
    required: true,
    type: Object
  })
  readonly value!: ParameterChangeAction

  get title (): string {
    let title = 'Parameter value change'
    if (this.value.parameter) {
      title = `${this.value.parameter.label} changed`
    }
    return title
  }
}
</script>

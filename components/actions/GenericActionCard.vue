<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
          {{ actionDate }}
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
      {{ value.actionTypeName }}
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
      <div
        v-show="show"
      >
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <label>Description</label>
          {{ value.description }}
        </v-card-text>
        <v-card-text
          v-if="value.attachments.length > 0"
          class="grey lighten-5 text--primary pt-2"
        >
          <label>Attachments</label>
          <div v-for="(attachment, index) in value.attachments" :key="index">
            <v-icon small class="text-decoration-none">
              mdi-open-in-new
            </v-icon> <a :href="attachment.url" target="_blank">{{ attachment.label }}</a>
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a Generic Device Actions card
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { GenericAction } from '@/models/GenericAction'

import DotMenu from '@/components/DotMenu.vue'

/**
 * A class component for Generic Device Action card
 * @extends Vue
 */
@Component({
  components: {
    DotMenu
  }
})
// @ts-ignore
export default class GenericActionCard extends Vue {
  private show: boolean = false

  /**
   * a GenericAction
   */
  @Prop({
    default: () => new GenericAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: GenericAction

  get actionDate (): string {
    let actionDate = dateToDateTimeString(this.value.beginDate)
    if (this.value.endDate) {
      actionDate += ' - ' + dateToDateTimeString(this.value.endDate)
    }
    return actionDate
  }
}
</script>

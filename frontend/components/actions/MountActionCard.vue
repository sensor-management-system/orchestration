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
  <base-expandable-list-item :expandable-color="'grey lighten-5'">
    <template #header>
      <v-card-subtitle class="pb-0">
        <span>{{ value.basicData.beginDate | toUtcDate }}</span>
        <span class="text-caption text--secondary">(UTC)</span>
        by {{ value.beginContact.toString() }}
      </v-card-subtitle>
    </template>
    <template #default="{show}">
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            Mounted on {{ value.configuration.label }}
          </v-card-title>
        </v-col>
      </v-row>
      <v-row v-show="!show && value.basicData.beginDescription" no-gutters>
        <v-col>
          <v-card-subtitle class="text--primary pt-0 description-preview">
            {{ value.basicData.beginDescription }}
          </v-card-subtitle>
        </v-col>
      </v-row>
    </template>
    <template #dot-menu-items>
      <slot name="menu" />
    </template>
    <template #actions>
      <slot name="actions" />
      <v-btn
        :to="'/configurations/' + value.configuration.id"
        color="primary"
        text
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #expandable>
      <div
        class="text--primary pt-0 px-3"
      >
        <v-row v-if="value.parentPlatform !== null" dense>
          <v-col>
            <label>Parent platform</label>{{ value.parentPlatform.shortName }}
          </v-col>
        </v-row>
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
        <v-row dense>
          <v-col>
            <label>Description</label>
            {{ value.basicData.beginDescription | orDefault }}
          </v-col>
        </v-row>
      </div>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
/**
 * @file provides a component for a Mount Action Action card
 * @author <tobias.kuhnert@ufz.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

/**
 * A class component for Mount Action card
 * @extends Vue
 */
@Component({
  components: { BaseExpandableListItem },
  filters: {
    toUtcDate: dateToDateTimeString
  }
})
// @ts-ignore
export default class PlatformMountActionCard extends Vue {
  private show: boolean = false

  /**
   * a PlatformMountAction
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: PlatformMountAction | DeviceMountAction
}
</script>
<style scoped>
.description-preview {
  vertical-align: middle !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
</style>

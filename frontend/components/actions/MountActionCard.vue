<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
        <v-row v-if="value.parentDevice" dense>
          <v-col>
            <label>Parent device</label>{{ value.parentDevice.shortName }}
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
        <div v-if="value.basicData.x !== null || value.basicData.y !== null || value.basicData.z !== null">
          <v-row
            dense
          >
            <v-col cols="12" md="4">
              <label>x</label>
              {{ value.basicData.x | orDefault }}
            </v-col>
            <v-col cols="12" md="4">
              <label>y</label>
              {{ value.basicData.y | orDefault }}
            </v-col>
            <v-col cols="12" md="4">
              <label>EPSG Code</label>
              {{ value.basicData.epsgCode | orDefault }}
            </v-col>
          </v-row>
          <v-row
            dense
          >
            <v-col cols="12" md="4" />
            <v-col cols="12" md="4">
              <label>z</label>
              {{ value.basicData.z | orDefault }}
            </v-col>
            <v-col cols="12" md="4">
              <label>Elevation Datum</label>
              {{ value.basicData.elevationDatumName | orDefault }}
            </v-col>
          </v-row>
        </div>
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

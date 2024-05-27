<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item :expandable-color="'grey lighten-5'">
    <template #header>
      <v-card-subtitle class="pb-0">
        <span>{{ value.basicData.endDate | toUtcDate }}</span>
        <span class="text-caption text--secondary">(UTC)</span>
        by {{ contact }}
      </v-card-subtitle>
    </template>
    <template #default="{show}">
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            Unmounted on {{ value.configuration.label }}
          </v-card-title>
        </v-col>
      </v-row>
      <v-row v-show="!show && value.basicData.endDescription" no-gutters>
        <v-col>
          <v-card-subtitle class="text--primary pt-0 description-preview">
            {{ value.basicData.endDescription }}
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
            {{ value.basicData.endDescription | orDefault }}
          </v-col>
        </v-row>
      </div>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
/**
 * @file provides a component for a Device Unmount Action card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'

/**
 * A class component for Device Unmount Action card
 * @extends Vue
 */
@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  },
  components: {
    BaseExpandableListItem
  }
})
// @ts-ignore
export default class DeviceUnmountActionCard extends Vue {
  /**
   * a DeviceMountAction
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: DeviceMountAction | PlatformMountAction

  get contact (): ContactBasicData {
    if (this.value.endContact !== null) {
      return this.value.endContact
    }
    return this.value.beginContact
  }
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

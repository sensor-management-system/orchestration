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
  <base-expandable-list-item expandable-color="grey lighten-5">
    <template #header>
      <v-card-subtitle class="pb-0">
        <span> {{ value.currentCalibrationDate | toUtcDate }}</span>
        <span class="text-caption text--secondary">(UTC)</span>
        by {{ value.contact.toString() }}
      </v-card-subtitle>
    </template>
    <template #default="{show}">
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            Device calibration
          </v-card-title>
        </v-col>
      </v-row>
      <v-row v-show="!show && value.description" no-gutters>
        <v-col>
          <v-card-subtitle class="text--primary pt-0 description-preview">
            {{ value.description }}
          </v-card-subtitle>
        </v-col>
      </v-row>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <slot name="actions" />
    </template>
    <template #expandable>
      <v-card-text
        class="grey lighten-5 text--primary pt-2"
      >
        <v-row dense>
          <v-col cols="12" md="4">
            <label>
              Formula
            </label>
            {{ value.formula | orDefault }}
          </v-col>
          <v-col cols="12" md="4">
            <label>
              Value
            </label>
            {{ value.value | orDefault }}
          </v-col>
          <v-col v-if="value.nextCalibrationDate != null" cols="12" md="4">
            <label>
              Next calibration date
            </label>
            {{ value.nextCalibrationDate | toUtcDate }}
            <span class="text-caption text--secondary">(UTC)</span>
          </v-col>
        </v-row>
        <div v-if="value.measuredQuantities && value.measuredQuantities.length > 0">
          <label>Measured quantities</label>
          <ul>
            <li v-for="measuredQuantity in value.measuredQuantities" :key="measuredQuantity.id">
              {{ generateMeasuredQuantityLabel(measuredQuantity) }}
            </li>
          </ul>
        </div>
        <div v-if="value.description">
          <label>Description</label>
          {{ value.description | orDefault }}
        </div>
      </v-card-text>
      <attachments-block :value="value.attachments" :is-public="isPublic" @open-attachment="openAttachment" />
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
/**
 * @file provides a component for a device calibration action card
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { dateToDateTimeString } from '@/utils/dateHelper'

import AttachmentsBlock from '@/components/actions/AttachmentsBlock.vue'
import { Attachment } from '@/models/Attachment'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import { DeviceProperty } from '@/models/DeviceProperty'

@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  },
  components: {
    BaseExpandableListItem,
    AttachmentsBlock
  }
})
export default class DeviceCalibrationActionCard extends Vue {
  private show: boolean = false

  @Prop({
    default: () => new DeviceCalibrationAction(),
    required: true,
    type: Object
  })
  readonly value!: DeviceCalibrationAction

  @Prop({
    type: Boolean,
    default: false
  })
  readonly isPublic!: Boolean

  openAttachment (attachment: Attachment) {
    this.$emit('open-attachment', attachment)
  }

  generateMeasuredQuantityLabel (measuredQuantity: DeviceProperty) {
    if (measuredQuantity) {
      const propertyName = measuredQuantity.propertyName ?? ''
      const label = measuredQuantity.label ?? ''
      const unit = measuredQuantity.unitName ?? ''
      return `${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
    }
    return ''
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

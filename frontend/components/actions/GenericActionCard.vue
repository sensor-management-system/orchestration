<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <base-expandable-list-item expandable-color="grey lighten-5">
    <template #header>
      <v-card-subtitle class="pb-0">
        <span>{{ actionDate }}</span>
        <span class="text-caption text--secondary">(UTC)</span>
        by {{ value.contact.toString() }}
      </v-card-subtitle>
    </template>
    <template #default="{show}">
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            {{ value.actionTypeName }}
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
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-card-text>
      <attachments-block :value="value.attachments" :is-public="isPublic" @open-attachment="openAttachment" />
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
/**
 * @file provides a component for a Generic Device Actions card
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { GenericAction } from '@/models/GenericAction'

import AttachmentsBlock from '@/components/actions/AttachmentsBlock.vue'
import { Attachment } from '@/models/Attachment'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

/**
 * A class component for Generic Device Action card
 * @extends Vue
 */
@Component({
  components: { AttachmentsBlock, BaseExpandableListItem }
})
// @ts-ignore
export default class GenericActionCard extends Vue {
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

  @Prop({
    type: Boolean,
    default: false
  })
  readonly isPublic!: Boolean

  get actionDate (): string {
    let actionDate = dateToDateTimeString(this.value.beginDate)
    if (this.value.endDate) {
      actionDate += ' - ' + dateToDateTimeString(this.value.endDate)
    }
    return actionDate
  }

  openAttachment (attachment: Attachment) {
    this.$emit('open-attachment', attachment)
  }
}
</script>
<style scoped>
.description-preview{
  vertical-align: middle !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
</style>

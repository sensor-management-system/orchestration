<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item expandable-color="grey lighten-5">
    <template #header>
      <v-card-subtitle class="pb-0">
        <span> {{ value.date | toUtcDate }}</span>
        <span class="text-caption text--secondary">(UTC)</span>
        by {{ value.contact.toString() }}
      </v-card-subtitle>
    </template>
    <template #default="{show}">
      <v-row no-gutters>
        <v-col cols="12">
          <v-card-title class="text--primary pt-0 pb-0">
            {{ title }}
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
    </template>
  </base-expandable-list-item>
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
import AttachmentsBlock from '@/components/actions/AttachmentsBlock.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  },
  components: {
    BaseExpandableListItem,
    AttachmentsBlock,
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
<style scoped>
.description-preview {
  vertical-align: middle !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
</style>

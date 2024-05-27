<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <slot name="actions" />
    </template>
    <template #default>
      {{ title }}
    </template>
    <template
      v-if="value.description || actions.length"
      #expandable
    >
      <v-card-text
        v-if="value.description"
        class="py-2"
      >
        {{ value.description }}
      </v-card-text>
      <v-simple-table
        v-if="actions.length"
        dense
      >
        <thead>
          <tr>
            <th
              class="date-column"
            >
              Date (UTC)
            </th>
            <th>Value</th>
            <slot name="action-header" />
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="action in actions"
            :key="`change-action-${action.id}`"
          >
            <td
              class="date-column"
            >
              {{ action.date | toUtcDateTimeStringHHMM }}
            </td>
            <td
              class="py-2"
            >
              <ExpandableText
                :value="action.value"
                :shorten-at="120"
              />
            </td>
            <slot name="parameter-actions" :parameter-action="action" />
          </tr>
        </tbody>
      </v-simple-table>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Parameter } from '@/models/Parameter'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import { sortCriteriaDescending } from '@/utils/dateHelper'

import DotMenu from '@/components/DotMenu.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    DotMenu,
    BaseExpandableListItem,
    ExpandableText
  }
})
export default class ParameterListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private value!: Parameter

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  private parameterChangeActions!: ParameterChangeAction[]

  @Prop({
    required: true
  })
  private index!: number

  get title () {
    if (this.value) {
      const label = this.value.label ?? ''
      const unit = this.value.unitName ?? ''
      return `#${this.index + 1} - ${label} ${unit ? `(${unit})` : ''}`
    }
    return ''
  }

  get actions (): ParameterChangeAction[] {
    return this.parameterChangeActions.filter(action => action.parameter?.id === this.value.id).sort((a, b) => a.date && b.date ? sortCriteriaDescending(a.date, b.date) : 0)
  }
}
</script>
<style lang="scss" scoped>
.v-data-table {
  .date-column {
    width: 200px;
  }
}
</style>

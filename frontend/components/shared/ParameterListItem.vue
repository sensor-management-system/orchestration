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

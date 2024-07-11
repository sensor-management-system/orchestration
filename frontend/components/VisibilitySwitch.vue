<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-radio-group
    v-model="visibility"
    row
    label="Visibility"
    :hint="visibilityHint"
    persistent-hint
    :rules="rules"
    :readonly="readonly"
    :disabled="readonly"
  >
    <v-radio
      v-if="!disabledOptions.includes(visibilityPrivateValue)"
      :value="visibilityPrivateValue"
      :readonly="readonly"
      :disabled="readonly"
      color="red"
    >
      <template #label>
        <visibility-chip
          v-model="visibilityPrivateValue"
          :disabled="visibility !== visibilityPrivateValue"
        />
      </template>
    </v-radio>
    <v-radio
      v-if="!disabledOptions.includes(visibilityInternalValue)"
      :value="visibilityInternalValue"
      :readonly="readonly"
      :disabled="readonly"
      color="orange"
    >
      <template #label>
        <visibility-chip
          v-model="visibilityInternalValue"
          :disabled="visibility !== visibilityInternalValue"
        />
      </template>
    </v-radio>
    <v-radio
      v-if="!disabledOptions.includes(visibilityPublicValue)"
      :value="visibilityPublicValue"
      :readonly="readonly"
      :disabled="readonly"
      color="green"
    >
      <template #label>
        <visibility-chip
          v-model="visibilityPublicValue"
          :disabled="visibility !== visibilityPublicValue"
        />
      </template>
    </v-radio>
  </v-radio-group>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Visibility } from '@/models/Visibility'

import VisibilityChip from '@/components/VisibilityChip.vue'

type ruleFunction = ((value: string) => string | boolean)

@Component({
  components: {
    VisibilityChip
  }
})
export default class VisibilitySwitch extends Vue {
  /**
   * the visibility of the entity
   */
  @Prop({
    required: true,
    type: String
  })
  readonly value!: Visibility

  /**
   * the name of the entity that provides the permission groups
   * (eg. 'device' or 'platform' or 'configuration'
   */
  @Prop({
    default: 'entity',
    required: false,
    type: String
  })
  readonly entityName!: string

  /**
   * an array of validation rules
   */
  @Prop({
    default: () => [],
    type: Array
  })
  readonly rules!: ruleFunction[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: () => [],
    type: Array
  })
  readonly disabledOptions!: Visibility[]

  get visibility (): Visibility {
    return this.value
  }

  set visibility (value: Visibility) {
    this.$emit('input', value)
  }

  get visibilityPrivateValue (): string {
    return Visibility.Private
  }

  get visibilityInternalValue (): string {
    return Visibility.Internal
  }

  get visibilityPublicValue (): string {
    return Visibility.Public
  }

  get visibilityHint (): string {
    if (this.value === Visibility.Private) {
      return 'This ' + this.entityName + ' is visible and editable just for you.'
    }
    if (this.value === Visibility.Internal) {
      return 'This ' + this.entityName + ' is visible for all users who are logged in. Only members of the assigned groups can edit it.'
    }
    return 'This ' + this.entityName + ' is visible for all users. Only members of the assigned groups can edit it.'
  }
}
</script>

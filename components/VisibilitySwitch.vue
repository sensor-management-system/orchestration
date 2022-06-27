<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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

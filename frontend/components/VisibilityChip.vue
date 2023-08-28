<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
  <v-chip
    v-if="value"
    small
    :color="color"
    :text-color="textColor"
    class="mr-1 mb-1"
  >
    {{ text }}
  </v-chip>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Visibility } from '@/models/Visibility'

@Component
export default class VisibilityChip extends Vue {
  @Prop({
    required: true,
    type: String
  })
  readonly value!: Visibility

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly disabled!: boolean

  get text (): string {
    switch (true) {
      case this.value === Visibility.Internal:
        return 'Internal'
      case this.value === Visibility.Public:
        return 'Public'
    }
    return 'Private'
  }

  get textColor (): string {
    if (!this.disabled) {
      switch (true) {
        case this.value === Visibility.Private:
          // fallthrough
        case this.value === Visibility.Internal:
          return 'white'
        case this.value === Visibility.Public:
          return 'black'
      }
    }
    return 'default'
  }

  get color (): string {
    if (!this.disabled) {
      switch (true) {
        case this.value === Visibility.Private:
          return 'red'
        case this.value === Visibility.Internal:
          return 'orange'
        case this.value === Visibility.Public:
          return 'green'
      }
    }
    return 'default'
  }
}
</script>

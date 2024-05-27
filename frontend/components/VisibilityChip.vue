<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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

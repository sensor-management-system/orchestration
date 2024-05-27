<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-chip
    v-if="text && color"
    :color="color"
    text-color="white"
    small
    class="mr-1 mb-1"
  >
    {{ text }}
  </v-chip>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

interface ChipSetting {
  value: boolean | null
  text: string
  color: string
}

@Component
export default class ExportControlChip extends Vue {
  @Prop({
    default: null,
    type: Boolean
  })
  readonly value!: boolean | null

  get settings (): ChipSetting[] {
    return [
      {
        value: null,
        text: 'Dual use unknown',
        color: 'red'
      },
      {
        value: true,
        text: 'Dual use',
        color: 'orange'
      },
      {
        value: false,
        text: 'No dual use',
        color: 'grey'
      }
    ]
  }

  get color (): string | null {
    for (const entry of this.settings) {
      if (entry.value === this.value) {
        return entry.color
      }
    }
    return null
  }

  get text (): string | null {
    for (const entry of this.settings) {
      if (entry.value === this.value) {
        return entry.text
      }
    }
    return null
  }
}
</script>

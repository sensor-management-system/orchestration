<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-chip
    v-if="value"
    :color="color"
    text-color="white"
    small
    class="mr-1 mb-1"
  >
    {{ value }}
  </v-chip>
</template>

<script lang="ts">

import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A class component that displays a colored chip with a status
 * the value property
 * @extends Vue
 */
@Component
export default class StatusChip extends Vue {
  /**
   * the text of the badge
   */
  @Prop({
    default: '',
    type: String
  })
  // @ts-ignore
  readonly value: string

  /**
   * a status color mapping
   *
   * refer to the material colors as listed here:
   * https://dev.vuetifyjs.com/en/styles/colors/#material-colors
   */
  private colors: { [status: string]: string } = {
    // for platforms & devices
    blocked: 'red',
    'in use': 'green',
    'in warehouse': 'blue',
    maintenance: 'blue',
    scrapped: 'blue-grey',
    'under construction': 'brown',

    // for configurations
    active: 'green',
    deprecated: 'red',
    draft: 'blue'
  }

  get color (): string {
    const status: string = this.value.toLowerCase()
    // check if status has a color assigned to it
    if (!(status in this.colors)) {
      return 'grey'
    }
    return this.colors[status]
  }
}
</script>

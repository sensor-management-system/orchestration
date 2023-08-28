<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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

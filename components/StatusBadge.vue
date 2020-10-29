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
  <v-badge
    :color="getColor()"
    :content="value"
    :value="!!value"
    inline
  >
    <slot />
  </v-badge>
</template>

<script lang="ts">
/**
 * @file provides a component for a colorful status badge
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { Vue, Component, Prop } from 'nuxt-property-decorator'

/**
 * A class component that wraps a badge component and sets a color depending on
 * the value property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class StatusBadge extends Vue {
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
    scrapped: 'blue-grey',
    'under construction': 'brown',

    // for configurations
    active: 'green',
    deprecated: 'red',
    draft: 'blue'
  }

  /**
   * returns a color name depending on the status
   *
   * @return {string} a color name as defined in {@link StatusBadge#colors}
   */
  getColor (): string {
    const status: string = this.value.toLowerCase()
    // check if status has a color assigned to it
    if (!(status in this.colors)) {
      return ''
    }
    return this.colors[status]
  }
}
</script>

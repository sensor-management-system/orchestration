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
 * the value property provided
 * @extends Vue
 */
@Component
// @ts-ignore
export default class StatusBadge extends Vue {
  @Prop({
    default: '',
    type: String
  })
  // @ts-ignore
  readonly value: string

  /**
   * refer to the material colors as listed here:
   * https://dev.vuetifyjs.com/en/styles/colors/#material-colors
   */
  private colors: { [status: string]: string } = {
    blocked: 'red',
    'in use': 'green',
    'in warehouse': 'blue',
    scrapped: 'blue-grey',
    'under construction': 'brown'
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

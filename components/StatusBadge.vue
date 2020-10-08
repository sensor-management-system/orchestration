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

enum KnownStatus {
  BLOCKED = 'blocked',
  IN_USE = 'in use',
  IN_WAREHOUSE = 'in warehouse',
  SCRAPPED = 'scrapped',
  UNDER_CONSTRUCTION = 'under construction'
}

type StatusColors = { [key in KnownStatus]: string }

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
  private colors: StatusColors = {
    [KnownStatus.BLOCKED]: 'red',
    [KnownStatus.IN_USE]: 'green',
    [KnownStatus.IN_WAREHOUSE]: 'blue',
    [KnownStatus.SCRAPPED]: 'blue-grey',
    [KnownStatus.UNDER_CONSTRUCTION]: 'brown'
  }

  /**
   * returns a color name depending on the status
   *
   * @return {string} a color name as defined in {@link StatusBadge#colors}
   */
  getColor (): string {
    const status: string = this.value.toLowerCase()
    if (!(Object.values(KnownStatus).includes(status)) || !(status in this.colors)) {
      return ''
    }
    return this.colors[status as keyof StatusColors]
  }
}
</script>

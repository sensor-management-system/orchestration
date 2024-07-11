<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllSites"
    :label="label"
    color="blue"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select sites
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { Site } from '@/models/Site'

type SitesLoaderFunction = () => Promise<Site[]>

/**
 * A class component to select sites
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class SiteSearchSelect extends Vue {
  /**
   * a list of sites
   */
  @Prop({
    default: () => [] as Site[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Site[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * the label of the component
   */
  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string

  /**
   * fetches all sites from the API
   *
   * @return {SitesLoaderFunction} a function that returns a promise which returns a list of sites
   */
  get findAllSites (): SitesLoaderFunction {
    return () => { return this.$api.sites.searchAll() }
  }

  /**
   * returns the list of sites
   *
   * @return {Site[]} a list of sites
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of sites has changed
   *
   * @param {Site[]} newValue - a list of sites
   * @fires SiteSearchSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event SitesSearchSelect#input
     * @type {Sites[]}
     */
    this.$emit('input', newValue)
  }
}
</script>

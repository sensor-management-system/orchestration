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
    :fetch-function="findAllSiteUsages"
    :label="label"
    color="brown"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select site usages
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { SiteUsage } from '@/models/SiteUsage'

type SiteUsagesLoaderFunction = () => Promise<SiteUsage[]>

/**
 * A class component to select site usages
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class SiteUsageSelect extends Vue {
  /**
   * a list of site usages
   */
  @Prop({
    default: () => [] as SiteUsage[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: SiteUsage[]

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
  readonly label!: String

  /**
   * fetches a list of site usages
   *
   * @return {SiteUsageLoaderFunction} a list of site usages
   */
  get findAllSiteUsages (): SiteUsagesLoaderFunction {
    return () => { return this.$api.siteUsages.findAll() }
  }

  /**
   * returns the list of site usages
   *
   * @return {SiteUsage[]} a list of site usages
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of site usages has changed
   *
   * @param {SiteUsage[]} newValue - a list of site usages
   * @fires SiteUsageSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event SiteUsageSelect#input
     * @type {SiteUsage[]}
     */
    this.$emit('input', newValue)
  }
}
</script>

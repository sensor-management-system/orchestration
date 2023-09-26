<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
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

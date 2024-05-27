<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-tabs
    :value="value"
    background-color="grey lighten-3"
    show-arrows
    @change="changeTab"
  >
    <template
      v-for="(tab, index) in tabs"
    >
      <v-tab
        v-if="isString(tab)"
        :key="index"
      >
        {{ tab }}
      </v-tab>
      <v-tab
        v-else-if="isRoute(tab)"
        :key="index"
        :disabled="tab.disabled"
        nuxt
        :to="tab.to"
      >
        {{ tab.name }}
      </v-tab>
      <v-tab
        v-else-if="isLink(tab)"
        :key="index"
        :disabled="tab.disabled"
        :href="tab.href"
      >
        {{ tab.name }}
      </v-tab>
      <v-tab
        v-else
        :key="index"
        :disabled="tab.disabled"
      >
        {{ tab.name }}
      </v-tab>
    </template>
  </v-tabs>
</template>

<script lang="ts">
/**
 * @file provides a component with tabs for the App-Bar
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { TabItemConfiguration } from '@/models/TabItemConfiguration'

/**
 * A class component to provide tabs to an app-bar extension
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AppBarTabsExtension extends Vue {
  /**
   * the active tab
   */
  @Prop({
    default: null
  })
  // @ts-ignore
  readonly value: string | number | null

  /**
   * an array of tabs
   */
  @Prop({
    default: () => [] as TabItemConfiguration[],
    type: Array
  })
  // @ts-ignore
  readonly tabs: TabItemConfiguration[]

  /**
   * changes the current tab
   *
   * @param {number} tab - number of the active tab
   * @fires AppBarExtension#change
   */
  changeTab (tab: number) {
    /**
     * fires an change event
     * @event AppBarExtension#change
     * @type {number}
     */
    this.$emit('change', tab)
  }

  isRoute (tab: TabItemConfiguration): boolean {
    return typeof tab === 'object' && 'to' in tab
  }

  isLink (tab: TabItemConfiguration): boolean {
    return typeof tab === 'object' && 'href' in tab
  }

  isString (tab: TabItemConfiguration): boolean {
    return typeof tab === 'string'
  }
}
</script>

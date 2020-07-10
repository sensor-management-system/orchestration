<template>
  <v-tabs
    :value="activeTab"
    background-color="grey lighten-3"
    @change="changeTab"
  >
    <v-tab
      v-for="(tab, index) in tabs"
      :key="index"
    >
      {{ tab }}
    </v-tab>
  </v-tabs>
</template>

<script lang="ts">
/**
 * @file provides a component with save and cancel buttons for the App-Bar
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component } from 'nuxt-property-decorator'

/**
 * A class component to provide tabs to an app-bar extension
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AppBarTabsExtension extends Vue {
  private activeTab: number = 0

  get tabs (): String[] {
    return [] as String[]
  }

  changeTab (tab: number) {
    this.activeTab = tab
    this.$nuxt.$emit('AppBarExtension:change', tab)
  }
}
</script>

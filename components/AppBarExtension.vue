<template>
  <v-tabs
    :value="activeTab"
    @change="changeTab"
    background-color="grey lighten-3"
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
 * A class component to select persons
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AppBarExtension extends Vue {
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

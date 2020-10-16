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

  created () {
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      if (tab !== this.activeTab) {
        this.activeTab = tab
      }
    })
  }

  get tabs (): String[] {
    return [] as String[]
  }

  changeTab (tab: number) {
    this.activeTab = tab
    this.$nuxt.$emit('AppBarExtension:change', this.activeTab)
  }
}
</script>

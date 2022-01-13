<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020,2021
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
  <div>
    <v-tabs-items
      v-model="activeTab"
    >
      <ConfigurationsSearch
        v-model="searchResults"
        :load-initial-data="true"
      />
    </v-tabs-items>
    <ConfigurationsOverviewCard
      v-for="result in searchResults"
      :key="result.id"
      :configuration="result"
      :is-user-authenticated="$auth.loggedIn"
      @showDeleteDialog="initDeleteDialog"
    />
    <ConfigurationsDeleteDialog
      v-model="showDeleteDialog"
      :configuration-to-delete="configurationToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <v-btn
      v-if="$auth.loggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      nuxt
      to="/configurations/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Configuration } from '@/models/Configuration'

import ConfigurationsOverviewCard from '@/components/configurations/ConfigurationsOverviewCard.vue'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import ConfigurationsDownloader from '@/components/configurations/ConfigurationsDownloader.vue'
import ConfigurationsBasicSearch from '@/components/configurations/ConfigurationsBasicSearch.vue'
import ConfigurationsExtendedSearch from '@/components/configurations/ConfigurationsExtendedSearch.vue'
import ConfigurationsSearch from '@/components/configurations/ConfigurationsSearch.vue'

@Component({
  components: {
    ConfigurationsSearch,
    ConfigurationsExtendedSearch,
    ConfigurationsBasicSearch,
    ConfigurationsDownloader,
    ConfigurationsDeleteDialog,
    ConfigurationsOverviewCard
  }
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private searchResults: Configuration[] = []

  private configurationToDelete: Configuration|null=null

  private showDeleteDialog: boolean=false;

  created () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Search',
        'Extended Search'
      ],
      title: 'Configurations'
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  initDeleteDialog (configuration: Configuration) {
    this.showDeleteDialog = true
    this.configurationToDelete = configuration
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.configurationToDelete = null
  }

  deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.configurationToDelete === null) {
      return
    }

    this.$api.configurations.deleteById(this.configurationToDelete.id).then(() => {
      // remove configuration from search results
      const indexToDelete = this.searchResults.findIndex(configuration => configuration.id === this.configurationToDelete?.id)
      if (indexToDelete > -1) {
        this.searchResults.splice(indexToDelete, 1)
      }
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    }).finally(() => {
      this.configurationToDelete = null
    })
  }
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

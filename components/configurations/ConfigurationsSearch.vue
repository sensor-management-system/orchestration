<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
      <v-tab-item :eager="true">
        <ConfigurationsBasicSearch
          @search="basicSearch"
        />
      </v-tab-item>
      <v-tab-item :eager="true">
        <ConfigurationsExtendedSearch
          @search="extendedSearch"
        />
      </v-tab-item>
    </v-tabs-items>

    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />

    <div v-if="!totalCount && !loading">
      <p class="text-center">
        There are no configurations that match your search criteria.
      </p>
    </div>

    <div
      v-if="totalCount"
    >
      <v-subheader>
        {{ numbersFoundMessage }}
        <v-spacer />

        <ConfigurationsDownloader
          v-if="lastActiveSearcher != null"
          :last-active-searcher="lastActiveSearcher"
        />
      </v-subheader>

      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="loadAndSetPage"
      />
      <ConfigurationsOverviewCard
        v-for="result in getSearchResultForPage(page)"
        :key="result.id"
        :configuration="result"
        :is-user-authenticated="$auth.loggedIn"
        @showDeleteDialog="initDeleteDialog"
      />
      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="loadAndSetPage"
      />
    </div>
    <ConfigurationsDeleteDialog
      v-model="showDeleteDialog"
      :configuration-to-delete="configurationToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Project } from '@/models/Project'
import { Configuration } from '@/models/Configuration'
import { IConfigurationSearchOption } from '@/models/SearchTypes'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { ConfigurationSearcher } from '@/services/sms/ConfigurationApi'

import ConfigurationsBasicSearch from '@/components/configurations/ConfigurationsBasicSearch.vue'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import ConfigurationsDownloader from '@/components/configurations/ConfigurationsDownloader.vue'
import ConfigurationsExtendedSearch from '@/components/configurations/ConfigurationsExtendedSearch.vue'
import ConfigurationsOverviewCard from '@/components/configurations/ConfigurationsOverviewCard.vue'

export type PaginatedResult = {
  [page: number]: Configuration[]
}

export type ConfigurationCallbackFunc = (value: Configuration) => Promise<void>

@Component({
  components: {
    ConfigurationsBasicSearch,
    ConfigurationsDeleteDialog,
    ConfigurationsDownloader,
    ConfigurationsExtendedSearch,
    ConfigurationsOverviewCard
  }
})
export default class ConfigurationsSearch extends Vue {
  private totalCount: number = 0
  private lastActiveSearcher: ConfigurationSearcher | null = null
  private loader: null | IPaginationLoader<Configuration> = null
  private loading: boolean = true
  private page: number = 0
  private pageSize: number = 20
  private searchResults: PaginatedResult = {}

  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  @Prop({
    default: 0,
    required: false,
    type: Number
  })
  readonly activeTab!: number

  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  private loadInitialData!: boolean

  @Prop({
    required: false,
    type: Function
  })
  readonly deleteCallback!: undefined | ConfigurationCallbackFunc

  created () {
    if (this.loadInitialData) {
      this.basicSearch('')
    }
  }

  get numbersFoundMessage () {
    let message = ''
    if (this.totalCount === 1) {
      message = '1 configuration found'
    }
    if (this.totalCount > 1) {
      message = `${this.totalCount} configurations found`
    }
    return message
  }

  basicSearch (searchText: string = '') {
    this.runSearch(searchText, [], [])
  }

  extendedSearch ({
    searchText,
    selectedConfigurationStates,
    selectedProjects
  }: IConfigurationSearchOption) {
    this.runSearch(
      searchText,
      selectedConfigurationStates,
      selectedProjects
    )
  }

  async runSearch (
    searchText: string | null,
    configurationStates: string[],
    projects: Project[]
  ) {
    this.totalCount = 0
    this.loading = true
    this.searchResults = {}
    this.loader = null

    this.lastActiveSearcher = this.$api.configurations
      .newSearchBuilder()
      .withText(searchText)
      .withOneStatusOf(configurationStates)
      .withOneMatchingProjectOf(projects)
      .build()

    try {
      this.loader = await this.lastActiveSearcher.findMatchingAsPaginationLoader(this.pageSize)
      this.searchResults[1] = this.loader.elements
      this.totalCount = this.loader.totalCount
      this.page = 1
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.loading = false
    }
  }

  async loadPage (pageNr: number, useCache: boolean = true) {
    // use the results that were already loaded if available
    if (useCache && this.searchResults[pageNr]) {
      return
    }
    if (this.loader != null && this.loader.funToLoadPage != null) {
      try {
        this.loading = true
        const loader = await this.loader.funToLoadPage(pageNr)
        this.loader = loader
        this.searchResults[pageNr] = loader.elements
        this.totalCount = loader.totalCount
      } catch (_error) {
        this.$store.commit('snackbar/setError', 'Loading of configurations failed')
      } finally {
        this.loading = false
      }
    }
  }

  get numberOfPages (): number {
    return Math.ceil(this.totalCount / this.pageSize)
  }

  async loadAndSetPage (page: number, useCache: boolean = true) {
    await this.loadPage(page, useCache)
    this.page = page
  }

  getSearchResultForPage (pageNr: number): Configuration[] | undefined {
    return this.searchResults[pageNr]
  }

  getAllResults (): Configuration[] {
    let result: Configuration[] = []
    Object.entries(this.searchResults).map(i => i[1]).forEach((i: Configuration[]) => {
      result = [...result, ...i]
    })
    return result
  }

  initDeleteDialog (configuration:Configuration) {
    this.showDeleteDialog = true
    this.configurationToDelete = configuration
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.configurationToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.configurationToDelete === null) {
      this.closeDialog()
      return
    }
    if (!this.deleteCallback || typeof this.deleteCallback !== 'function') {
      this.closeDialog()
      return
    }
    this.loading = true
    try {
      await this.deleteCallback(this.configurationToDelete)
      this.closeDialog()
      // if we know that the deleted device was the last of the page, we
      // decrement the page by one
      let page = this.page
      if (this.getSearchResultForPage(page)?.length === 1) {
        page = page > 1 ? page - 1 : 1
      }
      this.loadAndSetPage(page, false)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
.progress-spinner {
  position: absolute;
  top: 40vh;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 32px;
  z-index: 99;
}
</style>

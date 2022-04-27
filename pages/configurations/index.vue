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
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchText"
              label="Label"
              placeholder="Label of configuration"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
            cols="12"
            md="7"
            align-self="center"
          >
            <v-btn
              color="primary"
              small
              @click="basicSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearBasicSearch"
            >
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Label"
              placeholder="Label of configuration"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <StringSelect
              v-model="selectedConfigurationStates"
              label="Select a status"
              :items="configurationStates"
              color="green"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <ProjectSelect
              v-model="selectedProjects"
              label="Select a project"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            align-self="center"
          >
            <v-btn
              color="primary"
              small
              @click="extendedSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
              small
              @click="clearExtendedSearch"
            >
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>
    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="configurations.length <=0 && !loading">
      <p class="text-center">
        There are no platforms that match your search criteria.
      </p>
    </div>
    <div
      v-if="configurations.length >0"
    >
      <v-subheader>
        <template v-if="configurations.length == 1">
          1 configuration found
        </template>
        <template v-else>
          {{ configurations.length }} configurations found
        </template>
        <v-spacer/>
      </v-subheader>

      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
      <BaseList
        :list-items="configurations"
      >
        <template #list-item="{item}">
          <ConfigurationsListItem
            :configuration="item"
          >
            <template #dot-menu-items>
              <DotMenuActionDelete
                :readonly="!$auth.loggedIn"
                @click="initDeleteDialog(item)"
              />
            </template>
          </ConfigurationsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
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

import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import { mapActions, mapState } from 'vuex'
import { ConfigurationSearchParamsSerializer, IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { Project } from '@/models/Project'
import StringSelect from '@/components/StringSelect.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'
import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'
import { QueryParams } from '@/modelUtils/QueryParams'

@Component({
  components: {
    ProjectSelect,
    StringSelect,
    DotMenuActionDelete,
    ConfigurationsDeleteDialog,
    ConfigurationsListItem,
    BaseList
  },
  computed: mapState('configurations', ['configurations', 'pageNumber', 'pageSize', 'totalPages', 'configurationStates','projects']),
  methods: {
    ...mapActions('configurations', ['searchConfigurationsPaginated', 'setPageNumber', 'loadConfigurationsStates','loadProjects', 'deleteConfiguration']),
    ...mapActions('appbar',['initConfigurationsIndexAppBar','setDefaults'])

  }
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private loading = false

  private searchText: string | null = null
  private selectedConfigurationStates: string[] = []
  private selectedProjects: Project[] = []

  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  async created () {
    try {
      this.loading = true
      await this.initConfigurationsIndexAppBar()
      await this.loadConfigurationsStates()
      await this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.loading=false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get page () {
    return this.pageNumber
    this.setPageInUrl()
  }

  set page (newVal) {
    this.setPageNumber(newVal)
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  get searchParams (): IConfigurationSearchParams {
    return {
      searchText: this.searchText,
      states: this.selectedConfigurationStates,
      projects: this.selectedProjects
    }
  }

  isExtendedSearch (): boolean {
    return !!this.selectedProjects.length ||
      !!this.selectedConfigurationStates.length
  }

  async runInitialSearch () {
    this.activeTab = this.isExtendedSearch() ? 1 : 0

    this.page = this.getPageFromUrl()
    await this.runSearch()
  }

  basicSearch (): Promise<void> {
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
    this.page = 1//Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch (): Promise<void> {
    this.page = 1//Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedConfigurationStates = []
    this.selectedProjects = []
    this.initUrlQueryParams()
  }

  async runSearch () {
    try {
      this.loading = true
      this.initUrlQueryParams()
      await this.searchConfigurationsPaginated(this.searchParams)
      this.setPageInUrl()
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.loading = false
    }
  }

  initDeleteDialog (configuration: Configuration) {
    this.showDeleteDialog = true
    this.configurationToDelete = configuration
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.configurationToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.configurationToDelete === null || this.configurations.id === null) {
      this.closeDialog()
      return
    }
    try {
      this.loading = true
      this.deleteConfiguration(this.configurationToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    } catch {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new ConfigurationSearchParamsSerializer({
      states: this.configurationStates,
      projects: this.projects,
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.states) {
      this.selectedConfigurationStates = searchParamsObject.states
    }
    if (searchParamsObject.projects) {
      this.selectedProjects = searchParamsObject.projects
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new ConfigurationSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 1
    }
    return 1;
  }
  setPageInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(this.page)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

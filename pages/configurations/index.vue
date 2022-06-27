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
            cols="5"
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
          <v-col
            align-self="center"
            class="text-right"
          >
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              to="/configurations/new"
            >
              New Configuration
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
          <v-col
            cols="5"
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
          <v-col
            align-self="center"
            class="text-right"
          >
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              to="/configurations/new"
            >
              New Configuration
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
        There are no configurations that match your search criteria.
      </p>
    </div>
    <div
      v-if="configurations.length >0"
    >
      <v-row
        no-gutters
        class="mt-10"
      >
        <v-subheader>
          <template v-if="configurations.length == 1">
            1 configuration found
          </template>
          <template v-else>
            {{ configurations.length }} configurations found
          </template>
          <v-spacer />
        </v-subheader>
        <v-spacer />
        <v-col
          cols="4"
        >
          <v-pagination
            v-model="page"
            :disabled="loading"
            :length="totalPages"
            :total-visible="7"
            @input="runSearch"
          />
        </v-col>
        <v-col
          cols="4"
          class="flex-grow-1 flex-shrink-0"
        >
          <v-subheader>
            <page-size-select
              v-model="size"
              :items="pageSizeItems"
              label="Items per page"
            />
          </v-subheader>
        </v-col>
      </v-row>
      <BaseList
        :list-items="configurations"
      >
        <template #list-item="{item}">
          <ConfigurationsListItem
            :configuration="item"
          >
            <template
              v-if="$auth.loggedIn"
              #dot-menu-items
            >
              <DotMenuActionDelete
                v-if="canDeleteEntity(item)"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { CanDeleteEntityGetter, CanAccessEntityGetter } from '@/store/permissions'

import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import ConfigurationsDeleteDialog from '@/components/configurations/ConfigurationsDeleteDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import StringSelect from '@/components/StringSelect.vue'
import ProjectSelect from '@/components/ProjectSelect.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'

import { Configuration } from '@/models/Configuration'
import { Project } from '@/models/Project'
import { ConfigurationSearchParamsSerializer, IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { QueryParams } from '@/modelUtils/QueryParams'
@Component({
  components: {
    ProjectSelect,
    StringSelect,
    DotMenuActionDelete,
    ConfigurationsDeleteDialog,
    ConfigurationsListItem,
    BaseList,
    PageSizeSelect
  },
  computed: {
    ...mapState('configurations', ['configurations', 'pageNumber', 'pageSize', 'totalPages', 'configurationStates', 'projects']),
    ...mapGetters('configurations', ['pageSizes']),
    ...mapGetters('permissions', ['canDeleteEntity', 'canAccessEntity'])
  },
  methods: {
    ...mapActions('configurations', ['searchConfigurationsPaginated', 'setPageNumber', 'setPageSize', 'loadConfigurationsStates', 'loadProjects', 'deleteConfiguration']),
    ...mapActions('appbar', ['initConfigurationsIndexAppBar', 'setDefaults'])

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

  // vuex definition for typescript check
  canDeleteEntity!: CanDeleteEntityGetter
  canAccessEntity!: CanAccessEntityGetter
  initConfigurationsIndexAppBar!: () => void
  setDefaults!: () => void
  loadConfigurationsStates!: () => void
  pageNumber!: number
  setPageNumber!: (newPageNumber: number) => void
  pageSize!: number
  setPageSize!: (newPageSize: number) => void
  pageSizes!: number[]
  searchConfigurationsPaginated!: (searchParams: IConfigurationSearchParams) => void
  configurations!: Configuration[]
  deleteConfiguration!: (id: string) => void
  configurationStates!: string[]
  projects!: Project[]

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
      this.loading = false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
    this.setPageNumber(newVal)
    this.setPageInUrl(false)
  }

  get size (): number {
    return this.pageSize
  }

  set size (newVal: number) {
    this.setPageSize(newVal)
    this.setSizeInUrl(false)
    this.runSearch()
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
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
    this.size = this.getSizeFromUrl()
    await this.runSearch()
  }

  basicSearch () {
    this.selectedConfigurationStates = []
    this.selectedProjects = []
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch () {
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
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
      this.setSizeInUrl()
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
    if (this.configurationToDelete === null || this.configurationToDelete.id === null) {
      this.closeDialog()
      return
    }
    try {
      this.loading = true
      await this.deleteConfiguration(this.configurationToDelete.id)
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
      projects: this.projects
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

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 1
    }
    return 1
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

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
  }

  setSizeInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.size) {
      // add size to the current url params
      query = {
        ...this.$route.query,
        size: String(this.size)
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

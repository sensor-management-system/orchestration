<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
      :value="activeTab"
      @input="setActiveTab"
    >
      <v-tab-item :eager="true">
        <v-row
          dense
        >
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search configurations"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
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
        <v-row
          dense
        >
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search configurations"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <StringSelect
              v-model="selectedConfigurationStates"
              label="Select a status"
              :items="configurationStates"
              color="green"
              small
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <StringSelect
              v-model="selectedProjects"
              label="Select a project"
              :items="projects"
              color="red"
              small
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <site-search-select v-model="selectedSites" label="Select a site" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <permission-group-search-select v-model="selectedPermissionGroups" label="Select a permission group" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="3">
            <v-checkbox v-model="includeArchivedConfigurations" label="Include archived configurations" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
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
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <FoundEntries v-model="totalCount" entity-name="configuration" />
            <v-spacer />
          </v-subheader>
        </v-col>
        <v-spacer />
        <v-col
          cols="12"
          md="6"
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
          cols="12"
          md="3"
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
              #dot-menu-items
            >
              <DotMenuActionSensorML
                @click="openSensorML(item)"
              />
              <DotMenuActionArchive
                v-if="canArchiveEntity(item)"
                @click="initArchiveDialog(item)"
              />
              <DotMenuActionRestore
                v-if="canRestoreEntity(item)"
                @click="runRestoreConfiguration(item)"
              />
              <DotMenuActionDelete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
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
    <DeleteDialog
      v-if="configurationToDelete"
      v-model="showDeleteDialog"
      title="Delete Configuration"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the configuration <em>{{ configurationToDelete.label }}</em>?
    </DeleteDialog>
    <ConfigurationArchiveDialog
      v-model="showArchiveDialog"
      :configuration-to-archive="configurationToArchive"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, IAppbarState, SetActiveTabAction } from '@/store/appbar'
import { CanDeleteEntityGetter, CanAccessEntityGetter, LoadPermissionGroupsAction, PermissionsState, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'
import { ArchiveConfigurationAction, RestoreConfigurationAction, ExportAsSensorMLAction, LoadConfigurationAction, ConfigurationsState, ReplaceConfigurationInConfigurationsAction, GetSensorMLUrlAction, LoadProjectsAction } from '@/store/configurations'
import { SearchSitesAction, SitesState } from '@/store/sites'

import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import ConfigurationArchiveDialog from '@/components/configurations/ConfigurationArchiveDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import SiteSearchSelect from '@/components/SitesSearchSelect.vue'
import StringSelect from '@/components/StringSelect.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'

import { Configuration } from '@/models/Configuration'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { ConfigurationSearchParamsSerializer, IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { QueryParams } from '@/modelUtils/QueryParams'
import { Site } from '@/models/Site'
import FoundEntries from '@/components/shared/FoundEntries.vue'
@Component({
  components: {
    FoundEntries,
    StringSelect,
    DotMenuActionDelete,
    DotMenuActionSensorML,
    DeleteDialog,
    ConfigurationsListItem,
    BaseList,
    PageSizeSelect,
    PermissionGroupSearchSelect,
    SiteSearchSelect,
    DotMenuActionArchive,
    DotMenuActionRestore,
    ConfigurationArchiveDialog
  },
  computed: {
    ...mapState('configurations', ['configurations', 'pageNumber', 'pageSize', 'totalPages', 'totalCount', 'configurationStates', 'configuration', 'projects']),
    ...mapState('appbar', ['activeTab']),
    ...mapGetters('configurations', ['pageSizes']),
    ...mapGetters('permissions', ['canDeleteEntity', 'canAccessEntity', 'permissionGroups', 'canArchiveEntity', 'canRestoreEntity']),
    ...mapState('sites', ['sites'])
  },
  methods: {
    ...mapActions('configurations', ['searchConfigurationsPaginated', 'loadConfiguration', 'setPageNumber', 'setPageSize', 'loadConfigurationsStates', 'deleteConfiguration', 'archiveConfiguration', 'restoreConfiguration', 'exportAsSensorML', 'replaceConfigurationInConfigurations', 'getSensorMLUrl', 'loadProjects']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setActiveTab']),
    ...mapActions('permissions', ['loadPermissionGroups']),
    ...mapActions('sites', ['searchSites'])
  }
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private loading = false

  private searchText: string | null = null
  private selectedConfigurationStates: string[] = []
  private selectedPermissionGroups: PermissionGroup[] = []
  private selectedProjects: string[] = []
  private selectedSites: Site[] = []
  private includeArchivedConfigurations: boolean = false

  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  private showArchiveDialog: boolean = false
  private configurationToArchive: Configuration | null = null

  // vuex definition for typescript check
  canDeleteEntity!: CanDeleteEntityGetter
  canAccessEntity!: CanAccessEntityGetter
  initConfigurationsIndexAppBar!: () => void
  loadConfigurationsStates!: () => void
  loadProjects!: LoadProjectsAction
  loadPermissionGroups!: LoadPermissionGroupsAction
  pageNumber!: number
  setPageNumber!: (newPageNumber: number) => void
  pageSize!: number
  setPageSize!: (newPageSize: number) => void
  pageSizes!: number[]
  totalCount!: ConfigurationsState['totalCount']
  searchConfigurationsPaginated!: (searchParams: IConfigurationSearchParams) => void
  configurations!: Configuration[]
  deleteConfiguration!: (id: string) => void
  configurationStates!: string[]
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  activeTab!: IAppbarState['activeTab']
  setActiveTab!: SetActiveTabAction
  exportAsSensorML!: ExportAsSensorMLAction
  permissionGroups!: PermissionsState['permissionGroups']
  archiveConfiguration!: ArchiveConfigurationAction
  restoreConfiguration!: RestoreConfigurationAction
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  loadConfiguration!: LoadConfigurationAction
  configuration!: ConfigurationsState['configuration']
  replaceConfigurationInConfigurations!: ReplaceConfigurationInConfigurationsAction
  getSensorMLUrl!: GetSensorMLUrlAction
  searchSites!: SearchSitesAction
  sites!: SitesState['sites']
  projects!: ConfigurationsState['projects']

  async created () {
    try {
      this.loading = true
      this.initializeAppBar()
      await Promise.all([
        this.loadConfigurationsStates(),
        this.loadPermissionGroups(),
        this.loadProjects(),
        this.searchSites()
      ])
      await this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.loading = false
    }
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
    const sizeChanged: boolean = this.size !== newVal

    this.setPageSize(newVal)
    this.setSizeInUrl(false)

    if (sizeChanged) {
      this.runSearch()
    }
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  get searchParams (): IConfigurationSearchParams {
    return {
      searchText: this.searchText,
      states: this.selectedConfigurationStates,
      permissionGroups: this.selectedPermissionGroups,
      projects: this.selectedProjects,
      sites: this.selectedSites,
      includeArchivedConfigurations: this.includeArchivedConfigurations
    }
  }

  isExtendedSearch (): boolean {
    return !!this.selectedPermissionGroups.length ||
      !!this.selectedConfigurationStates.length ||
      !!this.selectedProjects.length ||
      !!this.selectedSites.length ||
      this.includeArchivedConfigurations === true
  }

  async runInitialSearch () {
    this.setActiveTab(this.isExtendedSearch() ? 1 : 0)

    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()
    await this.runSearch()
  }

  basicSearch () {
    this.selectedConfigurationStates = []
    this.selectedProjects = []
    this.selectedSites = []
    this.selectedPermissionGroups = []
    this.includeArchivedConfigurations = false
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
    this.selectedSites = []
    this.selectedPermissionGroups = []
    this.includeArchivedConfigurations = false
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

  initArchiveDialog (configuration: Configuration) {
    this.showArchiveDialog = true
    this.configurationToArchive = configuration
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
    this.configurationToArchive = null
  }

  async archiveAndCloseDialog () {
    if (this.configurationToArchive === null || this.configurationToArchive.id === null) {
      return
    }
    try {
      this.loading = true
      await this.archiveConfiguration(this.configurationToArchive.id)
      await this.loadConfiguration(this.configurationToArchive.id)
      await this.replaceConfigurationInConfigurations(this.configuration!)
      this.$store.commit('snackbar/setSuccess', 'Configuration archived')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Configuration could not be archived')
    } finally {
      this.loading = false
      this.closeArchiveDialog()
    }
  }

  async runRestoreConfiguration (configuration: Configuration) {
    if (configuration.id) {
      this.loading = true
      try {
        await this.restoreConfiguration(configuration.id)
        await this.loadConfiguration(configuration.id)
        await this.replaceConfigurationInConfigurations(this.configuration!)
        this.$store.commit('snackbar/setSuccess', 'Configuration restored')
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Configuration could not be restored')
      } finally {
        this.loading = false
      }
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new ConfigurationSearchParamsSerializer({
      states: this.configurationStates,
      permissionGroups: this.permissionGroups,
      sites: this.sites,
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
    if (searchParamsObject.sites) {
      this.selectedSites = searchParamsObject.sites
    }
    if (searchParamsObject.permissionGroups) {
      this.selectedPermissionGroups = searchParamsObject.permissionGroups
    }
    if (searchParamsObject.includeArchivedConfigurations) {
      this.includeArchivedConfigurations = searchParamsObject.includeArchivedConfigurations
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

  initializeAppBar () {
    this.setTabs([
      'Search',
      'Extended Search'
    ])
    this.setTitle('Configurations')
  }

  async openSensorML (configuration: Configuration) {
    if (configuration.visibility === Visibility.Public) {
      const url = await this.getSensorMLUrl(configuration.id!)
      window.open(url)
    } else {
      try {
        const blob = await this.exportAsSensorML(configuration.id)
        const url = window.URL.createObjectURL(blob)
        window.open(url)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Configuration could not be exported as SensorML')
      }
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

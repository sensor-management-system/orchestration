<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
              :to="newConfigurationLink"
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
            <StringSelect
              v-model="selectedCampaigns"
              label="Select a campaign"
              :items="campaigns"
              color="brown"
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
          <v-col v-if="$auth.loggedIn" cols="12" md="3">
            <v-checkbox v-model="onlyOwnConfigurations" label="Only own configurations" />
          </v-col>
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
    <div v-if="configurations.length <=0 && !isLoading">
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
            :disabled="isLoading"
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
            from="searchResult"
          >
            <template
              #dot-menu-items
            >
              <DotMenuActionSensorML
                @click="openSensorMLDialog(item)"
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
        :disabled="isLoading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <DeleteDialog
      v-if="configurationToDelete"
      v-model="showDeleteDialog"
      title="Delete Configuration"
      :disabled="isLoading"
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
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedConfigurationSensorMLFilename"
      :url="selectedConfigurationSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, IAppbarState, SetActiveTabAction, SetBackToAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanDeleteEntityGetter, CanAccessEntityGetter, LoadPermissionGroupsAction, PermissionsState, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'
import {
  ArchiveConfigurationAction,
  RestoreConfigurationAction,
  ExportAsSensorMLAction,
  LoadConfigurationAction,
  ConfigurationsState,
  ReplaceConfigurationInConfigurationsAction,
  GetSensorMLUrlAction,
  LoadProjectsAction,
  LoadCampaignsAction,
  SearchConfigurationsPaginatedAction
} from '@/store/configurations'
import { SearchSitesAction, SitesState } from '@/store/sites'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import ConfigurationArchiveDialog from '@/components/configurations/ConfigurationArchiveDialog.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import SiteSearchSelect from '@/components/SitesSearchSelect.vue'
import StringSelect from '@/components/StringSelect.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import FoundEntries from '@/components/shared/FoundEntries.vue'

import { Configuration } from '@/models/Configuration'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { ConfigurationSearchParamsSerializer, IConfigurationSearchParams } from '@/modelUtils/ConfigurationSearchParams'
import { Site } from '@/models/Site'
import { QueryParams } from '@/modelUtils/QueryParams'

@Component({
  components: {
    FoundEntries,
    StringSelect,
    DotMenuActionDelete,
    DotMenuActionSensorML,
    DeleteDialog,
    DownloadDialog,
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
    ...mapState('configurations', ['configurations', 'pageNumber', 'pageSize', 'totalPages', 'totalCount', 'configurationStates', 'configuration', 'projects', 'campaigns']),
    ...mapState('appbar', ['activeTab']),
    ...mapGetters('configurations', ['pageSizes']),
    ...mapGetters('permissions', ['canDeleteEntity', 'canAccessEntity', 'permissionGroups', 'canArchiveEntity', 'canRestoreEntity']),
    ...mapState('sites', ['sites']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', [
      'searchConfigurationsPaginated',
      'loadConfiguration',
      'setPageNumber',
      'setPageSize',
      'loadConfigurationsStates',
      'deleteConfiguration',
      'archiveConfiguration',
      'restoreConfiguration',
      'exportAsSensorML',
      'replaceConfigurationInConfigurations',
      'getSensorMLUrl',
      'loadProjects',
      'loadCampaigns'
    ]),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setActiveTab', 'setBackTo', 'setShowBackButton']),
    ...mapActions('permissions', ['loadPermissionGroups']),
    ...mapActions('sites', ['searchSites']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class SearchConfigurationsPage extends Vue {
  private searchText: string | null = null
  private selectedConfigurationStates: string[] = []
  private selectedPermissionGroups: PermissionGroup[] = []
  private selectedProjects: string[] = []
  private selectedCampaigns: string[] = []
  private selectedSites: Site[] = []
  private onlyOwnConfigurations: boolean = false
  private includeArchivedConfigurations: boolean = false

  private showDeleteDialog: boolean = false
  private configurationToDelete: Configuration | null = null

  private showArchiveDialog: boolean = false
  private configurationToArchive: Configuration | null = null

  private showDownloadDialog: boolean = false
  private configurationForSensorML: Configuration | null = null

  // vuex definition for typescript check
  canDeleteEntity!: CanDeleteEntityGetter
  canAccessEntity!: CanAccessEntityGetter
  initConfigurationsIndexAppBar!: () => void
  loadConfigurationsStates!: () => void
  loadProjects!: LoadProjectsAction
  loadCampaigns!: LoadCampaignsAction
  loadPermissionGroups!: LoadPermissionGroupsAction
  pageNumber!: number
  setPageNumber!: (newPageNumber: number) => void
  pageSize!: number
  setPageSize!: (newPageSize: number) => void
  pageSizes!: number[]
  totalCount!: ConfigurationsState['totalCount']
  searchConfigurationsPaginated!: SearchConfigurationsPaginatedAction
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
  campaigns!: ConfigurationsState['campaigns']
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setBackTo!: SetBackToAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    try {
      this.setLoading(true)
      this.initializeAppBar()
      await Promise.all([
        this.loadConfigurationsStates(),
        this.loadPermissionGroups(),
        this.loadProjects(),
        this.loadCampaigns(),
        this.searchSites()
      ])
      await this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.setLoading(false)
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
      onlyOwnConfigurations: this.onlyOwnConfigurations && this.$auth.loggedIn,
      projects: this.selectedProjects,
      campaigns: this.selectedCampaigns,
      sites: this.selectedSites,
      includeArchivedConfigurations: this.includeArchivedConfigurations
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnConfigurations === true ||
      !!this.selectedPermissionGroups.length ||
      !!this.selectedConfigurationStates.length ||
      !!this.selectedProjects.length ||
      !!this.selectedCampaigns.length ||
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
    this.selectedCampaigns = []
    this.selectedSites = []
    this.selectedPermissionGroups = []
    this.onlyOwnConfigurations = false
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
    this.selectedCampaigns = []
    this.selectedSites = []
    this.selectedPermissionGroups = []
    this.onlyOwnConfigurations = false
    this.includeArchivedConfigurations = false
    this.initUrlQueryParams()
  }

  async runSearch () {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchConfigurationsPaginated(this.searchParams)
      await this.setPageAndSizeInUrl()
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of configurations failed')
    } finally {
      this.setLoading(false)
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
      this.setLoading(true)
      await this.deleteConfiguration(this.configurationToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Configuration deleted')
    } catch {
      this.$store.commit('snackbar/setError', 'Configuration could not be deleted')
    } finally {
      this.setLoading(false)
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
      this.setLoading(true)
      await this.archiveConfiguration(this.configurationToArchive.id)
      await this.loadConfiguration(this.configurationToArchive.id)
      await this.replaceConfigurationInConfigurations(this.configuration!)
      this.$store.commit('snackbar/setSuccess', 'Configuration archived')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Configuration could not be archived')
    } finally {
      this.setLoading(false)
      this.closeArchiveDialog()
    }
  }

  async runRestoreConfiguration (configuration: Configuration) {
    if (configuration.id) {
      this.setLoading(true)
      try {
        await this.restoreConfiguration(configuration.id)
        await this.loadConfiguration(configuration.id)
        await this.replaceConfigurationInConfigurations(this.configuration!)
        this.$store.commit('snackbar/setSuccess', 'Configuration restored')
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Configuration could not be restored')
      } finally {
        this.setLoading(false)
      }
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new ConfigurationSearchParamsSerializer({
      states: this.configurationStates,
      permissionGroups: this.permissionGroups,
      sites: this.sites,
      projects: this.projects,
      campaigns: this.campaigns
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnConfigurations) {
      this.onlyOwnConfigurations = searchParamsObject.onlyOwnConfigurations
    }
    if (searchParamsObject.states) {
      this.selectedConfigurationStates = searchParamsObject.states
    }
    if (searchParamsObject.projects) {
      this.selectedProjects = searchParamsObject.projects
    }
    if (searchParamsObject.campaigns) {
      this.selectedCampaigns = searchParamsObject.campaigns
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

  setPageAndSizeInUrl (preserveHash: boolean = true): Promise<Route> {
    // In general it should be possible to just call
    // setPageInUrl()
    // and
    // setSizeInUrl()
    // However, it seems that setSizeInUrl removes the page parameter then.
    // So we do both in one run.
    let query: QueryParams = {
      ...this.$route.query
    }
    if (this.size) {
      // add size to the current url params
      query = {
        ...query,
        size: String(this.size)
      }
    }
    if (this.page) {
      // add query to the current url params
      query = {
        ...query,
        page: String(this.page)
      }
    }
    return this.$router.replace({
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
    this.setShowBackButton(false)
  }

  openSensorMLDialog (configuration: Configuration) {
    this.configurationForSensorML = configuration
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.configurationForSensorML = null
    this.showDownloadDialog = false
  }

  get selectedConfigurationSensorMLFilename (): string {
    if (this.configurationForSensorML != null) {
      return `${this.configurationForSensorML.label}.xml`
    }
    return 'configuration.xml'
  }

  async selectedConfigurationSensorMLUrl (): Promise<string | null> {
    if (!this.configurationForSensorML) {
      return null
    }
    if (this.configurationForSensorML?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.configurationForSensorML.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.configurationForSensorML!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Configuration could not be exported as SensorML')
        return null
      }
    }
  }

  get newConfigurationLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/configurations/new${params}`
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

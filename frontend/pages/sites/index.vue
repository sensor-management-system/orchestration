<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-tabs-items :value="activeTab" @input="setActiveTab">
      <v-tab-item :eager="true">
        <v-row dense>
          <v-col cols="12" md="5">
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search sites & labs"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col align-self="center">
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
          <v-col align-self="center" class="text-right">
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              :to="newSiteLink"
            >
              New Site / Lab
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
              placeholder="Search sites & labs"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <SiteUsageSelect v-model="selectedSearchSiteUsages" label="Select usage" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <SiteTypeSelect v-model="selectedSearchSiteTypes" label="Select type" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <permission-group-search-select v-model="selectedSearchPermissionGroups" label="Select a permission group" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col v-if="$auth.loggedIn" cols="12" md="3">
            <v-checkbox v-model="onlyOwnSites" label="Only own sites & labs" />
          </v-col>
          <v-col cols="12" md="3">
            <v-checkbox v-model="includeArchivedSites" label="Include archived sites & labs" />
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
              to="/sites/new"
            >
              New Site / Lab
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>

    <div v-if="sites.length <= 0 && !isLoading">
      <p class="text-center">
        There are no sites / labs that match your search criteria.
      </p>
    </div>

    <div v-if="sites.length > 0">
      <v-row no-gutters class="mt-10">
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <FoundEntries v-model="totalCount" entity-name="site / lab" entity-name-plural="sites & labs" />
            <v-spacer />

            <template v-if="sites.length > 0" />
          </v-subheader>
        </v-col>

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
      <BaseList :list-items="sites">
        <template #list-item="{ item }">
          <SitesListItem
            :key="item.id"
            :site="item"
            from="searchResult"
          >
            <template
              #dot-menu-items
            >
              <DotMenuActionSensorML
                @click="openSensorMLDialog(item)"
              />
              <DotMenuActionCopy
                v-if="$auth.loggedIn"
                :path="copyLink(item.id)"
              />
              <DotMenuActionArchive
                v-if="canArchiveEntity(item)"
                @click="initArchiveDialog(item)"
              />
              <DotMenuActionRestore
                v-if="canRestoreEntity(item)"
                @click="runRestoreSite(item)"
              />
              <DotMenuActionDelete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
                @click="initDeleteDialog(item)"
              />
            </template>
          </SitesListItem>
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
    <SiteDeleteDialog
      v-model="showDeleteDialog"
      :site-to-delete="siteToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <SiteArchiveDialog
      v-model="showArchiveDialog"
      :site-to-archive="siteToArchive"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedSiteSensorMLFilename"
      :url="selectedSiteSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'

import { mapState, mapActions, mapGetters } from 'vuex'

import { SetActiveTabAction, SetTabsAction, SetTitleAction, SetBackToAction, SetShowBackButtonAction } from '@/store/appbar'

import { Site } from '@/models/Site'

import BaseList from '@/components/shared/BaseList.vue'
import SitesListItem from '@/components/sites/SitesListItem.vue'
import SiteDeleteDialog from '@/components/sites/SiteDeleteDialog.vue'
import SiteArchiveDialog from '@/components/sites/SiteArchiveDialog.vue'
import {
  SitesState,
  SearchSitesPaginatedAction,
  PageSizesGetter,
  SetPageNumberAction,
  SetPageSizeAction,
  LoadSiteAction,
  ArchiveSiteAction,
  DeleteSiteAction,
  RestoreSiteAction,
  ReplaceSiteInSitesAction,
  ExportAsSensorMLAction,
  GetSensorMLUrlAction
} from '@/store/sites'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import SiteUsageSelect from '@/components/SiteUsageSelect.vue'
import SiteTypeSelect from '@/components/SiteTypeSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'

import {
  PermissionsState,
  CanAccessEntityGetter,
  CanDeleteEntityGetter,
  CanArchiveEntityGetter,
  LoadPermissionGroupsAction,
  CanRestoreEntityGetter
} from '@/store/permissions'
import {
  LoadSiteUsagesAction,
  LoadSiteTypesAction,
  VocabularyState
} from '@/store/vocabulary'
import { PermissionGroup } from '@/models/PermissionGroup'
import { QueryParams } from '@/modelUtils/QueryParams'
import { SiteSearchParamsSerializer } from '@/modelUtils/SiteSearchParams'
import { SiteUsage } from '@/models/SiteUsage'
import { SiteType } from '@/models/SiteType'
import FoundEntries from '@/components/shared/FoundEntries.vue'
import { Visibility } from '@/models/Visibility'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

@Component({
  components: {
    FoundEntries,
    BaseList,
    SitesListItem,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenuActionSensorML,
    DotMenuActionArchive,
    DotMenuActionRestore,
    PageSizeSelect,
    SiteArchiveDialog,
    SiteDeleteDialog,
    SiteUsageSelect,
    SiteTypeSelect,
    PermissionGroupSearchSelect,
    DownloadDialog
  },
  computed: {
    ...mapGetters('permissions', ['canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity', 'canAccessEntity', 'permissionGroups']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapState('appbar', ['activeTab']),
    ...mapState('sites', ['sites', 'pageNumber', 'pageSize', 'totalPages', 'totalCount', 'site']),
    ...mapGetters('sites', ['pageSizes']),
    ...mapState('vocabulary', ['siteUsages', 'siteTypes'])

  },
  methods: {
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setActiveTab', 'setBackTo', 'setShowBackButton']),
    ...mapActions('sites', [
      'searchSitesPaginated',
      'setPageNumber',
      'setPageSize',
      'deleteSite',
      'archiveSite',
      'restoreSite',
      'loadSite',
      'replaceSiteInSites',
      'exportAsSensorML',
      'getSensorMLUrl'
    ]),
    ...mapActions('permissions', ['loadPermissionGroups']),
    ...mapActions('vocabulary', ['loadSiteUsages', 'loadSiteTypes']),
    ...mapActions('progressindicator', ['setLoading'])

  }
})
export default class SearchSitesPage extends Vue {
  private selectedSearchSiteUsages: SiteUsage[] = []
  private selectedSearchSiteTypes: SiteType[] = []
  private selectedSearchPermissionGroups: PermissionGroup[] = []
  private onlyOwnSites: boolean = false
  private includeArchivedSites: boolean = false
  private searchText: string | null = null
  private showDeleteDialog: boolean = false
  private siteToDelete: Site | null = null
  private showArchiveDialog: boolean = false
  private siteToArchive: Site | null = null

  private showDownloadDialog: boolean = false
  private siteForSensorML: Site | null = null

  // vuex definition for typescript check
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  searchSitesPaginated!: SearchSitesPaginatedAction
  pageSize!: SitesState['pageSize']
  totalPages!: SitesState['totalPages']
  totalCount!: SitesState['totalCount']
  pageNumber!: SitesState['pageNumber']
  pageSizes!: PageSizesGetter
  permissionGroups!: PermissionsState['permissionGroups']
  loadPermissionGroups!: LoadPermissionGroupsAction
  setActiveTab!: SetActiveTabAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  loadSite!: LoadSiteAction
  deleteSite!: DeleteSiteAction
  archiveSite!: ArchiveSiteAction
  restoreSite!: RestoreSiteAction
  canAccessEntity!: CanAccessEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  site!: SitesState['site']
  sites!: SitesState['sites']
  loadSiteUsages!: LoadSiteUsagesAction
  siteUsages!: VocabularyState['siteUsages']
  loadSiteTypes!: LoadSiteTypesAction
  siteTypes!: VocabularyState['siteTypes']
  replaceSiteInSites !: ReplaceSiteInSitesAction
  exportAsSensorML!: ExportAsSensorMLAction
  getSensorMLUrl!: GetSensorMLUrlAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setBackTo!: SetBackToAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    this.initializeAppBar()
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadPermissionGroups(),
        this.loadSiteUsages(),
        this.loadSiteTypes()
      ])
      this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of sites & labs failed')
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

  get searchParams () {
    return {
      searchText: this.searchText,
      permissionGroups: this.selectedSearchPermissionGroups,
      siteUsages: this.selectedSearchSiteUsages,
      siteTypes: this.selectedSearchSiteTypes,
      onlyOwnSites: this.onlyOwnSites && this.$auth.loggedIn,
      includeArchivedSites: this.includeArchivedSites
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnSites === true ||
      !!this.selectedSearchSiteUsages.length ||
      !!this.selectedSearchSiteTypes.length ||
      !!this.selectedSearchPermissionGroups.length ||
      this.includeArchivedSites === true
  }

  async runInitialSearch (): Promise<void> {
    this.setActiveTab(this.isExtendedSearch() ? 1 : 0)
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  basicSearch () {
    this.selectedSearchPermissionGroups = []
    this.onlyOwnSites = false
    this.includeArchivedSites = false
    this.page = 1 // Important to set page to one otherwise it's possible that you don't anything
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

    this.selectedSearchSiteUsages = []
    this.selectedSearchSiteTypes = []
    this.selectedSearchPermissionGroups = []
    this.onlyOwnSites = false
    this.includeArchivedSites = false
    this.initUrlQueryParams()
  }

  async runSearch (): Promise<void> {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchSitesPaginated(this.searchParams)
      await this.setPageAndSizeInUrl()
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of sites & labs failed')
    } finally {
      this.setLoading(false)
    }
  }

  initDeleteDialog (site: Site) {
    this.showDeleteDialog = true
    this.siteToDelete = site
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.siteToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.siteToDelete === null || this.siteToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteSite(this.siteToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Site / Lab deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Site / Lab could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  initArchiveDialog (site: Site) {
    this.showArchiveDialog = true
    this.siteToArchive = site
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
    this.siteToArchive = null
  }

  async archiveAndCloseDialog () {
    if (this.siteToArchive === null || this.siteToArchive.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archiveSite(this.siteToArchive.id)
      await this.loadSite({
        siteId: this.siteToArchive.id
      })
      await this.replaceSiteInSites(this.site!)
      this.$store.commit('snackbar/setSuccess', 'Site / Lab archived')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Site / Lab could not be archived')
    } finally {
      this.setLoading(false)
      this.closeArchiveDialog()
    }
  }

  async runRestoreSite (site: Site) {
    if (site.id) {
      this.setLoading(true)
      try {
        await this.restoreSite(site.id)
        await this.loadSite({
          siteId: site.id
        })
        await this.replaceSiteInSites(this.site!)
        this.$store.commit('snackbar/setSuccess', 'Site / Lab restored')
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Site / Lab could not be restored')
      } finally {
        this.setLoading(false)
      }
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new SiteSearchParamsSerializer({
      permissionGroups: this.permissionGroups,
      siteUsages: this.siteUsages,
      siteTypes: this.siteTypes
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnSites) {
      this.onlyOwnSites = searchParamsObject.onlyOwnSites
    }
    if (searchParamsObject.includeArchivedSites) {
      this.includeArchivedSites = searchParamsObject.includeArchivedSites
    }

    if (searchParamsObject.permissionGroups) {
      this.selectedSearchPermissionGroups = searchParamsObject.permissionGroups
    }
    if (searchParamsObject.siteUsages) {
      this.selectedSearchSiteUsages = searchParamsObject.siteUsages
    }
    if (searchParamsObject.siteTypes) {
      this.selectedSearchSiteTypes = searchParamsObject.siteTypes
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new SiteSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) ?? 1
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
    this.setTitle('Sites & Labs')
    this.setShowBackButton(false)
  }

  openSensorMLDialog (site: Site) {
    this.siteForSensorML = site
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.siteForSensorML = null
    this.showDownloadDialog = false
  }

  get selectedSiteSensorMLFilename (): string {
    if (this.siteForSensorML != null) {
      return `${this.siteForSensorML.label}.xml`
    }
    return 'site.xml'
  }

  async selectedSiteSensorMLUrl (): Promise<string | null> {
    if (!this.siteForSensorML) {
      return null
    }
    if (this.siteForSensorML?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.siteForSensorML.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.siteForSensorML!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Site could not be exported as SensorML')
        return null
      }
    }
  }

  copyLink (id: string): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/sites/copy/${id}${params}`
  }

  get newSiteLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/sites/new${params}`
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

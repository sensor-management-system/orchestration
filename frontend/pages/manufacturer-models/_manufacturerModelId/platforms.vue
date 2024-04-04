<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
    <v-row dense>
      <v-col cols="12" md="5">
        <v-text-field
          v-model="searchText"
          label="Search term"
          placeholder="Search platforms"
          hint="Please enter at least 3 characters"
          @keydown.enter="runBasicSearch"
        />
      </v-col>
      <v-col align-self="center">
        <v-btn color="primary" small @click="runBasicSearch">
          Search
        </v-btn>
        <v-btn text small @click="clearBasicSearch">
          Clear
        </v-btn>
      </v-col>
      <v-col align-self="center" class="text-right">
        <v-btn
          v-if="$auth.loggedIn"
          color="accent"
          small
          nuxt
          :to="newPlatformLink"
        >
          New Platform
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="platforms.length <=0 && !isLoading">
      <p class="text-center">
        There are no platforms that match your search criteria.
      </p>
    </div>
    <div v-if="platforms.length>0">
      <v-row
        no-gutters
        class="mt-10"
      >
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <found-entries v-model="totalCount" entity-name="platform" />
            <template v-if="platforms.length>0">
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="menu">
                  <v-tooltip top>
                    <template #activator="tooltip">
                      <v-btn
                        icon
                        v-on="{...menu.on, ...tooltip.on}"
                      >
                        <v-icon
                          dense
                        >
                          mdi-file-download
                        </v-icon>
                      </v-btn>
                    </template>
                    <span>Download results</span>
                  </v-tooltip>
                </template>
                <v-list>
                  <v-list-item
                    dense
                    @click.prevent="showCsvDownloadDialog = true"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-icon
                          left
                        >
                          mdi-table
                        </v-icon>
                        CSV
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
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
      <base-list
        :list-items="platforms"
      >
        <template #list-item="{item}">
          <platforms-list-item
            :key="item.id"
            :platform="item"
            from="searchResult"
          >
            <template #title>
              <extended-item-name
                :value="item"
                :skip-manufacturer-name="true"
                :skip-model="true"
              />
            </template>
            <template
              #dot-menu-items
            >
              <dot-menu-action-sensor-m-l
                @click="openSensorMLDialog(item)"
              />
              <dot-menu-action-copy
                v-if="$auth.loggedIn"
                :path="copyLink(item.id)"
              />
              <dot-menu-action-archive
                v-if="canArchiveEntity(item)"
                @click="initArchiveDialog(item)"
              />
              <dot-menu-action-restore
                v-if="canRestoreEntity(item)"
                @click="runRestorePlatform(item)"
              />
              <dot-menu-action-delete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
                @click="initDeleteDialog(item)"
              />
            </template>
          </platforms-list-item>
        </template>
      </base-list>
      <v-pagination
        v-model="page"
        :disabled="isLoading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <delete-dialog
      v-if="platformToDelete"
      v-model="showDeleteDialog"
      title="Delete Platform"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the platform <em>{{ platformToDelete.shortName }}</em>?
    </delete-dialog>
    <platform-archive-dialog
      v-model="showArchiveDialog"
      :platform-to-archive="platformToArchive"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedPlatformSensorMLFilename"
      :url="selectedPlatformSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
    <download-dialog
      v-model="showCsvDownloadDialog"
      filename="platforms.csv"
      :url="exportCsvUrl"
      @cancel="showCsvDownloadDialog = false"
    />
  </div>
</template>
<script lang="ts">

import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadingSpinnerState, SetLoadingAction } from '@/store/progressindicator'
import {
  PlatformsState,
  SetPageNumberAction,
  SetPageSizeAction,
  SearchPlatformsPaginatedAction,
  PageSizesGetter,
  DeletePlatformAction,
  ArchivePlatformAction,
  RestorePlatformAction,
  LoadPlatformAction,
  ReplacePlatformInPlatformsAction,
  ExportAsCsvAction,
  GetSensorMLUrlAction,
  ExportAsSensorMLAction
} from '@/store/platforms'
import { ManufacturermodelsState } from '@/store/manufacturermodels'
import { SetBackToAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanArchiveEntityGetter, CanDeleteEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import { QueryParams } from '@/modelUtils/QueryParams'
import { PlatformSearchParamsSerializer } from '@/modelUtils/PlatformSearchParams'

import { Platform } from '@/models/Platform'
import { Visibility } from '@/models/Visibility'

import FoundEntries from '@/components/shared/FoundEntries.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import PlatformArchiveDialog from '@/components/platforms/PlatformArchiveDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  computed: {
    ...mapGetters('platforms', ['pageSizes']),
    ...mapState('platforms', ['platforms', 'platform', 'pageNumber', 'pageSize', 'totalPages', 'totalCount']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('permissions', ['canAccessEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity']),
    ...mapState('manufacturermodels', ['manufacturerModel'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('appbar', ['setBackTo', 'setShowBackButton']),
    ...mapActions('platforms', [
      'setPageNumber',
      'setPageSize',
      'searchPlatformsPaginated',
      'exportAsCsv',
      'deletePlatform',
      'restorePlatform',
      'archivePlatform',
      'loadPlatform',
      'replacePlatformInPlatforms',
      'getSensorMLUrl',
      'exportAsSensorML'
    ])
  },
  components: {
    BaseList,
    DeleteDialog,
    PlatformsListItem,
    DownloadDialog,
    PlatformArchiveDialog,
    DotMenuActionArchive,
    DotMenuActionCopy,
    DotMenuActionDelete,
    DotMenuActionRestore,
    DotMenuActionSensorML,
    ExtendedItemName,
    FoundEntries,
    PageSizeSelect
  }
})
export default class ManufacturerModelPlatformsSearchPage extends Vue {
  private searchText: string | null = null

  private showDeleteDialog: boolean = false
  private platformToDelete: Platform | null = null

  private showArchiveDialog: boolean = false
  private platformToArchive: Platform | null = null

  private showDownloadDialog: boolean = false
  private platformForSensorML: Platform | null = null

  private showCsvDownloadDialog: boolean = false

  platforms!: PlatformsState['platforms']
  platform!: PlatformsState['platform']
  isLoading!: LoadingSpinnerState['isLoading']
  pageNumber!: PlatformsState['pageNumber']
  pageSize!: PlatformsState['pageSize']
  manufacturerModel!: ManufacturermodelsState['manufacturerModel']
  pageSizes!: PageSizesGetter
  canAccessEntity!: CanAccessEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setLoading!: SetLoadingAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  setBackTo!: SetBackToAction
  exportAsCsv!: ExportAsCsvAction
  deletePlatform!: DeletePlatformAction
  archivePlatform!: ArchivePlatformAction
  restorePlatform!: RestorePlatformAction
  loadPlatform!: LoadPlatformAction
  replacePlatformInPlatforms!: ReplacePlatformInPlatformsAction
  getSensorMLUrl!: GetSensorMLUrlAction
  exportAsSensorML!: ExportAsSensorMLAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    this.setShowBackButton(false)
    try {
      this.setLoading(true)
      this.initSearchQueryParams(this.$route.query)
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
    }
  }

  initSearchQueryParams (queryParams: QueryParams): void {
    const searchParamsObject = (new PlatformSearchParamsSerializer({
      states: [],
      platformTypes: [],
      manufacturer: [],
      permissionGroups: [],
      skipManufacturerName: true,
      skipModel: true
    })).toSearchParams(queryParams)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new PlatformSearchParamsSerializer({ skipManufacturerName: true, skipModel: true })).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  async runInitialSearch (): Promise<void> {
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) ?? 1
    }
    return 1
  }

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
  }

  runBasicSearch () {
    this.page = 1
    this.runSearch()
  }

  async runSearch () {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchPlatformsPaginated(this.searchParams)
      await this.setPageAndSizeInUrl()
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
    }
  }

  clearBasicSearch () {
    this.searchText = null
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

  initDeleteDialog (platform: Platform) {
    this.showDeleteDialog = true
    this.platformToDelete = platform
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.platformToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.platformToDelete === null || this.platformToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deletePlatform(this.platformToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  initArchiveDialog (platform: Platform) {
    this.showArchiveDialog = true
    this.platformToArchive = platform
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
    this.platformToArchive = null
  }

  async archiveAndCloseDialog () {
    if (this.platformToArchive === null || this.platformToArchive.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archivePlatform(this.platformToArchive.id)
      await this.loadPlatform({
        platformId: this.platformToArchive.id,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      await this.replacePlatformInPlatforms(this.platform!)
      this.$store.commit('snackbar/setSuccess', 'Platform archived')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Platform could not be archived')
    } finally {
      this.setLoading(false)
      this.closeArchiveDialog()
    }
  }

  async runRestorePlatform (platform: Platform) {
    if (platform.id) {
      this.setLoading(true)
      try {
        await this.restorePlatform(platform.id)
        await this.loadPlatform({
          platformId: platform.id,
          includeCreatedBy: true,
          includeUpdatedBy: true
        })
        await this.replacePlatformInPlatforms(this.platform!)
        this.$store.commit('snackbar/setSuccess', 'Platform restored')
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Platform could not be restored')
      } finally {
        this.setLoading(false)
      }
    }
  }

  openSensorMLDialog (platform: Platform) {
    this.platformForSensorML = platform
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.platformForSensorML = null
    this.showDownloadDialog = false
  }

  get selectedPlatformSensorMLFilename (): string {
    if (this.platformForSensorML != null) {
      return `${this.platformForSensorML.shortName}.xml`
    }
    return 'platform.xml'
  }

  async selectedPlatformSensorMLUrl (): Promise<string | null> {
    if (!this.platformForSensorML) {
      return null
    }
    if (this.platformForSensorML?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.platformForSensorML.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.platformForSensorML!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Platform could not be exported as SensorML')
        return null
      }
    }
  }

  async exportCsvUrl (): Promise<string> {
    this.setLoading(true)
    const blob = await this.exportAsCsv(this.searchParams)
    this.setLoading(false)
    return window.URL.createObjectURL(blob)
  }

  copyLink (id: string): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/platforms/copy/${id}${params}`
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
      manufacturer: [],
      states: [],
      types: [],
      permissionGroups: [],
      onlyOwnPlatforms: false,
      includeArchivedPlatforms: false,
      manufacturerName: this.manufacturerModel!.manufacturerName,
      model: this.manufacturerModel!.model
    }
  }

  get newPlatformLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/platforms/new${params}`
  }

  get manufacturerModelId () {
    return this.$route.params.manufacturerModelId
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
.v-select__selections input {
  display: none;
}
</style>

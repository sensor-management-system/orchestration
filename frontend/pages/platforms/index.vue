<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <div>
      <PlatformSearch>
        <template #actions>
          <v-btn
            v-if="$auth.loggedIn"
            color="accent"
            small
            nuxt
            :to="newPlatformLink"
          >
            New Platform
          </v-btn>
        </template>
      </PlatformSearch>
    </div>

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
            <FoundEntries v-model="totalCount" entity-name="platform" />
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
            @input="searchPlatformsPaginatedAndHooks"
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
        :list-items="platforms"
      >
        <template #list-item="{item}">
          <PlatformsListItem
            :key="item.id"
            :platform="item"
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
                @click="runRestorePlatform(item)"
              />
              <DotMenuActionDelete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
                @click="initDeleteDialog(item)"
              />
            </template>
          </PlatformsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="isLoading"
        :length="totalPages"
        :total-visible="7"
        @input="searchPlatformsPaginatedAndHooks"
      />
    </div>
    <DeleteDialog
      v-if="platformToDelete"
      v-model="showDeleteDialog"
      title="Delete Platform"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the platform <em>{{ platformToDelete.shortName }}</em>?
    </DeleteDialog>
    <PlatformArchiveDialog
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

import { mapState, mapActions, mapGetters } from 'vuex'

import {
  PlatformsState,
  SearchPlatformsPaginatedAction,
  SetPageNumberAction,
  SetPageSizeAction,
  ExportAsCsvAction,
  DeletePlatformAction,
  PageSizesGetter,
  ArchivePlatformAction,
  RestorePlatformAction,
  ExportAsSensorMLAction,
  LoadPlatformAction,
  ReplacePlatformInPlatformsAction,
  GetSensorMLUrlAction
} from 'store/platforms'
import { SetTitleAction, SetTabsAction, SetBackToAction, SetShowBackButtonAction } from '@/store/appbar'

import { CanAccessEntityGetter, CanDeleteEntityGetter, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import PlatformArchiveDialog from '@/components/platforms/PlatformArchiveDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import PlatformsBasicSearch from '@/components/platforms/PlatformsBasicSearch.vue'
import PlatformsBasicSearchField from '@/components/platforms/PlatformsBasicSearchField.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

import { Platform } from '@/models/Platform'
import { Visibility } from '@/models/Visibility'

import { QueryParams } from '@/modelUtils/QueryParams'
import PlatformSearch from '@/components/platforms/PlatformSearch.vue'
import FoundEntries from '@/components/shared/FoundEntries.vue'

@Component({
  components: {
    FoundEntries,
    PlatformSearch,
    PlatformsBasicSearchField,
    PlatformsBasicSearch,
    PlatformsListItem,
    BaseList,
    DotMenuActionDelete,
    DotMenuActionSensorML,
    DotMenuActionCopy,
    DeleteDialog,
    DownloadDialog,
    ManufacturerSelect,
    PlatformTypeSelect,
    StatusSelect,
    PageSizeSelect,
    PlatformArchiveDialog,
    DotMenuActionArchive,
    DotMenuActionRestore
  },
  computed: {
    ...mapState('platforms', ['platforms', 'pageNumber', 'pageSize', 'totalPages', 'totalCount', 'platform']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('platforms', ['pageSizes']),
    ...mapGetters('permissions', ['canDeleteEntity', 'canAccessEntity', 'canArchiveEntity', 'canRestoreEntity'])
  },
  methods: {
    ...mapActions('platforms', ['searchPlatformsPaginated', 'setPageNumber', 'setPageSize', 'exportAsCsv', 'deletePlatform', 'archivePlatform', 'restorePlatform', 'exportAsSensorML', 'loadPlatform', 'replacePlatformInPlatforms', 'getSensorMLUrl']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setBackTo', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SearchPlatformsPage extends Vue {
  private showDeleteDialog: boolean = false
  private showArchiveDialog: boolean = false
  private showDownloadDialog: boolean = false
  private showCsvDownloadDialog: boolean = false

  private platformToDelete: Platform | null = null
  private platformToArchive: Platform | null = null
  private platformForSensorML: Platform | null = null

  // vuex definition for typescript check
  platforms!: PlatformsState['platforms']
  pageNumber!: PlatformsState['pageNumber']
  pageSize!: PlatformsState['pageSize']
  totalPages!: PlatformsState['totalPages']
  totalCount!: PlatformsState['totalCount']
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  pageSizes!: PageSizesGetter
  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  exportAsCsv!: ExportAsCsvAction
  deletePlatform!: DeletePlatformAction
  canAccessEntity!: CanAccessEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  archivePlatform!: ArchivePlatformAction
  restorePlatform!: RestorePlatformAction
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  exportAsSensorML!: ExportAsSensorMLAction
  loadPlatform!: LoadPlatformAction
  replacePlatformInPlatforms!: ReplacePlatformInPlatformsAction
  platform!: PlatformsState['platform']
  getSensorMLUrl!: GetSensorMLUrlAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setBackTo!: SetBackToAction
  setShowBackButton!: SetShowBackButtonAction

  created () {
    this.initializeAppBar()
  }

  fetch () {
    // search is done by the fetch in the PlatformSearch component.
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()
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

  async searchPlatformsPaginatedAndHooks () {
    await this.searchPlatformsPaginated()
    this.setBackTo({ path: this.$route.path, query: this.$route.query })
  }

  set size (newVal: number) {
    const sizeChanged: boolean = this.size !== newVal

    this.setPageSize(newVal)
    this.setSizeInUrl(false)

    if (sizeChanged) {
      this.searchPlatformsPaginatedAndHooks()
    }
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  async exportCsvUrl (): Promise<string> {
    this.setLoading(true)
    const blob = await this.exportAsCsv()
    this.setLoading(false)
    return window.URL.createObjectURL(blob)
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
      this.searchPlatformsPaginatedAndHooks()
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
          includeUpdatedBy: true,
          includeImages: true
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

  initializeAppBar () {
    this.setTabs([
      'Search',
      'Extended Search'
    ])
    this.setTitle('Platforms')
    this.setShowBackButton(false)
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

  copyLink (id: string): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/platforms/copy/${id}${params}`
  }

  get newPlatformLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/platforms/new${params}`
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

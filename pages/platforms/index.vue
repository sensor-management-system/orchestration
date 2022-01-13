<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
            <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" @keydown.enter="basicSearch" />
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
            <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" @keydown.enter="extendedSearch" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <StatusSelect v-model="selectedSearchStates" label="Select a status" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <PlatformTypeSelect v-model="selectedSearchPlatformTypes" label="Select a platform type" />
          </v-col>
        </v-row>
        <v-row v-if="$auth.loggedIn">
          <v-col cols="12" md="3">
            <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />
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

    <div v-if="loading">
      <div class="text-center pt-2">
        <v-progress-circular indeterminate />
      </div>
    </div>
    <div v-if="searchResults.length == 0 && !loading">
      <v-card>
        <v-card-text>
          <p class="text-center">
            There are no platforms that match your search criteria.
          </p>
        </v-card-text>
      </v-card>
    </div>
    <div v-if="searchResults.length && !loading">
      <v-subheader>
        <template v-if="totalCount == 1">
          1 platform found
        </template>
        <template v-else>
          {{ totalCount }} platforms found
        </template>
        <v-spacer />

        <template v-if="lastActiveSearcher != null">
          <v-dialog v-model="processing" max-width="100">
            <v-card>
              <v-card-text>
                <div class="text-center pt-2">
                  <v-progress-circular indeterminate />
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-menu
            close-on-click
            close-on-content-click
            offset-x
            left
            z-index="999"
          >
            <template #activator="{ on }">
              <v-btn
                icon
                v-on="on"
              >
                <v-icon
                  dense
                >
                  mdi-file-download
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                dense
                @click.prevent="exportCsv"
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
      <v-hover
        v-for="result in searchResults"
        v-slot="{ hover }"
        :key="result.id"
      >
        <v-card
          :disabled="loading"
          :elevation="hover ? 6 : 2"
          class="ma-2"
        >
          <v-card-text
            @click.stop.prevent="showResultItem(result.id)"
          >
            <v-row
              no-gutters
            >
              <v-col>
                <StatusBadge
                  :value="getStatus(result)"
                >
                  <div :class="'text-caption' + (getType(result) === NO_TYPE ? ' text--disabled' : '')">
                    {{ getType(result) }}
                  </div>
                </StatusBadge>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <DotMenu>
                  <template #actions>
                    <DotMenuActionCopy
                      :readonly="!$auth.loggedIn"
                      :path="'/platforms/copy/' + result.id"
                    />
                    <DotMenuActionDelete
                      :readonly="!$auth.loggedIn"
                      @click="initDeleteDialog(result)"
                    />
                  </template>
                </DotMenu>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                {{ result.shortName }}
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <v-btn
                  :to="'/platforms/' + result.id"
                  color="primary"
                  text
                  @click.stop.prevent
                >
                  View
                </v-btn>
                <v-btn
                  icon
                  @click.stop.prevent="showResultItem(result.id)"
                >
                  <v-icon>{{ isResultItemShown(result.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
          <v-expand-transition>
            <v-card
              v-show="isResultItemShown(result.id)"
              flat
              tile
              color="grey lighten-5"
            >
              <v-card-text>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Manufacturer:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.manufacturerName) }}
                  </v-col>
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Model:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.model) }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Serial number:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.serialNumber) }}
                  </v-col>
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Inventory number:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.inventoryNumber) }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col
                    cols="4"
                    xs="4"
                    sm="3"
                    md="2"
                    lg="2"
                    xl="1"
                    class="font-weight-medium"
                  >
                    Description:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="10"
                    lg="10"
                    xl="11"
                    class="nowrap-truncate"
                  >
                    {{ getTextOrDefault(result.description) }}
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-expand-transition>
        </v-card>
      </v-hover>
    </div>
    <PlatformDeleteDialog
      v-model="showDeleteDialog"
      :platform-to-delete="platformToDelete"
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
      to="/platforms/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import StatusBadge from '@/components/StatusBadge.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { PlatformSearcher } from '@/services/sms/PlatformApi'
import PlatformDeleteDialog from '@/components/platforms/PlatformDeleteDialog.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

interface IRunSearchParameters {
  searchText: string | null
  manufacturer: Manufacturer[]
  states: Status[]
  types: PlatformType[]
  onlyOwnPlatforms: boolean
}

class BasicSearchParameters implements IRunSearchParameters {
  private readonly _searchText: string | null

  constructor (searchText: string | null) {
    this._searchText = searchText
  }

  get searchText (): string | null {
    return this._searchText
  }

  get manufacturer (): Manufacturer[] {
    return []
  }

  get states (): Status[] {
    return []
  }

  get types (): PlatformType[] {
    return []
  }

  get onlyOwnPlatforms (): boolean {
    return false
  }
}

@Component({
  components: {
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenu,
    PlatformDeleteDialog,
    ManufacturerSelect,
    PlatformTypeSelect,
    StatusBadge,
    StatusSelect
  }
})
export default class SearchPlatformsPage extends Vue {
  private pageSize: number = 20
  private loading: boolean = true
  private processing: boolean = false

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Platform> = null
  private lastActiveSearcher: PlatformSearcher | null = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []
  private onlyOwnPlatforms: boolean = false

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Platform[] = []
  private searchText: string | null = null

  private showDeleteDialog: boolean = false;

  private searchResultItemsShown: { [id: string]: boolean } = {}

  public readonly NO_TYPE: string = 'Unknown type'

  private platformToDelete: Platform | null = null

  created () {
    this.initializeAppBar()
  }

  mounted () {
    const promisePlatformTypes = this.$api.platformTypes.findAll()
    const promiseStates = this.$api.states.findAll()

    promisePlatformTypes.then((platformTypes) => {
      promiseStates.then((states) => {
        const platformTypeLookup = new Map<string, PlatformType>()
        const statusLookup = new Map<string, Status>()

        for (const platformType of platformTypes) {
          platformTypeLookup.set(platformType.uri, platformType)
        }
        for (const status of states) {
          statusLookup.set(status.uri, status)
        }

        this.platformTypeLookup = platformTypeLookup
        this.statusLookup = statusLookup

        this.runSelectedSearch()
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of states failed')
      })
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading of platform types failed')
    })

    window.onscroll = () => {
      // from https://www.digitalocean.com/community/tutorials/vuejs-implementing-infinite-scroll
      const isOnBottom = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight

      if (isOnBottom && this.canLoadNext()) {
        this.loadNext()
      }
    }
  }

  beforeDestroy () {
    this.unsetResultItemsShown()
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Search',
        'Extended Search'
      ],
      title: 'Platforms',
      saveBtnHidden: true,
      cancelBtnHidden: true
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  runSelectedSearch () {
    if (this.activeTab === 0) {
      this.basicSearch()
    } else {
      this.extendedSearch()
    }
  }

  basicSearch () {
    // only uses the text and the type (sensor or platform)
    this.runSearch(new BasicSearchParameters(this.searchText))
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch () {
    this.runSearch({
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchPlatformTypes,
      onlyOwnPlatforms: this.onlyOwnPlatforms && this.$auth.loggedIn
    })
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
  }

  runSearch (
    searchParameters: IRunSearchParameters
  ) {
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.loader = null

    const searchBuilder = this.$api.platforms
      .newSearchBuilder()
      .withText(searchParameters.searchText)
      .withOneMatchingManufacturerOf(searchParameters.manufacturer)
      .withOneMatchingStatusOf(searchParameters.states)
      .withOneMatchingPlatformTypeOf(searchParameters.types)

    if (searchParameters.onlyOwnPlatforms) {
      const email = this.$auth.user!.email as string
      if (email) {
        searchBuilder.withContactEmail(email)
      }
    }

    this.lastActiveSearcher = searchBuilder.build()
    this.lastActiveSearcher
      .findMatchingAsPaginationLoader(this.pageSize)
      .then(this.loadUntilWeHaveSomeEntries).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of platforms failed')
      })
  }

  loadUntilWeHaveSomeEntries (loader: IPaginationLoader<Platform>) {
    this.loader = loader
    this.loading = false
    this.searchResults = [...this.searchResults, ...loader.elements]
    this.totalCount = loader.totalCount

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader)
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional platforms failed')
      })
    }
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
        this.totalCount = nextLoader.totalCount
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional platforms failed')
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  exportCsv () {
    if (this.lastActiveSearcher != null) {
      this.processing = true
      this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
        this.processing = false
        saveAs(blob, 'platforms.csv')
      }).catch((_err) => {
        this.processing = false
        this.$store.commit('snackbar/setError', 'CSV export failed')
      })
    }
  }

  initDeleteDialog (platform: Platform) {
    this.showDeleteDialog = true
    this.platformToDelete = platform
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.platformToDelete = null
  }

  deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.platformToDelete === null) {
      return
    }

    this.$api.platforms.deleteById(this.platformToDelete.id!).then(() => {
      const searchIndex = this.searchResults.findIndex(r => r.id === this.platformToDelete?.id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
        this.totalCount -= 1
      }

      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    }).finally(() => {
      this.platformToDelete = null
    })
  }

  getType (platform: Platform) {
    if (this.platformTypeLookup.has(platform.platformTypeUri)) {
      const platformType: PlatformType = this.platformTypeLookup.get(platform.platformTypeUri) as PlatformType
      return platformType.name
    }
    if (platform.platformTypeName) {
      return platform.platformTypeName
    }
    return this.NO_TYPE
  }

  getStatus (platform: Platform) {
    if (this.statusLookup.has(platform.statusUri)) {
      const platformStatus: Status = this.statusLookup.get(platform.statusUri) as Status
      return platformStatus.name
    }
    if (platform.statusName) {
      return platform.statusName
    }
    return ''
  }

  showResultItem (id: string) {
    const show = !!this.searchResultItemsShown[id]
    Vue.set(this.searchResultItemsShown, id, !show)
  }

  isResultItemShown (id: string): boolean {
    return this.searchResultItemsShown[id]
  }

  unsetResultItemsShown (): void {
    this.searchResultItemsShown = {}
  }

  getTextOrDefault = (text: string): string => text || '-'
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

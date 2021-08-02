<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
          <v-col cols="12" md="2">
            <v-btn
              color="primary"
              @click="basicSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
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
        <v-row v-if="isLoggedIn">
          <v-col cols="12" md="3">
            <v-checkbox v-model="onlyOwnPlatforms" label="Only own platforms" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <v-btn
              color="primary"
              @click="extendedSearch"
            >
              Search
            </v-btn>
            <v-btn
              text
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
                <v-menu
                  close-on-click
                  close-on-content-click
                  offset-x
                  left
                  z-index="999"
                >
                  <template #activator="{ on }">
                    <v-btn
                      data-role="property-menu"
                      icon
                      small
                      v-on="on"
                    >
                      <v-icon
                        dense
                        small
                      >
                        mdi-dots-vertical
                      </v-icon>
                    </v-btn>
                  </template>

                  <v-list>
                    <v-list-item
                      :disabled="!isLoggedIn"
                      dense
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          :class="isLoggedIn ? 'text' : 'grey-text'"
                        >
                          <v-icon
                            left
                            small
                            :color="isLoggedIn ? 'black' : 'grey'"
                          >
                            mdi-content-copy
                          </v-icon>
                          Copy
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item
                      :disabled="!isLoggedIn"
                      dense
                      @click="showDeleteDialogFor(result.id)"
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          :class="isLoggedIn ? 'red--text' : 'grey--text'"
                        >
                          <v-icon
                            left
                            small
                            :color="isLoggedIn ? 'red' : 'grey'"
                          >
                            mdi-delete
                          </v-icon>
                          Delete
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-menu>
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
          <v-dialog v-model="showDeleteDialog[result.id]" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete platform
              </v-card-title>
              <v-card-text>
                Do you really want to delete the platform <em>{{ result.shortName }}</em>?
              </v-card-text>
              <v-card-actions>
                <v-btn
                  text
                  @click="hideDeleteDialogFor(result.id)"
                >
                  No
                </v-btn>
                <v-spacer />
                <v-btn
                  color="error"
                  text
                  @click="deleteAndCloseDialog(result.id)"
                >
                  <v-icon left>
                    mdi-delete
                  </v-icon>
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-hover>
    </div>
    <v-btn
      v-if="isLoggedIn"
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

@Component({
  components: {
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

  private showDeleteDialog: {[index: string]: boolean } = {}

  private searchResultItemsShown: { [id: string]: boolean } = {}

  public readonly NO_TYPE: string = 'Unknown type'

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
    this.showDeleteDialog = {}
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
    this.runSearch(this.searchText, [], [], [], false)
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch () {
    this.runSearch(
      this.searchText,
      this.selectedSearchManufacturers,
      this.selectedSearchStates,
      this.selectedSearchPlatformTypes,
      this.onlyOwnPlatforms && this.isLoggedIn
    )
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
    this.onlyOwnPlatforms = false
  }

  runSearch (
    searchText: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    platformTypes: PlatformType[],
    onlyOwnPlatforms: boolean
  ) {
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
    this.loader = null

    const searchBuilder = this.$api.platforms
      .newSearchBuilder()
      .withText(searchText)
      .withOneMatchingManufacturerOf(manufacturer)
      .withOneMatchingStatusOf(states)
      .withOneMatchingPlatformTypeOf(platformTypes)

    if (onlyOwnPlatforms) {
      const email = this.currentUserEmail
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

  loadUntilWeHaveSomeEntries (loader:IPaginationLoader<Platform>) {
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

  deleteAndCloseDialog (id: string) {
    this.$api.platforms.deleteById(id).then(() => {
      this.showDeleteDialog = {}

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
        this.totalCount -= 1
      }

      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    }).catch((_error) => {
      this.showDeleteDialog = {}
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
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

  showDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, true)
  }

  hideDeleteDialogFor (id: string) {
    Vue.set(this.showDeleteDialog, id, false)
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

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get currentUserEmail () {
    return this.$store.getters['oidc/userEmail']
  }
}

</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
</style>

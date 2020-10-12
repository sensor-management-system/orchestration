<template>
  <div>
    <v-tabs-items
      v-model="activeTab"
    >
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="5">
            <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" />
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
            <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" />
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
      </v-subheader>
      <v-hover
        v-for="result in searchResults"
        v-slot:default="{ hover }"
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
                  <template v-slot:activator="{ on }">
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
                      dense
                    >
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-icon
                            left
                            small
                          >
                            mdi-content-copy
                          </v-icon>
                          Copy
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item
                      dense
                      @click="showDeleteDialogFor(result.id)"
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          class="red--text"
                        >
                          <v-icon
                            left
                            small
                            color="red"
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
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/platforms"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<style lang="scss">
@import "~/assets/styles/_search.scss";
</style>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import StatusBadge from '@/components/StatusBadge.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import Manufacturer from '@/models/Manufacturer'
import Platform from '@/models/Platform'
import PlatformType from '@/models/PlatformType'
import Status from '@/models/Status'

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Search',
      'Extended Search'
    ]
  }
}

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
  private activeTab: number = 0
  private loading: boolean = true

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Platform> = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Platform[] = []
  private searchText: string | null = null

  private showDeleteDialog: {[index: string]: boolean } = {}

  private searchResultItemsShown: { [id: string]: boolean } = {}

  public readonly NO_TYPE: string = 'Unknown type'

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
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
    // make sure that all components (especially the dynamically passed ones) are rendered
    this.$nextTick(() => {
      this.$nuxt.$emit('AppBarContent:title', 'Platforms')
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
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarExtension:change')
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
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
    this.runSearch(this.searchText, [], [], [])
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch () {
    this.runSearch(
      this.searchText,
      this.selectedSearchManufacturers,
      this.selectedSearchStates,
      this.selectedSearchPlatformTypes
    )
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchPlatformTypes = []
  }

  runSearch (
    searchText: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    platformTypes: PlatformType[]
  ) {
    this.loading = true
    this.searchResults = []
    this.unsetResultItemsShown()
    this.showDeleteDialog = {}
    this.$api.platforms
      .newSearchBuilder()
      .withTextInName(searchText)
      .withOneMatchingManufacturerOf(manufacturer)
      .withOneMatchingStatusOf(states)
      .withOneMatchingPlatformTypeOf(platformTypes)
      .build()
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
}

</script>

<template>
  <div>
    <v-card>
      <v-tabs-items
        v-model="activeTab"
      >
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <v-row>
                <v-col cols="12" md="5">
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" />
                </v-col>
                <v-col cols="12" md="2">
                  <v-btn @click="basicSearch">
                    Search
                  </v-btn>
                </v-col>
                <v-col cols="12" md="1">
                  <v-btn @click="clearBasicSearch">
                    Clear
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item :eager="true">
          <v-card>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of platform" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <ManufacturerSelect v-model="selectedSearchManufacturers" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <StatusSelect v-model="selectedSearchStates" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="3">
                  <PlatformTypeSelect v-model="selectedSearchPlatformTypes" />
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="extendedSearch">
                Search
              </v-btn>
              <v-btn @click="clearExtendedSearch">
                Clear
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>

    <h2>Results:</h2>
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
    <div v-else>
      <v-card v-for="result in searchResults" :key="result.id" :disabled="loading">
        <v-card-title>
          {{ result.shortName }}
        </v-card-title>
        <v-card-text>
          <p>{{ getPlatformType(result) }}</p>
          <p>Project {{ getProject(result) }}</p>
          <p>Status {{ getStatus(result) }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn :to="'/platforms/' + result.id">
            View
          </v-btn>
          <v-btn>Copy</v-btn>
          <v-btn @click.stop="showDeleteDialog = true">
            Delete
          </v-btn>
          <v-dialog v-model="showDeleteDialog" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete platform
              </v-card-title>
              <v-card-text>
                Do you really want to delete the platform <em>{{ result.shortName }}</em>?
              </v-card-text>
              <v-card-actions>
                <v-btn @click="showDeleteDialog = false">
                  No
                </v-btn>
                <v-spacer />
                <v-btn color="error" @click="deleteAndCloseDialog(result.id)">
                  <v-icon left>
                    mdi-delete
                  </v-icon>
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </div>
    <v-speed-dial
      v-model="fab"
      fixed
      bottom
      right
      direction="top"
      open-on-hover
    >
      <template v-slot:activator>
        <v-btn
          color="primary"
          dark
          fab
          to="/platforms"
        >
          <v-icon>
            mdi-plus
          </v-icon>
        </v-btn>
      </template>
    </v-speed-dial>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import CVService from '../../services/CVService'
import SmsService from '../../services/SmsService'

import Manufacturer from '../../models/Manufacturer'
import PlatformType from '../../models/PlatformType'
import Platform from '../../models/Platform'
import Status from '../../models/Status'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

// @ts-ignore
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
// @ts-ignore
import StatusSelect from '@/components/StatusSelect.vue'
// @ts-ignore
import PlatformTypeSelect from '@/components/PlatformTypeSelect.vue'

// @ts-ignore
import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
// @ts-ignore
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'

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
    StatusSelect,
    PlatformTypeSelect
  }
})
export default class SeachPlatformsPage extends Vue {
  private pageSize: number = 20
  private activeTab: number = 0
  private fab: boolean = false
  private loading: boolean = true

  private loader: null | IPaginationLoader<Platform> = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchPlatformTypes: PlatformType[] = []

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Platform[] = []
  private searchText: string | null = null

  private showDeleteDialog: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    const promisePlatformTypes = CVService.findAllPlatformTypes()
    const promiseStates = CVService.findAllStates()

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
      })
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
  }

  runSearch (
    searchText: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    platformTypes: PlatformType[]
  ) {
    this.loading = true
    this.searchResults = []
    SmsService.findPlatforms(
      this.pageSize,
      searchText,
      manufacturer,
      states,
      platformTypes
    ).then(this.loadUntilWeHaveSomeEntries)
  }

  loadUntilWeHaveSomeEntries (loader:IPaginationLoader<Platform>) {
    this.loader = loader
    this.loading = false
    this.searchResults = [...this.searchResults, ...loader.elements]

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader)
      })
    }
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  deleteAndCloseDialog (id: number) {
    SmsService.deletePlatform(id).then(() => {
      this.showDeleteDialog = false

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }

      this.$store.commit('snackbar/setSuccess', 'Platform deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Platform could not be deleted')
    })
  }

  getPlatformType (platform: Platform) {
    if (this.platformTypeLookup.has(platform.platformTypeUri)) {
      const platformType: PlatformType = this.platformTypeLookup.get(platform.platformTypeUri) as PlatformType
      return platformType.name
    }
    if (platform.platformTypeName) {
      return platform.platformTypeName
    }
    return 'Unknown type'
  }

  getProject (_platform: Platform) {
    // TODO
    return 'No project yet'
  }

  getStatus (platform: Platform) {
    if (this.statusLookup.has(platform.statusUri)) {
      const platformStatus: Status = this.statusLookup.get(platform.statusUri) as Status
      return platformStatus.name
    }
    if (platform.statusName) {
      return platform.statusName
    }
    return 'Unknown status'
  }
}

</script>

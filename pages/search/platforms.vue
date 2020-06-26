<template>
  <div>
    <v-snackbar v-model="showSuccessMessage" top color="success">
      {{ successMessage }}
      <v-btn fab @click="showSaveSuccess = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-snackbar>
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
                  <v-autocomplete
                    v-model="manufacturerToAdd"
                    label="add manufacturer"
                    :items="notSelectedManufacturers"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-btn
                    fab
                    depressed
                    small
                    :disabled="manufacturerToAdd == null"
                    @click="addSelectedManufacturer"
                  >
                    <v-icon>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <v-chip
                    v-for="(manufacturer, index) in selectedSearchManufacturers"
                    :key="manufacturer.id"
                    class="ma-2"
                    color="brown"
                    text-color="white"
                    :close="true"
                    @click:close="removeManufacturer(index)"
                  >
                    {{ manufacturer }}
                  </v-chip>
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
    <v-card v-for="result in searchResults" :key="result.id">
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

@Component
export default class SeachPlatformsPage extends Vue {
  private activeTab: number = 0
  private fab: boolean = false

  private searchManufacturers: Manufacturer[] = []
  private selectedSearchManufacturers: Manufacturer[] = []
  private manufacturerToAdd: Manufacturer | null = null

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Platform[] = []
  private searchText: string | null = null

  private showDeleteDialog: boolean = false
  private showSuccessMessage: boolean = false
  private successMessage = ''

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    CVService.findAllManufacturers().then((manufacturers) => {
      this.searchManufacturers = manufacturers
    })
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
    this.runSearch(this.searchText, [])
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch () {
    this.runSearch(this.searchText, this.selectedSearchManufacturers)
  }

  clearExtendedSearch () {
    this.clearBasicSearch()
    this.selectedSearchManufacturers = []
    this.manufacturerToAdd = null
  }

  runSearch (searchText: string | null, manufacturer: Manufacturer[]) {
    SmsService.findPlatforms(
      searchText, manufacturer
    ).then((findResults) => {
      this.searchResults = findResults
    })
  }

  addSelectedManufacturer () {
    this.$set(
      this.selectedSearchManufacturers,
      this.selectedSearchManufacturers.length,
      this.manufacturerToAdd
    )
    this.manufacturerToAdd = null
  }

  removeManufacturer (index: number) {
    this.$delete(this.selectedSearchManufacturers, index)
  }

  deleteAndCloseDialog (id: number) {
    SmsService.deletePlatform(id).then(() => {
      this.showDeleteDialog = false

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }

      this.successMessage = 'Platform deleted'
      this.showSuccessMessage = true
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

  get notSelectedManufacturers () {
    const result = []
    const selectedManufactures = new Set()

    for (const singleManufacturer of this.selectedSearchManufacturers) {
      selectedManufactures.add(singleManufacturer)
    }

    for (const singleManufacturer of this.searchManufacturers) {
      if (!selectedManufactures.has(singleManufacturer)) {
        result.push(singleManufacturer)
      }
    }
    return result
  }
}

</script>

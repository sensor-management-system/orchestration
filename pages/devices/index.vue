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
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
                </v-col>
                <v-col cols="12" md="3">
                  <v-select v-model="selectedSearchType" label="Type" :placeholder="searchTypePlaceholder" :items="searchTypes" />
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
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
                </v-col>
                <v-col cols="12" md="3">
                  <v-select v-model="selectedSearchType" label="search type" :placeholder="searchTypePlaceholder" :items="searchTypes" />
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
    <v-card v-for="result in searchResults" :key="result.searchType + result.id">
      <v-card-title>
        {{ result.name }}
      </v-card-title>
      <v-card-text>
        <p>{{ result.type }}</p>
        <p>Project {{ result.project }}</p>
        <p>Status {{ result.status }}</p>
      </v-card-text>
      <v-card-actions v-if="isPlatform(result)">
        <v-btn :to="'/devices/platforms/' + result.id">
          View
        </v-btn>
        <v-btn>Copy</v-btn>
        <v-btn @click.stop="showDeletePlatformDialog = true">
          Delete
        </v-btn>
        <v-dialog v-model="showDeletePlatformDialog" max-width="290">
          <v-card>
            <v-card-title class="headline">
              Delete platform
            </v-card-title>
            <v-card-text>
              Do you really want to delete the platform <em>{{ result.name }}</em>?
            </v-card-text>
            <v-card-actions>
              <v-btn @click="showDeletePlatformDialog = false">
                No
              </v-btn>
              <v-spacer />
              <v-btn color="error" @click="deletePlatformAndCloseDialog(result.id)">
                <v-icon left>
                  mdi-delete
                </v-icon>
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card-actions>
      <v-card-actions v-if="isDevice(result)">
        <v-btn :to="'devices/devices/' + result.id">
          View
        </v-btn>
        <v-btn>Copy</v-btn>
        <v-btn @click.stop="showDeleteDeviceDialog = true">
          Delete
        </v-btn>
        <v-dialog v-model="showDeleteDeviceDialog" max-width="290">
          <v-card>
            <v-card-title class="headline">
              Delete device
            </v-card-title>
            <v-card-text>
              Do you really want to delete the device <em>{{ result.name }}</em>?
            </v-card-text>
            <v-card-actions>
              <v-btn @click="showDeleteDeviceDialog = false">
                No
              </v-btn>
              <v-spacer />
              <v-btn color="error" @click="deleteDeviceAndCloseDialog(result.id)">
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
          v-model="fab"
          color="blue darken-2"
          dark
          fab
        >
          <v-icon v-if="fab">
            mdi-close
          </v-icon>
          <v-icon v-else>
            mdi-plus
          </v-icon>
        </v-btn>
      </template>
      <v-btn
        rounded
        to="/devices/platforms"
        color="primary"
      >
        Add platform
      </v-btn>
      <v-btn
        rounded
        to="/devices/devices"
        color="primary"
      >
        Add device
      </v-btn>
    </v-speed-dial>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import CVService from '../../services/CVService'
import SmsService from '../../services/SmsService'

import { PlatformOrDeviceSearchType } from '../../enums/PlatformOrDeviceSearchType'

import { IDeviceOrPlatformSearchObject } from '../../models/IDeviceOrPlatformSearchObject'
import { PlatformOrDeviceType } from '../../enums/PlatformOrDeviceType'
import Manufacturer from '../../models/Manufacturer'
import PlatformType from '../../models/PlatformType'
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
export default class DevicesIndexPage extends Vue {
  private activeTab: number = 0
  private fab: boolean = false

  private searchManufacturers: Manufacturer[] = []
  private selectedSearchManufacturers: Manufacturer[] = []
  private manufacturerToAdd: Manufacturer | null = null

  private platformTypeLookup: Map<string, PlatformType> = new Map<string, PlatformType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Array<IDeviceOrPlatformSearchObject> = []
  private searchText: string | null = null
  private searchTypes: PlatformOrDeviceSearchType[] = Object.values(PlatformOrDeviceSearchType)

  private selectedSearchType: PlatformOrDeviceSearchType = PlatformOrDeviceSearchType.PLATFORMS_AND_DEVICES

  private showDeletePlatformDialog: boolean = false
  private showDeleteDeviceDialog: boolean = false
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
      this.$nuxt.$emit('AppBarContent:title', 'Devices')
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
    this.runSearch(this.searchText, this.selectedSearchType, [])
  }

  clearBasicSearch () {
    this.searchText = null
    this.selectedSearchType = PlatformOrDeviceSearchType.PLATFORMS_AND_DEVICES
  }

  extendedSearch () {
    this.runSearch(this.searchText, this.selectedSearchType, this.selectedSearchManufacturers)
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []

    this.manufacturerToAdd = null
  }

  runSearch (searchText: string | null, searchType: PlatformOrDeviceSearchType, manufacturer: Manufacturer[]) {
    SmsService.findPlatformsAndSensors(
      searchText, searchType, manufacturer, this.platformTypeLookup, this.statusLookup
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

  deletePlatformAndCloseDialog (id: number) {
    SmsService.deletePlatform(id).then(() => {
      this.showDeletePlatformDialog = false

      const searchIndex = this.searchResults.findIndex(r => r.id === id && r.searchType === PlatformOrDeviceType.PLATFORM)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }

      this.successMessage = 'Platform deleted'
      this.showSuccessMessage = true
    })
  }

  deleteDeviceAndCloseDialog (id: number) {
    SmsService.deleteDevice(id).then(() => {
      this.showDeleteDeviceDialog = false

      const searchIndex = this.searchResults.findIndex(r => r.id === id && r.searchType === PlatformOrDeviceType.DEVICE)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }
      this.successMessage = 'Device deleted'
      this.showSuccessMessage = true
    })
  }

  isPlatform (searchObject: IDeviceOrPlatformSearchObject) {
    return searchObject.searchType === PlatformOrDeviceType.PLATFORM
  }

  isDevice (searchObject: IDeviceOrPlatformSearchObject) {
    return searchObject.searchType === PlatformOrDeviceType.DEVICE
  }

  get searchTypePlaceholder () {
    return PlatformOrDeviceSearchType.PLATFORMS_AND_DEVICES
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

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
                  <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
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
                  <DeviceTypeSelect v-model="selectedSearchDeviceTypes" label="Select a device type" />
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
            There are no devices that match our search criteria.
          </p>
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <v-card v-for="result in searchResults" :key="result.searchType + result.id" :disabled="loading">
        <v-card-title>
          {{ result.shortName }}
        </v-card-title>
        <v-card-text>
          <p>{{ getType(result) }}</p>
          <p>Project {{ getProject(result) }}</p>
          <p>Status {{ getStatus(result) }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn :to="'/devices/' + result.id">
            View
          </v-btn>
          <v-btn>Copy</v-btn>
          <v-btn @click.stop="showDeleteDialog = true">
            Delete
          </v-btn>
          <v-dialog v-model="showDeleteDialog" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete device
              </v-card-title>
              <v-card-text>
                Do you really want to delete the device <em>{{ result.shortName }}</em>?
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
          v-model="fab"
          color="primary"
          dark
          fab
          to="/devices"
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

import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'
import DeviceTypeSelect from '@/components/DeviceTypeSelect.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import CVService from '@/services/CVService'
import SmsService from '@/services/SmsService'

import Device from '@/models/Device'
import DeviceType from '@/models/DeviceType'
import Manufacturer from '@/models/Manufacturer'
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
  components: { ManufacturerSelect, StatusSelect, DeviceTypeSelect }
})
export default class SeachDevicesPage extends Vue {
  private pageSize: number = 20
  private activeTab: number = 0
  private fab: boolean = false
  private loading: boolean = true

  private loader: null | IPaginationLoader<Device> = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []

  private deviceTypeLookup: Map<string, DeviceType> = new Map<string, DeviceType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Device[] = []
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
    const promiseDeviceTypes = CVService.findAllDeviceTypes()
    const promiseStates = CVService.findAllStates()

    promiseDeviceTypes.then((deviceTypes) => {
      promiseStates.then((states) => {
        const deviceTypeTypeLookup = new Map<string, DeviceType>()
        const statusLookup = new Map<string, Status>()

        for (const deviceType of deviceTypes) {
          deviceTypeTypeLookup.set(deviceType.uri, deviceType)
        }
        for (const status of states) {
          statusLookup.set(status.uri, status)
        }

        this.deviceTypeLookup = deviceTypeTypeLookup
        this.statusLookup = statusLookup

        this.runSelectedSearch()
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of states failed')
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of device types failed')
      })
    })
    // make sure that all components (especially the dynamically passed ones) are rendered
    this.$nextTick(() => {
      this.$nuxt.$emit('AppBarContent:title', 'Devices')
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
      this.selectedSearchDeviceTypes
    )
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
  }

  runSearch (
    searchText: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    types: DeviceType[]
  ) {
    this.loading = true
    this.searchResults = []
    SmsService.findDevices(
      this.pageSize, searchText, manufacturer, states, types
    ).then(this.loadUntilWeHaveSomeEntries).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    })
  }

  loadUntilWeHaveSomeEntries (loader: IPaginationLoader<Device>) {
    this.loader = loader
    this.loading = false
    this.searchResults = [...this.searchResults, ...loader.elements]

    if (this.searchResults.length >= this.pageSize || !this.canLoadNext()) {
      this.loading = false
    } else if (this.canLoadNext() && loader.funToLoadNext != null) {
      loader.funToLoadNext().then((nextLoader) => {
        this.loadUntilWeHaveSomeEntries(nextLoader)
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional devices failed')
      })
    }
  }

  loadNext () {
    if (this.loader != null && this.loader.funToLoadNext != null) {
      this.loader.funToLoadNext().then((nextLoader) => {
        this.loader = nextLoader
        this.searchResults = [...this.searchResults, ...nextLoader.elements]
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading of additional devices failed')
      })
    }
  }

  canLoadNext () {
    return this.loader != null && this.loader.funToLoadNext != null
  }

  deleteAndCloseDialog (id: number) {
    SmsService.deleteDevice(id).then(() => {
      this.showDeleteDialog = false

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }

      this.$store.commit('snackbar/setSuccess', 'Device deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    })
  }

  getType (device: Device) {
    if (this.deviceTypeLookup.has(device.deviceTypeUri)) {
      const deviceType: DeviceType = this.deviceTypeLookup.get(device.deviceTypeUri) as DeviceType
      return deviceType.name
    }
    if (device.deviceTypeName) {
      return device.deviceTypeName
    }
    return 'Unknown type'
  }

  getProject (_device: Device) {
    // TODO
    return 'No project yet'
  }

  getStatus (device: Device) {
    if (this.statusLookup.has(device.statusUri)) {
      const deviceStatus: Status = this.statusLookup.get(device.statusUri) as Status
      return deviceStatus.name
    }
    if (device.statusName) {
      return device.statusName
    }
    return 'Unknown status'
  }
}

</script>

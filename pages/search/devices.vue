<template>
  <div>
    <v-tabs-items
      v-model="activeTab"
    >
      <v-tab-item :eager="true">
        <v-row>
          <v-col cols="12" md="5">
            <v-text-field v-model="searchText" label="Name" placeholder="Name of device" />
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
            There are no devices that match our search criteria.
          </p>
        </v-card-text>
      </v-card>
    </div>
    <div v-if="searchResults.length && !loading">
      <v-subheader>
        600 devices found
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
                <v-badge
                  :color="getStatusColor(result)"
                  :content="getStatus(result)"
                  :value="!!getStatus(result)"
                  inline
                >
                  <div :class="'text-caption' + (getType(result) === NO_TYPE ? ' text--disabled' : '')">
                    {{ getType(result) }}
                  </div>
                </v-badge>
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
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-icon
                            left
                          >
                            mdi-content-copy
                          </v-icon>
                          Copy
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item
                      @click.stop.prevent="showDeleteDialogFor(result.id)"
                    >
                      <v-list-item-content>
                        <v-list-item-title
                          class="red--text"
                        >
                          <v-icon
                            left
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
                  :to="'/devices/' + result.id"
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
                  <v-col cols="12" md="4">
                    <span class="font-weight-medium">Manufacturer: </span>{{ result.manufacturerName }}
                  </v-col>
                  <v-col cols="12" md="4">
                    <span class="font-weight-medium">Model: </span>{{ result.model }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col cols="12" md="4">
                    <span class="font-weight-medium">Serial number: </span>{{ result.serialNumber }}
                  </v-col>
                  <v-col cols="12" md="4">
                    <span class="font-weight-medium">Inventory number: </span>{{ result.inventoryNumber }}
                  </v-col>
                </v-row>
                <v-row
                  dense
                >
                  <v-col cols="12">
                    <span class="font-weight-medium">Description: </span>{{ result.description }}
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-expand-transition>
          <v-dialog v-model="showDeleteDialog[result.id]" max-width="290">
            <v-card>
              <v-card-title class="headline">
                Delete device
              </v-card-title>
              <v-card-text>
                Do you really want to delete the device <em>{{ result.shortName }}</em>?
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
      to="/devices"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
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
  private loading: boolean = true

  private loader: null | IPaginationLoader<Device> = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []

  private deviceTypeLookup: Map<string, DeviceType> = new Map<string, DeviceType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: Device[] = []
  private searchText: string | null = null

  private showDeleteDialog: { [id: string]: boolean} = {}

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
    const promiseDeviceTypes = this.$api.deviceTypes.findAll()
    const promiseStates = this.$api.states.findAll()

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
    this.$api.devices
      .newSearchBuilder()
      .withTextInName(searchText)
      .withOneMachtingManufacturerOf(manufacturer)
      .withOneMatchingStatusOf(states)
      .withOneMatchingDeviceTypeOf(types)
      .build()
      .findMatchingAsPaginationLoader(this.pageSize)
      .then(this.loadUntilWeHaveSomeEntries).catch((_error) => {
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

  deleteAndCloseDialog (id: string) {
    this.$api.devices.deleteById(id).then(() => {
      this.showDeleteDialog = {}

      const searchIndex = this.searchResults.findIndex(r => r.id === id)
      if (searchIndex > -1) {
        this.searchResults.splice(searchIndex, 1)
      }

      this.$store.commit('snackbar/setSuccess', 'Device deleted')
    }).catch((_error) => {
      this.showDeleteDialog = {}
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
    return this.NO_TYPE
  }

  getProject (_device: Device) {
    // TODO
    return 'No project yet'
  }

  getStatus (device: Device): string {
    if (this.statusLookup.has(device.statusUri)) {
      const deviceStatus: Status = this.statusLookup.get(device.statusUri) as Status
      return deviceStatus.name
    }
    if (device.statusName) {
      return device.statusName
    }
    return ''
  }

  getStatusColor (device: Device): string {
    const colors: { [key: string]: string } = {
      blocked: 'red',
      'in use': 'green',
      'in warehouse': 'blue',
      scrapped: 'blue-grey',
      'under construction': 'brown'
    }
    const status: string = this.getStatus(device).toLowerCase()
    if (!colors[status]) {
      return ''
    }
    return colors[status]
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
}

</script>

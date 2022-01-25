<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020,2021
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
            <v-text-field
              v-model="searchText"
              label="Name"
              placeholder="Name of device"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
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
            <v-text-field
              v-model="searchText"
              label="Name"
              placeholder="Name of device"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
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
        <v-row v-if="$auth.loggedIn">
          <v-col cols="12" md="3">
            <v-checkbox v-model="onlyOwnDevices" label="Only own devices" />
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

    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="!totalCount && !loading">
      <p class="text-center">
        There are no devices that match your search criteria.
      </p>
    </div>

    <div v-if="totalCount">
      <v-subheader>
        <template v-if="totalCount == 1">
          1 device found
        </template>
        <template v-else>
          {{ totalCount }} devices found
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

      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
      />
      <v-hover
        v-for="result in getSearchResultForPage(page)"
        :id="'item-' + result.id"
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
                      :path="'/devices/copy/' + result.id"
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
      <v-pagination
        :value="page"
        :disabled="loading"
        :length="numberOfPages"
        :total-visible="7"
        @input="setPage"
      />
    </div>
    <DeviceDeleteDialog
      v-model="showDeleteDialog"
      :device-to-delete="deviceToDelete"
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
      nuxt
      to="/devices/new"
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

import DeviceTypeSelect from '@/components/DeviceTypeSelect.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import DeviceDeleteDialog from '@/components/devices/DeviceDeleteDialog.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'

import { DeviceSearcher } from '@/services/sms/DeviceApi'

import { QueryParams } from '@/modelUtils/QueryParams'
import { IDeviceSearchParams, DeviceSearchParamsSerializer } from '@/modelUtils/DeviceSearchParams'

type PaginatedResult = {
  [page: number]: Device[]
}

@Component({
  components: {
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenu,
    DeviceDeleteDialog,
    DeviceTypeSelect,
    ManufacturerSelect,
    StatusBadge,
    StatusSelect
  }
})
export default class SearchDevicesPage extends Vue {
  private pageSize: number = 20
  private page: number = 0
  private loading: boolean = true
  private processing: boolean = false

  private totalCount: number = 0
  private loader: null | IPaginationLoader<Device> = null
  private lastActiveSearcher: DeviceSearcher | null = null

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []
  private onlyOwnDevices: boolean = false

  private manufacturer: Manufacturer[] = []
  private states: Status[] = []
  private deviceTypes: DeviceType[] = []

  private deviceTypeLookup: Map<string, DeviceType> = new Map<string, DeviceType>()
  private statusLookup: Map<string, Status> = new Map<string, Status>()

  private searchResults: PaginatedResult = {}
  private searchText: string | null = null

  private showDeleteDialog: boolean = false

  private searchResultItemsShown: { [id: string]: boolean } = {}

  public readonly NO_TYPE: string = 'Unknown type'

  private deviceToDelete: Device | null = null

  created () {
    this.initializeAppBar()
  }

  async mounted () {
    await this.fetchEntities()
    this.initSearchQueryParams(this.$route.query)
    this.runInitialSearch()
  }

  async fetchEntities (): Promise<void> {
    const deviceTypeTypeLookup = new Map<string, DeviceType>()
    const statusLookup = new Map<string, Status>()

    try {
      const [deviceTypes, states, manufacturer] = await Promise.all([
        this.$api.deviceTypes.findAll(),
        this.$api.states.findAll(),
        this.$api.manufacturer.findAll()
      ])

      this.deviceTypes = deviceTypes
      this.states = states
      this.manufacturer = manufacturer

      for (const deviceType of deviceTypes) {
        deviceTypeTypeLookup.set(deviceType.uri, deviceType)
      }
      for (const status of states) {
        statusLookup.set(status.uri, status)
      }
      this.deviceTypeLookup = deviceTypeTypeLookup
      this.statusLookup = statusLookup
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of entities failed')
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
      title: 'Devices',
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

  isExtendedSearch (): boolean {
    return this.onlyOwnDevices === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchDeviceTypes.length ||
      !!this.selectedSearchManufacturers.length
  }

  async runInitialSearch (): Promise<void> {
    this.activeTab = this.isExtendedSearch() ? 1 : 0

    const page: number | undefined = this.getPageFromUrl()

    await this.runSearch(
      {
        searchText: this.searchText,
        manufacturer: this.selectedSearchManufacturers,
        states: this.selectedSearchStates,
        types: this.selectedSearchDeviceTypes,
        onlyOwnDevices: this.onlyOwnDevices && this.$auth.loggedIn
      },
      page
    )
  }

  basicSearch (): Promise<void> {
    return this.runSearch({
      searchText: this.searchText,
      manufacturer: [],
      states: [],
      types: [],
      onlyOwnDevices: false
    })
  }

  clearBasicSearch () {
    this.searchText = null
  }

  extendedSearch (): Promise<void> {
    return this.runSearch({
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchDeviceTypes,
      onlyOwnDevices: this.onlyOwnDevices && this.$auth.loggedIn
    })
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
    this.onlyOwnDevices = false
  }

  async runSearch (
    searchParameters: IDeviceSearchParams,
    page: number = 1
  ): Promise<void> {
    this.initUrlQueryParams(searchParameters)

    this.totalCount = 0
    this.loading = true
    this.searchResults = {}
    this.unsetResultItemsShown()
    this.loader = null
    this.page = 0

    const searchBuilder = this.$api.devices
      .newSearchBuilder()
      .withText(searchParameters.searchText)
      .withOneMachtingManufacturerOf(searchParameters.manufacturer)
      .withOneMatchingStatusOf(searchParameters.states)
      .withOneMatchingDeviceTypeOf(searchParameters.types)

    if (searchParameters.onlyOwnDevices) {
      const email = this.$auth.user!.email as string
      if (email) {
        searchBuilder.withContactEmail(email)
      }
    }

    this.lastActiveSearcher = searchBuilder.build()
    try {
      const loader = await this.lastActiveSearcher.findMatchingAsPaginationLoaderOnPage(page, this.pageSize)
      this.loader = loader
      this.searchResults[page] = loader.elements
      this.totalCount = loader.totalCount
      this.page = page
      this.setPageInUrl(page)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.loading = false
    }
  }

  async loadPage (pageNr: number, useCache: boolean = true) {
    // use the results that were already loaded if available
    if (useCache && this.searchResults[pageNr]) {
      return
    }
    if (this.loader != null && this.loader.funToLoadPage != null) {
      try {
        this.loading = true
        const loader = await this.loader.funToLoadPage(pageNr)
        this.loader = loader
        this.searchResults[pageNr] = loader.elements
        this.totalCount = loader.totalCount
      } catch (_error) {
        this.$store.commit('snackbar/setError', 'Loading of devices failed')
      } finally {
        this.loading = false
      }
    }
  }

  get numberOfPages (): number {
    return Math.ceil(this.totalCount / this.pageSize)
  }

  async setPage (page: number) {
    await this.loadPage(page)
    this.page = page
    this.setPageInUrl(page, false)
  }

  getSearchResultForPage (pageNr: number): Device[] | undefined {
    return this.searchResults[pageNr]
  }

  exportCsv () {
    if (this.lastActiveSearcher != null) {
      this.processing = true
      this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
        this.processing = false
        saveAs(blob, 'devices.csv')
      }).catch((_err) => {
        this.processing = false
        this.$store.commit('snackbar/setError', 'CSV export failed')
      })
    }
  }

  async deleteAndCloseDialog (id: string) {
    if (this.deviceToDelete === null) {
      return
    }
    this.loading = true
    try {
      await this.$api.devices.deleteById(id)
      // if we know that the deleted device was the last of the page, we
      // decrement the page by one
      if (this.getSearchResultForPage(this.page)?.length === 1) {
        this.page = this.page > 1 ? this.page - 1 : 1
      }
      this.loadPage(this.page, false)
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
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

  initDeleteDialog (device: Device) {
    this.showDeleteDialog = true
    this.deviceToDelete = device
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.deviceToDelete = null
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

  initSearchQueryParams (params: QueryParams): void {
    const searchParamsObject = (new DeviceSearchParamsSerializer({
      states: this.states,
      deviceTypes: this.deviceTypes,
      manufacturer: this.manufacturer
    })).toSearchParams(params)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnDevices) {
      this.onlyOwnDevices = searchParamsObject.onlyOwnDevices
    }
    if (searchParamsObject.manufacturer) {
      this.selectedSearchManufacturers = searchParamsObject.manufacturer
    }
    if (searchParamsObject.types) {
      this.selectedSearchDeviceTypes = searchParamsObject.types
    }
    if (searchParamsObject.states) {
      this.selectedSearchStates = searchParamsObject.states
    }
  }

  initUrlQueryParams (params: IDeviceSearchParams): void {
    this.$router.push({
      query: (new DeviceSearchParamsSerializer()).toQueryParams(params),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 0
    }
  }

  setPageInUrl (page: number, preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(page)
      }
    } else {
      // remove page from the current url params
      const {
        // eslint-disable-next-line
        page,
        ...params
      } = this.$route.query
      query = params
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
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

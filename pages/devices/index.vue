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
    <div v-if="devices.length <=0 && !loading">
      <p class="text-center">
        There are no devices that match your search criteria.
      </p>
    </div>

    <div v-if="devices.length>0">
      <v-subheader>
        <template v-if="devices.length == 1">
          1 device found
        </template>
        <template v-else>
          {{ devices.length }} devices found
        </template>
        <v-spacer />

        <template v-if="devices.length>0">
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
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
      <BaseList
        :list-items="devices"
      >
        <template v-slot:list-item="{item}">
          <DevicesListItem
            :key="item.id"
            :device="item"
          >
            <template #dot-menu-items>
              <DotMenuActionCopy
                :readonly="!$auth.loggedIn"
                :path="'/devices/copy/' + item.id"
              />
              <DotMenuActionDelete
                :readonly="!$auth.loggedIn"
                @click="initDeleteDialog(item)"
              />
            </template>
          </DevicesListItem>
        </template>

      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
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
      style="top:85%"
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
import { mapActions, mapState } from 'vuex'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'

type PaginatedResult = {
  [page: number]: Device[]
}

@Component({
  components: {
    DevicesListItem,
    BaseList,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DeviceDeleteDialog,
    DeviceTypeSelect,
    ManufacturerSelect,
    StatusBadge,
    StatusSelect
  },
  computed:{
    ...mapState('vocabulary',['devicetypes','manufacturers','equipmentstatus']),
    ...mapState('devices',['devices','pageNumber','pageSize','totalPages'])
  },
  methods:{
    ...mapActions('vocabulary',['loadEquipmentstatus','loadDevicetypes','loadManufacturers']),
    ...mapActions('devices',['searchDevicesPaginated','setPageNumber','exportAsCsv','deleteDevice']),
    ...mapActions('appbar',['initDevicesIndexAppBar','setDefaults'])
  }
})
export default class SearchDevicesPage extends Vue {
  private loading: boolean = false
  private processing: boolean = false

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []
  private onlyOwnDevices: boolean = false
  private searchText: string | null = null

  private showDeleteDialog: boolean = false
  private deviceToDelete: Device | null = null

  async created () {
    try {
      this.loading = true
      await this.initDevicesIndexAppBar()
      await this.loadEquipmentstatus()
      await this.loadDevicetypes()
      await this.loadManufacturers()
      await this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.loading=false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get page(){
    return this.pageNumber;
  }

  set page(newVal){
    this.setPageNumber(newVal);
    this.setPageInUrl()
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  get searchParams(){
    return {
      searchText: this.searchText,
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchDeviceTypes,
      onlyOwnDevices: this.onlyOwnDevices && this.$auth.loggedIn
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnDevices === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchDeviceTypes.length ||
      !!this.selectedSearchManufacturers.length
  }

  async runInitialSearch (): Promise<void> {
    this.activeTab = this.isExtendedSearch() ? 1 : 0

    this.page = this.getPageFromUrl()

    await this.runSearch()
  }

  basicSearch (){
    this.selectedSearchManufacturers= []
    this.selectedSearchStates= []
    this.selectedSearchDeviceTypes= []
    this.onlyOwnDevices= false
    this.page = 1//Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch () {
    this.page = 1//Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
    this.onlyOwnDevices = false
    this.initUrlQueryParams()
  }

  async runSearch (): Promise<void> {
    try {
      this.loading=true
      this.initUrlQueryParams()
      await this.searchDevicesPaginated(this.searchParams)
      this.setPageInUrl()
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.loading = false
    }
  }

  exportCsv () {
    if(this.devices.length>0){
      this.processing=true
      this.exportAsCsv(this.searchParams).then((blob) => {
        saveAs(blob, 'devices.csv')
      }).catch((_err) => {
        this.$store.commit('snackbar/setError', 'CSV export failed')
      }).finally(()=>{
        this.processing = false
      })
    }
  }

  initDeleteDialog (device: Device) {
    this.showDeleteDialog = true
    this.deviceToDelete = device
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.deviceToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.deviceToDelete === null || this.deviceToDelete.id === null) {
      return
    }
    this.loading = true
    try {
      await this.deleteDevice(this.deviceToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new DeviceSearchParamsSerializer({
      states: this.states,
      deviceTypes: this.deviceTypes,
      manufacturer: this.manufacturer
    })).toSearchParams(this.$route.query)

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

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new DeviceSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page)
    }
    return 1
  }

  setPageInUrl (page: number, preserveHash: boolean = true): void {
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

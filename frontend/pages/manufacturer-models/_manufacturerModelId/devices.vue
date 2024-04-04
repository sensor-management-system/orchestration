<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
    <v-row dense>
      <v-col cols="12" md="5">
        <v-text-field
          v-model="searchText"
          label="Search term"
          placeholder="Search devices"
          hint="Please enter at least 3 characters"
          @keydown.enter="runBasicSearch"
        />
      </v-col>
      <v-col align-self="center">
        <v-btn color="primary" small @click="runBasicSearch">
          Search
        </v-btn>
        <v-btn text small @click="clearBasicSearch">
          Clear
        </v-btn>
      </v-col>
      <v-col align-self="center" class="text-right">
        <v-btn
          v-if="$auth.loggedIn"
          color="accent"
          small
          nuxt
          :to="newDeviceLink"
        >
          New Device
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="devices.length <=0 && !isLoading">
      <p class="text-center">
        There are no devices that match your search criteria.
      </p>
    </div>
    <div v-if="devices.length>0">
      <v-row
        no-gutters
        class="mt-10"
      >
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <found-entries v-model="totalCount" entity-name="device" />
            <template v-if="devices.length>0">
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="menu">
                  <v-tooltip top>
                    <template #activator="tooltip">
                      <v-btn
                        icon
                        v-on="{...menu.on, ...tooltip.on}"
                      >
                        <v-icon
                          dense
                        >
                          mdi-file-download
                        </v-icon>
                      </v-btn>
                    </template>
                    <span>Download results</span>
                  </v-tooltip>
                </template>
                <v-list>
                  <v-list-item
                    dense
                    @click.prevent="showCsvDownloadDialog = true"
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
        </v-col>
        <v-col
          cols="12"
          md="6"
        >
          <v-pagination
            v-model="page"
            :disabled="isLoading"
            :length="totalPages"
            :total-visible="7"
            @input="runSearch"
          />
        </v-col>
        <v-col
          cols="12"
          md="3"
          class="flex-grow-1 flex-shrink-0"
        >
          <v-subheader>
            <page-size-select
              v-model="size"
              :items="pageSizeItems"
              label="Items per page"
            />
          </v-subheader>
        </v-col>
      </v-row>
      <base-list
        :list-items="devices"
      >
        <template #list-item="{item}">
          <devices-list-item
            :key="item.id"
            :device="item"
            from="searchResult"
          >
            <template #title>
              <extended-item-name
                :value="item"
                :skip-manufacturer-name="true"
                :skip-model="true"
              />
            </template>
            <template
              #dot-menu-items
            >
              <dot-menu-action-sensor-m-l
                @click="openSensorMLDialog(item)"
              />
              <dot-menu-action-copy
                v-if="$auth.loggedIn"
                :path="copyLink(item.id)"
              />
              <dot-menu-action-archive
                v-if="canArchiveEntity(item)"
                @click="initArchiveDialog(item)"
              />
              <dot-menu-action-restore
                v-if="canRestoreEntity(item)"
                @click="runRestoreDevice(item)"
              />
              <dot-menu-action-delete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
                @click="initDeleteDialog(item)"
              />
            </template>
          </devices-list-item>
        </template>
      </base-list>
      <v-pagination
        v-model="page"
        :disabled="isLoading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <delete-dialog
      v-if="deviceToDelete"
      v-model="showDeleteDialog"
      title="Delete Device"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the device <em>{{ deviceToDelete.shortName }}</em>?
    </delete-dialog>
    <device-archive-dialog
      v-model="showArchiveDialog"
      :device-to-archive="deviceToArchive"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedDeviceSensorMLFilename"
      :url="selectedDeviceSensorMLUrl"
      @cancel="closeDownloadDialog"
    />
    <download-dialog
      v-model="showCsvDownloadDialog"
      filename="devices.csv"
      :url="exportCsvUrl"
      @cancel="showCsvDownloadDialog = false"
    />
  </div>
</template>
<script lang="ts">

import { Component, Vue } from 'nuxt-property-decorator'
import { Route } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadingSpinnerState, SetLoadingAction } from '@/store/progressindicator'
import {
  DevicesState,
  SetPageNumberAction,
  SetPageSizeAction,
  SearchDevicesPaginatedAction,
  PageSizesGetter,
  DeleteDeviceAction,
  ArchiveDeviceAction,
  RestoreDeviceAction,
  LoadDeviceAction,
  ReplaceDeviceInDevicesAction,
  ExportAsCsvAction,
  GetSensorMLUrlAction,
  ExportAsSensorMLAction
} from '@/store/devices'
import { ManufacturermodelsState } from '@/store/manufacturermodels'
import { SetBackToAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanArchiveEntityGetter, CanDeleteEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import { QueryParams } from '@/modelUtils/QueryParams'
import { DeviceSearchParamsSerializer } from '@/modelUtils/DeviceSearchParams'

import { Device } from '@/models/Device'
import { Visibility } from '@/models/Visibility'

import FoundEntries from '@/components/shared/FoundEntries.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'
import DeviceArchiveDialog from '@/components/devices/DeviceArchiveDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  computed: {
    ...mapGetters('devices', ['pageSizes']),
    ...mapState('devices', ['devices', 'device', 'pageNumber', 'pageSize', 'totalPages', 'totalCount']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('permissions', ['canAccessEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity']),
    ...mapState('manufacturermodels', ['manufacturerModel'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('appbar', ['setBackTo', 'setShowBackButton']),
    ...mapActions('devices', [
      'setPageNumber',
      'setPageSize',
      'searchDevicesPaginated',
      'exportAsCsv',
      'deleteDevice',
      'restoreDevice',
      'archiveDevice',
      'loadDevice',
      'replaceDeviceInDevices',
      'getSensorMLUrl',
      'exportAsSensorML'
    ])
  },
  components: {
    BaseList,
    DeleteDialog,
    DevicesListItem,
    DownloadDialog,
    DeviceArchiveDialog,
    DotMenuActionArchive,
    DotMenuActionCopy,
    DotMenuActionDelete,
    DotMenuActionRestore,
    DotMenuActionSensorML,
    ExtendedItemName,
    FoundEntries,
    PageSizeSelect
  }
})
export default class ManufacturerModelDevicesSearchPage extends Vue {
  private searchText: string | null = null

  private showDeleteDialog: boolean = false
  private deviceToDelete: Device | null = null

  private showArchiveDialog: boolean = false
  private deviceToArchive: Device | null = null

  private showDownloadDialog: boolean = false
  private deviceForSensorML: Device | null = null

  private showCsvDownloadDialog: boolean = false

  devices!: DevicesState['devices']
  device!: DevicesState['device']
  isLoading!: LoadingSpinnerState['isLoading']
  pageNumber!: DevicesState['pageNumber']
  pageSize!: DevicesState['pageSize']
  manufacturerModel!: ManufacturermodelsState['manufacturerModel']
  pageSizes!: PageSizesGetter
  canAccessEntity!: CanAccessEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setLoading!: SetLoadingAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchDevicesPaginated!: SearchDevicesPaginatedAction
  setBackTo!: SetBackToAction
  exportAsCsv!: ExportAsCsvAction
  deleteDevice!: DeleteDeviceAction
  archiveDevice!: ArchiveDeviceAction
  restoreDevice!: RestoreDeviceAction
  loadDevice!: LoadDeviceAction
  replaceDeviceInDevices!: ReplaceDeviceInDevicesAction
  getSensorMLUrl!: GetSensorMLUrlAction
  exportAsSensorML!: ExportAsSensorMLAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    this.setShowBackButton(false)

    try {
      this.setLoading(true)
      this.initSearchQueryParams(this.$route.query)
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.setLoading(false)
    }
  }

  initSearchQueryParams (queryParams: QueryParams): void {
    const searchParamsObject = (new DeviceSearchParamsSerializer({
      states: [],
      deviceTypes: [],
      manufacturer: [],
      permissionGroups: [],
      skipManufacturerName: true,
      skipModel: true
    })).toSearchParams(queryParams)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new DeviceSearchParamsSerializer({ skipManufacturerName: true, skipModel: true })).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  async runInitialSearch (): Promise<void> {
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) ?? 1
    }
    return 1
  }

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
  }

  runBasicSearch () {
    this.page = 1
    this.runSearch()
  }

  async runSearch () {
    try {
      this.setLoading(true)
      this.initUrlQueryParams()
      await this.searchDevicesPaginated(this.searchParams)
      await this.setPageAndSizeInUrl()
      this.setBackTo({ path: this.$route.path, query: this.$route.query })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.setLoading(false)
    }
  }

  clearBasicSearch () {
    this.searchText = null
  }

  setPageInUrl (preserveHash: boolean = true): void {
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

  setSizeInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.size) {
      // add size to the current url params
      query = {
        ...this.$route.query,
        size: String(this.size)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }

  setPageAndSizeInUrl (preserveHash: boolean = true): Promise<Route> {
    let query: QueryParams = {
      ...this.$route.query
    }
    if (this.size) {
      // add size to the current url params
      query = {
        ...query,
        size: String(this.size)
      }
    }
    if (this.page) {
      // add query to the current url params
      query = {
        ...query,
        page: String(this.page)
      }
    }
    return this.$router.replace({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
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
    try {
      this.setLoading(true)
      await this.deleteDevice(this.deviceToDelete.id)
      this.runSearch()
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }

  initArchiveDialog (device: Device) {
    this.showArchiveDialog = true
    this.deviceToArchive = device
  }

  closeArchiveDialog () {
    this.showArchiveDialog = false
    this.deviceToArchive = null
  }

  async archiveAndCloseDialog () {
    if (this.deviceToArchive === null || this.deviceToArchive.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.archiveDevice(this.deviceToArchive.id)
      await this.loadDevice({
        deviceId: this.deviceToArchive.id,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      await this.replaceDeviceInDevices(this.device!)
      this.$store.commit('snackbar/setSuccess', 'Device archived')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Device could not be archived')
    } finally {
      this.setLoading(false)
      this.closeArchiveDialog()
    }
  }

  async runRestoreDevice (device: Device) {
    if (device.id) {
      this.setLoading(true)
      try {
        await this.restoreDevice(device.id)
        await this.loadDevice({
          deviceId: device.id,
          includeCreatedBy: true,
          includeUpdatedBy: true
        })
        await this.replaceDeviceInDevices(this.device!)
        this.$store.commit('snackbar/setSuccess', 'Device restored')
      } catch (error) {
        this.$store.commit('snackbar/setError', 'Device could not be restored')
      } finally {
        this.setLoading(false)
      }
    }
  }

  openSensorMLDialog (device: Device) {
    this.deviceForSensorML = device
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.deviceForSensorML = null
    this.showDownloadDialog = false
  }

  get selectedDeviceSensorMLFilename (): string {
    if (this.deviceForSensorML != null) {
      return `${this.deviceForSensorML.shortName}.xml`
    }
    return 'device.xml'
  }

  async selectedDeviceSensorMLUrl (): Promise<string | null> {
    if (!this.deviceForSensorML) {
      return null
    }
    if (this.deviceForSensorML?.visibility === Visibility.Public) {
      return await this.getSensorMLUrl(this.deviceForSensorML.id!)
    } else {
      try {
        const blob = await this.exportAsSensorML(this.deviceForSensorML!.id!)
        return window.URL.createObjectURL(blob)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Device could not be exported as SensorML')
        return null
      }
    }
  }

  async exportCsvUrl (): Promise<string> {
    this.setLoading(true)
    const blob = await this.exportAsCsv(this.searchParams)
    this.setLoading(false)
    return window.URL.createObjectURL(blob)
  }

  copyLink (id: string): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/devices/copy/${id}${params}`
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
    this.setPageNumber(newVal)
    this.setPageInUrl(false)
  }

  get size (): number {
    return this.pageSize
  }

  set size (newVal: number) {
    const sizeChanged: boolean = this.size !== newVal

    this.setPageSize(newVal)
    this.setSizeInUrl(false)

    if (sizeChanged) {
      this.runSearch()
    }
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  get searchParams () {
    return {
      searchText: this.searchText,
      manufacturer: [],
      states: [],
      types: [],
      permissionGroups: [],
      onlyOwnDevices: false,
      includeArchivedDevices: false,
      manufacturerName: this.manufacturerModel!.manufacturerName,
      model: this.manufacturerModel!.model
    }
  }

  get newDeviceLink (): string {
    const params = '?' + (new URLSearchParams({ from: 'searchResult' })).toString()
    return `/devices/new${params}`
  }

  get manufacturerModelId () {
    return this.$route.params.manufacturerModelId
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
.v-select__selections input {
  display: none;
}
</style>

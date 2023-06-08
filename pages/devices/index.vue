<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
      :value="activeTab"
      @input="setActiveTab"
    >
      <v-tab-item :eager="true">
        <v-row
          dense
        >
          <v-col
            cols="12"
            md="5"
          >
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search devices"
              hint="Please enter at least 3 characters"
              @keydown.enter="basicSearch"
            />
          </v-col>
          <v-col
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
          <v-col
            align-self="center"
            class="text-right"
          >
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              to="/devices/new"
            >
              New Device
            </v-btn>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item :eager="true">
        <v-row
          dense
        >
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchText"
              label="Search term"
              placeholder="Search devices"
              hint="Please enter at least 3 characters"
              @keydown.enter="extendedSearch"
            />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <ManufacturerSelect v-model="selectedSearchManufacturers" label="Select a manufacturer" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <StatusSelect v-model="selectedSearchStates" label="Select a status" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <DeviceTypeSelect v-model="selectedSearchDeviceTypes" label="Select a device type" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col cols="12" md="12">
            <permission-group-search-select v-model="selectedSearchPermissionGroups" label="Select a permission group" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col v-if="$auth.loggedIn" cols="12" md="3">
            <v-checkbox v-model="onlyOwnDevices" label="Only own devices" />
          </v-col>
          <v-col cols="12" md="3">
            <v-checkbox v-model="includeArchivedDevices" label="Include archived devices" />
          </v-col>
        </v-row>
        <v-row
          dense
        >
          <v-col
            cols="5"
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
          <v-col
            align-self="center"
            class="text-right"
          >
            <v-btn
              v-if="$auth.loggedIn"
              color="accent"
              small
              nuxt
              to="/devices/new"
            >
              New Device
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
      <v-row
        no-gutters
        class="mt-10"
      >
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <FoundEntries v-model="totalCount" entity-name="device" />
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
        </v-col>

        <v-col
          cols="12"
          md="6"
        >
          <v-pagination
            v-model="page"
            :disabled="loading"
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

      <BaseList
        :list-items="devices"
      >
        <template #list-item="{item}">
          <DevicesListItem
            :key="item.id"
            :device="item"
          >
            <template
              #dot-menu-items
            >
              <DotMenuActionSensorML
                @click="openSensorML(item)"
              />
              <DotMenuActionCopy
                v-if="$auth.loggedIn"
                :path="'/devices/copy/' + item.id"
              />
              <DotMenuActionArchive
                v-if="canArchiveEntity(item)"
                @click="initArchiveDialog(item)"
              />
              <DotMenuActionRestore
                v-if="canRestoreEntity(item)"
                @click="runRestoreDevice(item)"
              />
              <DotMenuActionDelete
                v-if="$auth.loggedIn && canDeleteEntity(item)"
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
    <DeleteDialog
      v-if="deviceToDelete"
      v-model="showDeleteDialog"
      title="Delete Device"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the device <em>{{ deviceToDelete.shortName }}</em>?
    </DeleteDialog>
    <DeviceArchiveDialog
      v-model="showArchiveDialog"
      :device-to-archive="deviceToArchive"
      @cancel-archiving="closeArchiveDialog"
      @submit-archiving="archiveAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, IAppbarState, SetActiveTabAction } from '@/store/appbar'

import {
  VocabularyState,
  LoadEquipmentstatusAction,
  LoadDevicetypesAction,
  LoadManufacturersAction
} from '@/store/vocabulary'

import {
  DevicesState,
  SearchDevicesPaginatedAction,
  SetPageNumberAction,
  SetPageSizeAction,
  ExportAsCsvAction,
  DeleteDeviceAction,
  PageSizesGetter,
  ArchiveDeviceAction,
  RestoreDeviceAction,
  ExportAsSensorMLAction,
  LoadDeviceAction,
  ReplaceDeviceInDevicesAction,
  GetSensorMLUrlAction
} from '@/store/devices'

import {
  PermissionsState,
  CanAccessEntityGetter,
  CanDeleteEntityGetter,
  CanArchiveEntityGetter,
  LoadPermissionGroupsAction,
  CanRestoreEntityGetter
} from '@/store/permissions'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Status } from '@/models/Status'

import { QueryParams } from '@/modelUtils/QueryParams'
import { DeviceSearchParamsSerializer } from '@/modelUtils/DeviceSearchParams'

import DeviceTypeSelect from '@/components/DeviceTypeSelect.vue'
import ManufacturerSelect from '@/components/ManufacturerSelect.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import DeviceArchiveDialog from '@/components/devices/DeviceArchiveDialog.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionArchive from '@/components/DotMenuActionArchive.vue'
import DotMenuActionRestore from '@/components/DotMenuActionRestore.vue'
import DotMenuActionSensorML from '@/components/DotMenuActionSensorML.vue'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import PermissionGroupSearchSelect from '@/components/PermissionGroupSearchSelect.vue'
import { Visibility } from '@/models/Visibility'
import FoundEntries from '@/components/shared/FoundEntries.vue'

@Component({
  components: {
    FoundEntries,
    DevicesListItem,
    BaseList,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenuActionSensorML,
    DeleteDialog,
    DotMenuActionArchive,
    DotMenuActionRestore,
    DeviceArchiveDialog,
    DeviceTypeSelect,
    ManufacturerSelect,
    StatusSelect,
    PageSizeSelect,
    PermissionGroupSearchSelect
  },
  computed: {
    ...mapGetters('permissions', ['canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity', 'canAccessEntity', 'permissionGroups']),
    ...mapState('appbar', ['activeTab']),
    ...mapState('vocabulary', ['devicetypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('devices', ['devices', 'pageNumber', 'pageSize', 'totalPages', 'totalCount', 'device']),
    ...mapGetters('devices', ['pageSizes'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadEquipmentstatus', 'loadDevicetypes', 'loadManufacturers']),
    ...mapActions('devices', ['searchDevicesPaginated', 'setPageNumber', 'setPageSize', 'exportAsCsv', 'deleteDevice', 'archiveDevice', 'restoreDevice', 'exportAsSensorML', 'loadDevice', 'replaceDeviceInDevices', 'getSensorMLUrl']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setActiveTab']),
    ...mapActions('permissions', ['loadPermissionGroups'])
  }
})
export default class SearchDevicesPage extends Vue {
  private loading: boolean = false
  private processing: boolean = false

  private selectedSearchManufacturers: Manufacturer[] = []
  private selectedSearchStates: Status[] = []
  private selectedSearchDeviceTypes: DeviceType[] = []
  private selectedSearchPermissionGroups: PermissionGroup[] = []
  private onlyOwnDevices: boolean = false
  private includeArchivedDevices: boolean = false
  private searchText: string | null = null

  private showDeleteDialog: boolean = false
  private deviceToDelete: Device | null = null

  private showArchiveDialog: boolean = false
  private deviceToArchive: Device | null = null

  // vuex definition for typescript check
  devices!: DevicesState['devices']
  pageSize!: DevicesState['pageSize']
  totalPages!: DevicesState['totalPages']
  pageNumber!: DevicesState['pageNumber']
  pageSizes!: PageSizesGetter
  totalCount!: DevicesState['totalCount']
  permissionGroups!: PermissionsState['permissionGroups']
  loadEquipmentstatus!: LoadEquipmentstatusAction
  loadDevicetypes!: LoadDevicetypesAction
  loadManufacturers!: LoadManufacturersAction
  loadPermissionGroups!: LoadPermissionGroupsAction
  setPageNumber!: SetPageNumberAction
  setPageSize!: SetPageSizeAction
  searchDevicesPaginated!: SearchDevicesPaginatedAction
  exportAsCsv!: ExportAsCsvAction
  deleteDevice!: DeleteDeviceAction
  archiveDevice!: ArchiveDeviceAction
  restoreDevice!: RestoreDeviceAction
  devicetypes!: VocabularyState['devicetypes']
  manufacturers!: VocabularyState['manufacturers']
  equipmentstatus!: VocabularyState['equipmentstatus']
  canAccessEntity!: CanAccessEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  activeTab!: IAppbarState['activeTab']
  setActiveTab!: SetActiveTabAction
  exportAsSensorML!: ExportAsSensorMLAction
  loadDevice!: LoadDeviceAction
  replaceDeviceInDevices!: ReplaceDeviceInDevicesAction
  device!: DevicesState['device']
  getSensorMLUrl!: GetSensorMLUrlAction

  async created () {
    this.initializeAppBar()
    try {
      this.loading = true
      await Promise.all([
        this.loadEquipmentstatus(),
        this.loadDevicetypes(),
        this.loadManufacturers(),
        this.loadPermissionGroups()
      ])
      this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.loading = false
    }
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
      manufacturer: this.selectedSearchManufacturers,
      states: this.selectedSearchStates,
      types: this.selectedSearchDeviceTypes,
      permissionGroups: this.selectedSearchPermissionGroups,
      onlyOwnDevices: this.onlyOwnDevices && this.$auth.loggedIn,
      includeArchivedDevices: this.includeArchivedDevices
    }
  }

  isExtendedSearch (): boolean {
    return this.onlyOwnDevices === true ||
      !!this.selectedSearchStates.length ||
      !!this.selectedSearchDeviceTypes.length ||
      !!this.selectedSearchManufacturers.length ||
      !!this.selectedSearchPermissionGroups.length ||
      this.includeArchivedDevices === true
  }

  async runInitialSearch (): Promise<void> {
    this.setActiveTab(this.isExtendedSearch() ? 1 : 0)

    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  basicSearch () {
    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
    this.selectedSearchPermissionGroups = []
    this.onlyOwnDevices = false
    this.includeArchivedDevices = false
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearBasicSearch () {
    this.searchText = null
    this.initUrlQueryParams()
  }

  extendedSearch () {
    this.page = 1// Important to set page to one otherwise it's possible that you don't anything
    this.runSearch()
  }

  clearExtendedSearch () {
    this.clearBasicSearch()

    this.selectedSearchManufacturers = []
    this.selectedSearchStates = []
    this.selectedSearchDeviceTypes = []
    this.selectedSearchPermissionGroups = []
    this.onlyOwnDevices = false
    this.includeArchivedDevices = false
    this.initUrlQueryParams()
  }

  async runSearch (): Promise<void> {
    try {
      this.loading = true
      this.initUrlQueryParams()
      await this.searchDevicesPaginated(this.searchParams)
      this.setPageInUrl()
      this.setSizeInUrl()
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.loading = false
    }
  }

  async exportCsv () {
    if (this.devices.length > 0) {
      try {
        this.processing = true
        const blob = await this.exportAsCsv(this.searchParams)
        saveAs(blob, 'devices.csv')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'CSV export failed')
      } finally {
        this.processing = false
      }
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
    try {
      this.loading = true
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
      this.loading = true
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
      this.loading = false
      this.closeArchiveDialog()
    }
  }

  async runRestoreDevice (device: Device) {
    if (device.id) {
      this.loading = true
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
        this.loading = false
      }
    }
  }

  initSearchQueryParams (): void {
    const searchParamsObject = (new DeviceSearchParamsSerializer({
      states: this.equipmentstatus,
      deviceTypes: this.devicetypes,
      manufacturer: this.manufacturers,
      permissionGroups: this.permissionGroups
    })).toSearchParams(this.$route.query)

    // prefill the form by the serialized search params from the URL
    if (searchParamsObject.searchText) {
      this.searchText = searchParamsObject.searchText
    }
    if (searchParamsObject.onlyOwnDevices) {
      this.onlyOwnDevices = searchParamsObject.onlyOwnDevices
    }
    if (searchParamsObject.includeArchivedDevices) {
      this.includeArchivedDevices = searchParamsObject.includeArchivedDevices
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
    if (searchParamsObject.permissionGroups) {
      this.selectedSearchPermissionGroups = searchParamsObject.permissionGroups
    }
  }

  initUrlQueryParams (): void {
    this.$router.push({
      query: (new DeviceSearchParamsSerializer()).toQueryParams(this.searchParams),
      hash: this.$route.hash
    })
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) ?? 1
    }
    return 1
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

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
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

  initializeAppBar () {
    this.setTabs([
      'Search',
      'Extended Search'
    ])
    this.setTitle('Devices')
  }

  downloadSensorML (url: string, shortName: string) {
    const link = document.createElement('a')
    link.href = url
    link.download = `${shortName}.xml`
    link.click()
  }

  async openSensorML (device: Device) {
    if (device.visibility === Visibility.Public) {
      const url = await this.getSensorMLUrl(device.id!)
      window.open(url)
      this.downloadSensorML(url, device.shortName)
    } else {
      try {
        const blob = await this.exportAsSensorML(device.id!)
        const url = window.URL.createObjectURL(blob)
        window.open(url)
        this.downloadSensorML(url, device.shortName)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Device could not be exported as SensorML')
      }
    }
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

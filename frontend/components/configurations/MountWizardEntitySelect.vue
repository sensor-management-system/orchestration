<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <v-row>
      <v-col cols="6">
        <v-card>
          <v-container>
            <v-tabs
              v-model="tab"
              slider-color="primary"
            >
              <v-tab>Devices</v-tab>
              <v-tab>Platforms</v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item>
                <v-card>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="searchTextDevices"
                          label="Name"
                          placeholder="Search devices"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchDevicesForMount"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        md="5"
                        align-self="center"
                      >
                        <v-btn
                          color="primary"
                          small
                          @click="searchDevicesForMount"
                        >
                          Search
                        </v-btn>
                        <v-btn
                          text
                          small
                          @click="clearBasicSearchDevices"
                        >
                          Clear
                        </v-btn>
                      </v-col>
                      <v-col cols="12" md="7">
                        <v-subheader>
                          <page-size-select
                            v-model="deviceSearchSearchPageSize"
                            :items="devicePageSizeItems"
                            label="Items per page"
                          />
                        </v-subheader>
                      </v-col>
                    </v-row>
                    <div v-if="devicesTotalCount > 0 && deviceAvailabilities.length>0">
                      <v-subheader>
                        <template v-if="devicesTotalCount == 1">
                          1 device found
                        </template>
                        <template v-else>
                          {{ devicesTotalCount }} devices found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <v-pagination
                        v-if="devicesSearchPage != 1 || devicesTotalPages > 1"
                        v-model="devicesSearchPage"
                        :disabled="isLoading"
                        :length="devicesTotalPages"
                        :total-visible="7"
                      />
                      <base-mount-list
                        :value="syncedSelectedDevices"
                        :items="devices"
                        :availabilities="deviceAvailabilities"
                        keep-values-that-are-not-in-items
                        @selectEntity="setDeviceSelection($event)"
                      />
                      <v-pagination
                        v-if="devicesSearchPage != 1 || devicesTotalPages > 1"
                        v-model="devicesSearchPage"
                        :disabled="isLoading"
                        :length="devicesTotalPages"
                        :total-visible="7"
                      />
                    </div>
                    <div v-else-if="devicesTotalCount <=0 && hasSearchedDevice">
                      <v-subheader>
                        There are no devices that match your search criteria.
                      </v-subheader>
                    </div>
                  </v-container>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="searchTextPlatforms"
                          label="Name"
                          placeholder="Search platforms"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchPlatformsForMount"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        md="5"
                        align-self="center"
                      >
                        <v-btn
                          color="primary"
                          small
                          @click="searchPlatformsForMount"
                        >
                          Search
                        </v-btn>
                        <v-btn
                          text
                          small
                          @click="clearBasicSearchPlatforms"
                        >
                          Clear
                        </v-btn>
                      </v-col>
                      <v-col cols="12" md="7">
                        <v-subheader>
                          <page-size-select
                            v-model="platformSearchSearchPageSize"
                            :items="platformPageSizeItems"
                            label="Items per page"
                          />
                        </v-subheader>
                      </v-col>
                    </v-row>
                    <div v-if="platformsTotalCount > 0 && platformAvailabilities.length>0">
                      <v-subheader>
                        <template v-if="platformsTotalCount == 1">
                          1 platform found
                        </template>
                        <template v-else>
                          {{ platformsTotalCount }} platforms found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <v-pagination
                        v-if="platformsSearchPage != 1 || platformsTotalPages > 1"
                        v-model="platformsSearchPage"
                        :disabled="isLoading"
                        :length="platformsTotalPages"
                        :total-visible="7"
                      />
                      <base-mount-list
                        :value="syncedSelectedPlatforms"
                        :items="platforms"
                        :availabilities="platformAvailabilities"
                        keep-values-that-are-not-in-items
                        @selectEntity="setPlatformSelection($event)"
                      />
                      <v-pagination
                        v-if="platformsSearchPage != 1 || platformsTotalPages > 1"
                        v-model="platformsSearchPage"
                        :disabled="isLoading"
                        :length="platformsTotalPages"
                        :total-visible="7"
                      />
                    </div>
                    <div v-else-if="platformsTotalCount <=0 && hasSearchedPlatform">
                      <v-subheader>
                        There are no platforms that match your search criteria.
                      </v-subheader>
                    </div>
                  </v-container>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-container>
        </v-card>
      </v-col>
      <v-col cols="6">
        <v-slide-x-reverse-transition>
          <v-container v-if="selectedEntities.length > 0">
            <v-card-title class="grey--text text--darken-2">
              Current Selection
            </v-card-title>
            <BaseList
              :list-items="selectedEntities"
            >
              <template #list-item="{item}">
                <platforms-list-item v-if="item.type === 'platform'" :platform="item" :hide-header="true" target="_blank" />
                <devices-list-item v-if="item.type === 'device'" :device="item" :hide-header="true" target="_blank" />
              </template>
            </BaseList>
          </v-container>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, PropSync, InjectReactive, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { DevicesState, LoadDeviceAvailabilitiesAction, SearchDevicesPaginatedAction } from '@/store/devices'
import { PlatformsState, SearchPlatformsPaginatedAction, LoadPlatformAvailabilitiesAction } from '@/store/platforms'

import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import BaseList from '@/components/shared/BaseList.vue'
import BaseMountList from '@/components/shared/BaseMountList.vue'

import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

@Component({
  components: {
    PlatformsListItem,
    DevicesListItem,
    BaseList,
    BaseMountList,
    PageSizeSelect

  },
  computed: {
    ...mapState('devices', {
      devices: 'devices',
      deviceAvailabilities: 'deviceAvailabilities',
      devicesTotalCount: 'totalCount',
      devicesTotalPages: 'totalPages'
    }),
    ...mapState('platforms', {
      platforms: 'platforms',
      platformAvailabilities: 'platformAvailabilities',
      platformsTotalCount: 'totalCount',
      platformsTotalPages: 'totalPages'
    }),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('devices', {
      devicePageSizeItems: 'pageSizes'
    }),
    ...mapGetters('platforms', {
      platformPageSizeItems: 'pageSizes'
    })
  },
  methods: {
    ...mapActions('devices', ['searchDevicesPaginated', 'loadDeviceAvailabilities']),
    ...mapActions('platforms', ['searchPlatformsPaginated', 'loadPlatformAvailabilities']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class MountWizardEntitySelect extends Vue {
  @PropSync('selectedDevices', {
    required: false,
    type: Array
  })
    syncedSelectedDevices!: Device[]

  @PropSync('selectedPlatforms', {
    required: false,
    type: Array
  })
    syncedSelectedPlatforms!: Platform[]

  @PropSync('devicesToMount', {
    required: false,
    type: Array
  })
    syncedDevicesToMount!: { entity: Device, mountInfo: DeviceMountAction }[]

  @PropSync('platformsToMount', {
    required: false,
    type: Array
  })
    syncedPlatformsToMount!: { entity: Platform, mountInfo: PlatformMountAction }[]

  @InjectReactive() selectedDate!: DateTime
  @InjectReactive() selectedEndDate!: DateTime | null

  private resetDeviceSearchToFirstPage = false
  private resetPlatformSearchToFirstPage = false

  // vuex definition for typescript check
  devices!: DevicesState['devices']
  platforms!: PlatformsState['platforms']
  devicesTotalPages!: DevicesState['totalPages']
  platformsTotalPages!: PlatformsState['totalPages']
  searchDevicesPaginated!: SearchDevicesPaginatedAction
  loadDeviceAvailabilities!: LoadDeviceAvailabilitiesAction
  searchPlatformsPaginated!: SearchPlatformsPaginatedAction
  loadPlatformAvailabilities!: LoadPlatformAvailabilitiesAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  private tab = null

  private searchTextPlatforms: string = ''
  private searchTextDevices: string = ''

  private hasSearchedDevice = false
  private hasSearchedPlatform = false

  mounted () {
    // Start with some clean state for devices & platforms search
    this.$store.commit('devices/setDevices', [])
    this.$store.commit('devices/setTotalCount', 0)
    this.$store.commit('devices/setPageNumber', 1)
    this.$store.commit('platforms/setPlatforms', [])
    this.$store.commit('platforms/setTotalCount', 0)
    this.$store.commit('platforms/setPageNumber', 1)
  }

  clearBasicSearchPlatforms () {
    this.searchTextPlatforms = ''
    this.hasSearchedPlatform = false
  }

  clearBasicSearchDevices () {
    this.searchTextDevices = ''
    this.hasSearchedDevice = false
  }

  async searchDevicesForMount () {
    if (this.resetDeviceSearchToFirstPage) {
      this.$store.commit('devices/setPageNumber', 1)
      this.resetDeviceSearchToFirstPage = false
    }
    try {
      this.setLoading(true)
      await this.searchDevicesPaginated({
        searchText: this.searchTextDevices,
        manufacturer: [],
        states: [],
        types: [],
        permissionGroups: [],
        onlyOwnDevices: false,
        includeArchivedDevices: false
      })
      await this.checkAvailabilities('device')
      if (this.devicesSearchPage > this.devicesTotalPages) {
        // triggers also a new search
        // but prevent to set it to zero (this would trigger an error on backend)
        this.devicesSearchPage = Math.max(this.devicesTotalPages, 1)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.setLoading(false)
      this.hasSearchedDevice = true
    }
  }

  async searchPlatformsForMount () {
    if (this.resetPlatformSearchToFirstPage) {
      this.$store.commit('platforms/setPageNumber', 1)
      this.resetPlatformSearchToFirstPage = false
    }
    try {
      this.setLoading(true)

      // Not bound as methods, as there can be name conflicts with the devices.
      this.$store.dispatch('platforms/setSearchText', this.searchTextPlatforms)
      this.$store.dispatch('platforms/setSelectedSearchManufacturers', [])
      this.$store.dispatch('platforms/setSelectedSearchStates', [])
      this.$store.dispatch('platforms/setSelectedSearchPlatformTypes', [])
      this.$store.dispatch('platforms/setSelectedSearchPermissionGroups', [])
      this.$store.dispatch('platforms/setOnlyOwnPlatforms', false)
      this.$store.dispatch('platforms/setIncludeArchivedPlatforms', false)

      await this.searchPlatformsPaginated()
      await this.checkAvailabilities('platform')
      if (this.platformsSearchPage > this.platformsTotalPages) {
        // triggers also a new search
        // but prevent to set it to zero (this would trigger an error on backend)
        this.platformsSearchPage = Math.max(this.platformsTotalPages, 1)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.setLoading(false)
      this.hasSearchedPlatform = true
    }
  }

  async checkAvailabilities (type: string) {
    try {
      if (type === 'device') {
        const ids = this.devices.map(entity => entity.id)
        await this.loadDeviceAvailabilities({ ids, from: this.selectedDate, until: this.selectedEndDate })
      } else if (type === 'platform') {
        const ids = this.platforms.map(entity => entity.id)
        await this.loadPlatformAvailabilities({ ids, from: this.selectedDate, until: this.selectedEndDate })
      }
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of availabilities failed')
    }
  }

  setPlatformSelection (selection: Platform[]) {
    this.syncedSelectedPlatforms = selection
    this.syncedPlatformsToMount = this.removeSelectionFromMounts(this.syncedPlatformsToMount, this.syncedSelectedPlatforms) as { entity: Platform, mountInfo: PlatformMountAction }[]
  }

  setDeviceSelection (selection: Device[]) {
    this.syncedSelectedDevices = selection
    this.syncedDevicesToMount = this.removeSelectionFromMounts(this.syncedDevicesToMount, this.syncedSelectedDevices) as { entity: Device, mountInfo: DeviceMountAction}[]
  }

  removeSelectionFromMounts (entitiesToMount: { entity: Platform | Device, mountInfo: PlatformMountAction | DeviceMountAction }[], selectedEntities: Platform[] | Device[]): { entity: Platform | Device, mountInfo: PlatformMountAction | DeviceMountAction }[] {
    return entitiesToMount.filter((object1) => {
      return selectedEntities.some((object2: Platform | Device) => {
        return object1.entity.id === object2.id
      })
    })
  }

  get selectedEntities () {
    return [...this.syncedSelectedPlatforms, ...this.syncedSelectedDevices]
  }

  get deviceSearchSearchPageSize (): number {
    return this.$store.state.devices.pageSize
  }

  set deviceSearchSearchPageSize (newVal: number) {
    const oldVal = this.deviceSearchSearchPageSize
    if (oldVal !== newVal) {
      this.$store.dispatch('devices/setPageSize', newVal)
      this.searchDevicesForMount()
    }
  }

  get devicesSearchPage (): number {
    return this.$store.state.devices.pageNumber
  }

  set devicesSearchPage (newVal: number) {
    const oldVal = this.devicesSearchPage
    if (oldVal !== newVal) {
      this.$store.dispatch('devices/setPageNumber', newVal)
      this.searchDevicesForMount()
    }
  }

  get platformSearchSearchPageSize (): number {
    return this.$store.state.platforms.pageSize
  }

  set platformSearchSearchPageSize (newVal: number) {
    const oldVal = this.platformSearchSearchPageSize
    if (oldVal !== newVal) {
      this.$store.dispatch('platforms/setPageSize', newVal)
      this.searchPlatformsForMount()
    }
  }

  get platformsSearchPage (): number {
    return this.$store.state.platforms.pageNumber
  }

  set platformsSearchPage (newVal: number) {
    const oldVal = this.platformsSearchPage
    if (oldVal !== newVal) {
      this.$store.dispatch('platforms/setPageNumber', newVal)
      this.searchPlatformsForMount()
    }
  }

  @Watch('searchTextDevices')
  onSearchTextDevicesChanged () {
    this.resetDeviceSearchToFirstPage = true
  }

  @Watch('searchTextPlatforms')
  onSearchTextPlatformsChanged () {
    this.resetPlatformSearchToFirstPage = true
  }
}
</script>

<style scoped>

</style>

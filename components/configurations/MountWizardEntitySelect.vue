<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
                          placeholder="Name of device"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchDevicesForMount"
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
                      <ProgressIndicator
                        v-model="isLoading"
                      />
                    </v-row>
                    <div v-if="devices.length>0 && deviceAvailabilities.length>0">
                      <v-subheader>
                        <template v-if="devices.length == 1">
                          1 device found
                        </template>
                        <template v-else>
                          {{ devices.length }} devices found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <base-mount-list
                        v-model="syncedSelectedDevices"
                        :items="devices"
                        :availabilities="deviceAvailabilities"
                        @selectEntity="setDeviceSelection($event)"
                      />
                    </div>
                    <div v-else-if="devices.length <=0 && hasSearchedDevice">
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
                          placeholder="Name of platform"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchPlatformsForMount"
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
                    </v-row>
                    <div v-if="platforms.length>0 && platformAvailabilities.length>0">
                      <v-subheader>
                        <template v-if="platforms.length == 1">
                          1 platform found
                        </template>
                        <template v-else>
                          {{ platforms.length }} platforms found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <base-mount-list
                        v-model="syncedSelectedPlatforms"
                        :items="platforms"
                        :availabilities="platformAvailabilities"
                        @selectEntity="setPlatformSelection($event)"
                      />
                    </div>
                    <div v-else-if="platforms.length <=0 && hasSearchedPlatform">
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
                <platforms-list-item v-if="item.type === 'platform'" :platform="item" :hide-header="true" />
                <devices-list-item v-if="item.type === 'device'" :device="item" :hide-header="true" />
              </template>
            </BaseList>
          </v-container>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, PropSync, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { DevicesState, SearchDevicesAction, LoadDeviceAvailabilitiesAction } from '@/store/devices'
import { PlatformsState, SearchPlatformsAction, LoadPlatformAvailabilitiesAction } from '@/store/platforms'

import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import BaseList from '@/components/shared/BaseList.vue'
import BaseMountList from '@/components/shared/BaseMountList.vue'

import PlatformsListItem from '@/components/platforms/PlatformsListItem.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator,
    PlatformsListItem,
    DevicesListItem,
    BaseList,
    BaseMountList
  },
  computed: {
    ...mapState('devices', ['devices', 'deviceAvailabilities']),
    ...mapState('platforms', ['platforms', 'platformAvailabilities'])
  },
  methods: {
    ...mapActions('devices', ['searchDevices', 'loadDeviceAvailabilities']),
    ...mapActions('platforms', ['searchPlatforms', 'loadPlatformAvailabilities'])
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

  // vuex definition for typescript check
  devices!: DevicesState['devices']
  platforms!: PlatformsState['platforms']
  searchDevices!: SearchDevicesAction
  loadDeviceAvailabilities!: LoadDeviceAvailabilitiesAction
  searchPlatforms!: SearchPlatformsAction
  loadPlatformAvailabilities!: LoadPlatformAvailabilitiesAction

  private tab = null
  private isLoading = false

  private searchTextPlatforms: string = ''
  private searchTextDevices: string = ''

  private hasSearchedDevice = false
  private hasSearchedPlatform = false

  clearBasicSearchPlatforms () {
    this.searchTextPlatforms = ''
    this.hasSearchedPlatform = false
  }

  clearBasicSearchDevices () {
    this.searchTextPlatforms = ''
    this.hasSearchedDevice = false
  }

  async searchDevicesForMount () {
    try {
      this.isLoading = true
      await this.searchDevices(this.searchTextDevices)
      await this.checkAvailabilities('device')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.isLoading = false
      this.hasSearchedDevice = true
    }
  }

  async searchPlatformsForMount () {
    try {
      this.isLoading = true
      await this.searchPlatforms(this.searchTextPlatforms)
      await this.checkAvailabilities('platform')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
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
}
</script>

<style scoped>

</style>

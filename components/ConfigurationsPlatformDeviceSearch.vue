<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
    Add platforms and devices:
    <v-row v-if="searchOptions">
      <v-col cols="12" md="3">
        <v-select
          v-model="searchOptions.searchType"
          label="Type"
          :items="searchTypes"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchOptions.text"
          label="Name"
          @keydown.enter="search"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-btn
          color="primary"
          @click="search"
        >
          search
        </v-btn>
      </v-col>
    </v-row>
    <div v-if="loading">
      <div class="text-center pt-2">
        <v-progress-circular indeterminate />
      </div>
    </div>
    <div v-else>
      <v-row v-if="searchedForPlatforms && platforms.length">
        <v-col cols="12">
          <v-expansion-panels
            v-model="selectedPlatform"
          >
            <v-expansion-panel
              v-for="item in platforms"
              :key="'platform-' + item.id"
            >
              <v-expansion-panel-header>
                {{ item.shortName }} {{ isPlatformUsedFunc(item) ? ' - already mounted': '' }}
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-expansion-panels multiple>
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      Platform overview
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col>
                          <label>Long name</label>
                        </v-col>
                        <v-col>
                          {{ item.longName }}
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col>
                          <label>URN</label>
                        </v-col>
                        <v-col>
                          (TODO)
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col>
                          <v-btn :href="'platforms/' + item.id" target="_blank" :disabled="false">
                            <v-icon>
                              mdi-open-in-new
                            </v-icon>
                            Open in new tab
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel :disabled="isPlatformUsedFunc(item)">
                    <v-expansion-panel-header class="mount-expansion-panel">
                      Mount
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <ConfigurationsPlatformDeviceMountForm
                        ref="mountForm"
                        data-role-btn="add-platform"
                        :readonly="isPlatformUsedFunc(item)"
                        :contacts="contacts"
                        :current-user-mail="currentUserMail"
                        @add="addPlatform(item, $event)"
                      />
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
      <v-row v-else-if="searchedForPlatforms && !platforms.length">
        <p class="text-center">
          There are no platforms that match your search criteria.
        </p>
      </v-row>
      <v-row v-if="searchedForDevices && devices.length">
        <v-col cols="12">
          <v-expansion-panels
            v-model="selectedDevice"
          >
            <v-expansion-panel
              v-for="item in devices"
              :key="'device-' + item.id"
            >
              <v-expansion-panel-header>
                {{ item.shortName }} {{ isDeviceUsedFunc(item) ? ' - already mounted': '' }}
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-expansion-panels multiple>
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      Device overview
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col>
                          <label>Long name</label>
                        </v-col>
                        <v-col>
                          {{ item.longName }}
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col>
                          <label>URN</label>
                        </v-col>
                        <v-col>
                          (TODO)
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col>
                          <v-btn :href="'devices/' + item.id" target="_blank" :disabled="false">
                            <v-icon>
                              mdi-open-in-new
                            </v-icon>
                            Open in new tab
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel :disabled="isDeviceUsedFunc(item)">
                    <v-expansion-panel-header class="mount-expansion-panel">
                      Mount
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <ConfigurationsPlatformDeviceMountForm
                        data-role-btn="add-device"
                        :readonly="isDeviceUsedFunc(item)"
                        :contacts="contacts"
                        :current-user-mail="currentUserMail"
                        @add="addDevice(item, $event)"
                      />
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
      <v-row v-else-if="searchedForDevices && !devices.length">
        <p class="text-center">
          There are no devices that match your search criteria.
        </p>
      </v-row>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select platforms and devices for a configuration
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import ConfigurationsPlatformDeviceMountForm from '@/components/ConfigurationsPlatformDeviceMountForm.vue'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'

import { IMountData } from '@/viewmodels/IMountData'

enum SearchType {
  Platform = 'Platform',
  Device = 'Device'
}

interface ISearchOptions {
  searchType: SearchType
  text: string
}

type IsPlatformUsedFunc = (p: Platform) => boolean
type IsDeviceUsedFunc = (d: Device) => boolean

/**
 * A class component to search for platforms and devices
 * @extends Vue
 */
@Component({
  components: {
    ConfigurationsPlatformDeviceMountForm
  }
})
// @ts-ignore
export default class ConfigurationsPlatformDeviceSearch extends Vue {
  private searchOptions: ISearchOptions = {
    searchType: SearchType.Platform,
    text: ''
  }

  private platformsResult: Platform[] = [] as Platform[]
  private devicesResult: Device[] = [] as Device[]

  private selectedPlatform = -1
  private selectedDevice = -1

  private loading = false
  private searchedForPlatforms = false
  private searchedForDevices = false

  /**
   * a function that returns if a device is already present in a tree or not
   */
  @Prop({
    default: () => false,
    type: Function
  })
  // @ts-ignore
  readonly isDeviceUsedFunc: IsDeviceUsedFunc

  /**
   * a function that returns if a platform is already present in a tree or not
   */
  @Prop({
    default: () => false,
    type: Function
  })
  // @ts-ignore
  readonly isPlatformUsedFunc: IsPlatformUsedFunc

  @Prop({
    default: DateTime.utc(),
    type: DateTime
  })
  readonly selectedDate!: DateTime

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    type: String
  })
  // @ts-ignore
readonly currentUserMail: string|null

  get searchTypes (): string[] {
    return [SearchType.Platform, SearchType.Device]
  }

  /**
   * returns a list of platforms
   *
   * @return {Platform[]} an Array of platforms
   */
  get platforms (): Platform[] {
    return this.platformsResult
  }

  /**
   * sets the list of platforms
   *
   * when the list is not empty, the list of devices gets cleared
   *
   * @param {Platform[]} platforms - an Array of platforms to set
   */
  set platforms (platforms: Platform[]) {
    this.platformsResult = platforms
    if (platforms.length) {
      this.devicesResult = [] as Device[]
    }
  }

  /**
   * returns a list of devices
   *
   * @return {Device[]} an Array of devices
   */
  get devices (): Device[] {
    return this.devicesResult
  }

  /**
   * sets the list of devices
   *
   * when the list is not empty, the list of platforms gets cleared
   *
   * @param {Device[]} devices - an Array of devices to set
   */
  set devices (devices: Device[]) {
    this.devicesResult = devices
    if (devices.length) {
      this.platformsResult = [] as Platform[]
    }
  }

  /**
   * searches for platforms or devices depending on the searchType
   *
   * @async
   */
  async search () {
    this.loading = true
    this.searchedForPlatforms = false
    this.searchedForDevices = false
    switch (this.searchOptions.searchType) {
      case SearchType.Platform:
        this.platforms = await this.$api.platforms.newSearchBuilder()
          .withText(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        this.searchedForPlatforms = true
        break
      case SearchType.Device:
        this.devices = await this.$api.devices.newSearchBuilder()
          .withText(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        this.searchedForDevices = true
        break
      default:
        throw new TypeError('search function not defined for unknown value')
    }
    this.loading = false
  }

  /**
   * triggers an add-platform event
   *
   * @param {Platform} platform - the platform to add
   * @fires ConfigurationsPlatformDeviceSearch#add-platform
   */
  addPlatform (platform: Platform, mountData: IMountData) {
    /**
     * fires an add-plaform event
     * @event ConfigurationsPlatformDeviceSearch#add-platform
     * @type {Platform}
     */
    this.$emit(
      'add-platform',
      platform,
      mountData.offsetX,
      mountData.offsetY,
      mountData.offsetZ,
      mountData.contact,
      mountData.description
    )
  }

  /**
   * triggers an add-device event
   *
   * @param {Device} device - the device to add
   * @fires ConfigurationsPlatformDeviceSearch#add-device
   */
  addDevice (device: Device, mountData: IMountData) {
    /**
     * fires an add-device event
     * @event ConfigurationsPlatformDeviceSearch#add-device
     * @type {Device}
     */
    this.$emit(
      'add-device',
      device,
      mountData.offsetX,
      mountData.offsetY,
      mountData.offsetZ,
      mountData.contact,
      mountData.description
    )
  }
}
</script>

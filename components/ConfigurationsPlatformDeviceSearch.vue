<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
    <v-row>
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
    <v-row v-if="platforms.length">
      <v-col cols="12">
        <v-list
          two-line
          max-height="50vh"
          class="overflow-y-auto"
        >
          <v-list-item-group
            v-model="platformItem"
            color="primary"
          >
            <template
              v-for="(item, index) in platforms"
            >
              <v-list-item
                :key="'platform-' + item.id"
                :disabled="isPlatformUsedFunc(item)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item.shortName" />
                  <v-list-item-subtitle class="text--primary" v-text="item.longName" />
                  <v-list-item-subtitle>URN (TODO)</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn
                    :key="'btn-add-platform-' + item.id"
                    :disabled="isPlatformUsedFunc(item)"
                    data-role="add-platform"
                    @click="addPlatform(item)"
                  >
                    add
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
              <v-divider
                v-if="index + 1 < platforms.length"
                :key="'platformDivider-' + index"
              />
            </template>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
    <v-row v-if="devices.length">
      <v-col cols="12">
        <v-list
          two-line
          max-height="50vh"
          class="overflow-y-auto"
        >
          <v-list-item-group
            v-model="deviceItem"
            color="primary"
          >
            <template
              v-for="(item, index) in devices"
            >
              <v-list-item
                :key="'device-' + item.id"
                :disabled="isDeviceUsedFunc(item)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item.shortName" />
                  <v-list-item-subtitle class="text--primary" v-text="item.longName" />
                  <v-list-item-subtitle>URN (TODO)</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <div v-if="!canAddDevices">
                    Devices can only be added to platforms.
                  </div>
                  <v-btn
                    :key="'btn-add-device-' + item.id"
                    :disabled="isDeviceUsedFunc(item) || (!canAddDevices)"
                    data-role="add-device"
                    @click="addDevice(item)"
                  >
                    add
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
              <v-divider
                v-show="index + 1 < devices.length"
                :key="'deviceDivider-' + index"
              />
            </template>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select platforms and devices for a configuration
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'

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
@Component
// @ts-ignore
export default class ConfigurationsPlatformDeviceSearch extends Vue {
  private searchOptions: ISearchOptions = {
    searchType: SearchType.Platform,
    text: ''
  }

  private platformsResult: Platform[] = [] as Platform[]
  private devicesResult: Device[] = [] as Device[]

  private platformItem: string = ''
  private deviceItem: string = ''

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
    default: () => false,
    type: Boolean
  })
  readonly canAddDevices!: boolean

  get searchTypes (): string[] {
    const result = [SearchType.Platform]
    // maybe it makes more sense to allow the search
    // but show that devices need a platform to be added to
    if (this.canAddDevices) {
      result.push(SearchType.Device)
    }
    return result
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
    switch (this.searchOptions.searchType) {
      case SearchType.Platform:
        this.platforms = await this.$api.platforms.newSearchBuilder()
          .withText(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        break
      case SearchType.Device:
        this.devices = await this.$api.devices.newSearchBuilder()
          .withText(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        break
      default:
        throw new TypeError('search function not defined for unknown value')
    }
  }

  /**
   * triggers an add-platform event
   *
   * @param {Platform} platform - the platform to add
   * @fires ConfigurationsPlatformDeviceSearch#add-platform
   */
  addPlatform (platform: Platform) {
    /**
     * fires an add-plaform event
     * @event ConfigurationsPlatformDeviceSearch#add-platform
     * @type {Platform}
     */
    this.$emit('add-platform', platform)
  }

  /**
   * triggers an add-device event
   *
   * @param {Device} device - the device to add
   * @fires ConfigurationsPlatformDeviceSearch#add-device
   */
  addDevice (device: Device) {
    /**
     * fires an add-device event
     * @event ConfigurationsPlatformDeviceSearch#add-device
     * @type {Device}
     */
    if (this.canAddDevices) {
      this.$emit('add-device', device)
    }
  }
}
</script>

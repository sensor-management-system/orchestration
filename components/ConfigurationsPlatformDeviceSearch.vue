<template>
  <div>
    <v-row>
      <v-col cols="12">
        Add platforms and devices:
      </v-col>
    </v-row>
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
          max-height="450"
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
          max-height="450"
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
                  <v-btn
                    :key="'btn-add-device-' + item.id"
                    :disabled="isDeviceUsedFunc(item)"
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

import Platform from '@/models/Platform'
import Device from '@/models/Device'

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
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsPlatformDeviceSearch extends Vue {
  private searchTypes: string[] = [
    SearchType.Platform,
    SearchType.Device
  ]

  private searchOptions: ISearchOptions = {
    searchType: SearchType.Platform,
    text: ''
  }

  private platformsResult: Platform[] = [] as Platform[]
  private devicesResult: Device[] = [] as Device[]

  private platformItem: string = ''
  private deviceItem: string = ''

  @Prop({
    default: () => false,
    type: Function
  })
  // @ts-ignore
  readonly isDeviceUsedFunc: IsDeviceUsedFunc

  @Prop({
    default: () => false,
    type: Function
  })
  // @ts-ignore
  readonly isPlatformUsedFunc: IsPlatformUsedFunc

  get platforms (): Platform[] {
    return this.platformsResult
  }

  set platforms (platforms: Platform[]) {
    this.platformsResult = platforms
    if (platforms.length) {
      this.devicesResult = [] as Device[]
    }
  }

  get devices (): Device[] {
    return this.devicesResult
  }

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
          .withTextInName(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        break
      case SearchType.Device:
        this.devices = await this.$api.devices.newSearchBuilder()
          .withTextInName(this.searchOptions.text)
          .build()
          .findMatchingAsList()
        break
      default:
        throw new TypeError('search function not defined for unknown value')
    }
  }

  addPlatform (platform: Platform) {
    this.$emit('add-platform', platform)
  }

  addDevice (device: Device) {
    this.$emit('add-device', device)
  }
}
</script>

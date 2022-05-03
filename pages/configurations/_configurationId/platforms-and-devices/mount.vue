<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/configurations/' + configurationId + '/platforms-and-devices'"
      >
        cancel
      </v-btn>
    </v-card-actions>
    <v-stepper
      v-model="step"
    >
      <v-stepper-header>
        <v-stepper-step
          editable
          :complete="!!selectedDate"
          step="1"
        >
          Select a date
        </v-stepper-step>
        <v-stepper-step
          :editable="!!selectedDate"
          :rules="[()=>!!selectedDate]"
          step="2"
        >
          Choose node
        </v-stepper-step>
        <v-stepper-step
          :editable="!!selectedDate"
          :rules="[()=>!!selectedDate]"
          step="3"
        >
          Select device or platform
        </v-stepper-step>
        <v-stepper-step
          :editable="!!selectedDate && (isDeviceSelectedForMount || isPlatformSelectedForMount)"
          :rules="[()=>!!selectedDate && (isDeviceSelectedForMount || isPlatformSelectedForMount)]"
          step="4"
        >
          Submit
        </v-stepper-step>
      </v-stepper-header>
      <v-stepper-items>
        <v-stepper-content step="1">
          <v-row justify="center">
            <v-col cols="12" md="6">
              <DateTimePicker
                v-model="selectedDate"
                placeholder="e.g. 2000-01-31 12:00"
                label="Select a date"
              />
            </v-col>
          </v-row>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-row justify="center">
            <v-col cols="12" md="6">
              <v-card class="my-2">
                <v-container>
                  <v-row no-gutters>
                    <v-col>
                      <v-alert
                        border="top"
                        colored-border
                        type="info"
                        elevation="2"
                      >
                        <div>
                          Select a platform node (<v-icon>mdi-rocket-outline</v-icon>) to add a device or platform to it.
                        </div>
                        <div>
                          To add a device or platform directly to a configuration don't select anything.
                        </div>
                        <div>
                          You can deselect by clicking on a selected node.
                        </div>
                        <div>
                          You can't attach a device or platform to a mounted device (<v-icon>mdi-network-outline</v-icon>).
                        </div>
                      </v-alert>
                    </v-col>
                  </v-row>

                  <ConfigurationsTreeView
                    v-if="configuration"
                    ref="treeView"
                    v-model="selectedNode"
                    :items="tree"
                  />
                </v-container>
              </v-card>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="3">
          <v-row>
            <v-col>
              <v-card>
                <v-toolbar
                  color="grey"
                  dark
                  flat
                >
                  <v-spacer />
                  <v-toolbar-title>Search</v-toolbar-title>

                  <v-spacer />

                  <template #extension>
                    <v-tabs
                      v-model="tab"
                      centered
                      slider-color="yellow"
                    >
                      <v-tab>Platform</v-tab>
                      <v-tab>Device</v-tab>
                    </v-tabs>
                  </template>
                </v-toolbar>

                <v-tabs-items v-model="tab">
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
                        <div v-if="platforms.length>0">
                          <v-subheader>
                            <template v-if="platforms.length == 1">
                              1 device found
                            </template>
                            <template v-else>
                              {{ platforms.length }} platforms found
                            </template>
                            <v-spacer />
                          </v-subheader>
                          <BaseList
                            :list-items="platforms"
                          >
                            <template #list-item="{item}">
                              <PlatformMountListItem
                                :key="item.id"
                                :platform="item"
                              >
                                <template #mount>
                                  <ConfigurationsPlatformDeviceMountForm
                                    data-role-btn="add-platform"
                                    :readonly="false"
                                    :contacts="contacts"
                                    :current-user-mail="currentUserMail"
                                    @add="setPlatformToMount(item, $event)"
                                  />
                                </template>
                              </PlatformMountListItem>
                            </template>
                          </BaseList>
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
                        </v-row>
                        <div v-if="devices.length>0">
                          <v-subheader>
                            <template v-if="devices.length == 1">
                              1 device found
                            </template>
                            <template v-else>
                              {{ devices.length }} devices found
                            </template>
                            <v-spacer />
                          </v-subheader>
                          <BaseList
                            :list-items="devices"
                          >
                            <template #list-item="{item}">
                              <DevicesMountListItem
                                :key="item.id"
                                :device="item"
                              >
                                <template #mount>
                                  <ConfigurationsPlatformDeviceMountForm
                                    data-role-btn="add-device"
                                    :readonly="false"
                                    :contacts="contacts"
                                    :current-user-mail="currentUserMail"
                                    @add="setDeviceToMount(item, $event)"
                                  />
                                </template>
                              </DevicesMountListItem>
                            </template>
                          </BaseList>
                        </div>
                      </v-container>
                    </v-card>
                  </v-tab-item>
                </v-tabs-items>
              </v-card>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="4">
          <v-row justify="center">
            <v-col cols="12" md="6">
              <v-row>
                <v-col cols="3">
                  Selected Date
                </v-col>
                <v-col cols="9">
                  {{ selectedDate|dateToDateTimeStringHHMM }}
                </v-col>
              </v-row>
              <v-divider />
              <v-row>
                <v-col cols="3">
                  Selected Parent Platform
                </v-col>
                <v-col v-if="selectedNode && selectedNode.isPlatform()">
                  {{ selectedNode.unpack().platform.shortName }}
                </v-col>
                <v-col v-else>
                  No parent platform selected
                </v-col>
              </v-row>
              <v-divider />
              <v-row v-if="isPlatformSelectedForMount">
                <v-col cols="3">
                  Platform to mount
                </v-col>
                <v-col>{{ platformToMount.platform.shortName }}</v-col>
              </v-row>
              <v-row v-if="isDeviceSelectedForMount">
                <v-col cols="3">
                  Device to mount
                </v-col>
                <v-col>{{ deviceToMount.device.shortName }}</v-col>
              </v-row>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-btn
                block
                color="primary"
                @click="mount"
              >
                Submit
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DateTime } from 'luxon'
import { mapActions, mapGetters, mapState } from 'vuex'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { buildConfigurationTree } from '@/modelUtils/mountHelpers'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import DevicesMountListItem from '@/components/devices/DevicesMountListItem.vue'
import ConfigurationsPlatformDeviceMountForm from '@/components/ConfigurationsPlatformDeviceMountForm.vue'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import PlatformMountListItem from '@/components/platforms/PlatformMountListItem.vue'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import HintCard from '@/components/HintCard.vue'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Configuration } from '@/models/Configuration'
import { IDeviceSearchParams } from '@/modelUtils/DeviceSearchParams'
import { IPlatformSearchParams } from '@/modelUtils/PlatformSearchParams'

@Component({
  components: { ProgressIndicator, HintCard, PlatformMountListItem, ConfigurationsPlatformDeviceMountForm, DevicesMountListItem, DevicesListItem, BaseList, DateTimePicker, ConfigurationsTreeView },
  middleware: ['auth'],
  filters: { dateToDateTimeStringHHMM },
  computed: {
    ...mapGetters('configurations', ['mountingActionsDates']),
    ...mapState('configurations', ['configuration']),
    ...mapState('devices', ['devices']),
    ...mapState('platforms', ['platforms']),
    ...mapState('contacts', ['contacts'])
  },
  methods: {
    ...mapActions('devices', ['searchDevices']),
    ...mapActions('platforms', ['searchPlatforms']),
    ...mapActions('configurations', ['addDeviceMountAction', 'addPlatformMountAction', 'loadConfiguration']),
    ...mapActions('contacts', ['loadAllContacts'])
  }
})
export default class ConfigurationMountPlatformsAndDevicesPage extends Vue {
  private isSaving = false
  private isLoading = false

  private tab = null
  private step = 1

  private searchTextPlatforms: string|null = null
  private searchTextDevices: string|null = null
  private selectedType: string|null = null
  private selectedNode: ConfigurationsTreeNode | null = null
  private selectedDate = DateTime.utc()
  private platformToMount: {platform:Platform,mountInfo:{}}|null = null
  private deviceToMount: {device:Device,mountInfo:{}}|null = null

  // vuex definition for typescript check
  loadAllContacts!:()=>void
  configuration!:Configuration
  searchDevices!:(searchParams: IDeviceSearchParams)=>void
  searchPlatforms!:(searchParams: IPlatformSearchParams)=>void
  addDeviceMountAction!:(    {
    configurationId,
    deviceMountAction
  }: { configurationId: string, deviceMountAction: DeviceMountAction })=>Promise<void>
  addPlatformMountAction!:( {
    configurationId,
    platformMountAction
  }: { configurationId: string, platformMountAction: PlatformMountAction })=>Promise<void>
  loadConfiguration!: (id: string)=>void

  async created () {
    try {
      this.isLoading = true
      await this.loadAllContacts()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.isLoading = false
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get tree () {
    const selectedNodeId = this.selectedNode?.id
    const tree = buildConfigurationTree(this.configuration, this.selectedDate)
    if (selectedNodeId) {
      const node = tree.getById(selectedNodeId)
      if (node) {
        this.selectedNode = node
      }
    }
    return tree.toArray()
  }

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  clearBasicSearchPlatforms () {
    this.searchTextPlatforms = null
  }

  clearBasicSearchDevices () {
    this.searchTextPlatforms = null
  }

  async searchDevicesForMount () {
    try {
      this.isLoading = true
      await this.searchDevices({ searchText: this.searchTextDevices })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of devices failed')
    } finally {
      this.isLoading = false
    }
  }

  async searchPlatformsForMount () {
    try {
      this.isLoading = true
      await this.searchPlatforms({ searchText: this.searchTextPlatforms })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of platforms failed')
    } finally {
      this.isLoading = false
    }
  }

  mount () {
    if (this.isPlatformSelectedForMount) {
      this.mountPlatform(this.platformToMount!.platform, this.platformToMount!.mountInfo)
    }
    if (this.isDeviceSelectedForMount) {
      this.mountDevice(this.deviceToMount!.device, this.deviceToMount!.mountInfo)
    }
  }

  mountDevice (device:Device, mountInfo:any) {
    try {
      if (this.selectedNode && !this.selectedNode.canHaveChildren()) {
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      this.isSaving = true

      let parentPlatform = null

      if (this.selectedNode && this.selectedNode.canHaveChildren()) {
        parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
      }

      const newDeviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform,
        date: this.selectedDate,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        contact: mountInfo.contact,
        description: mountInfo.description
      })

      this.addDeviceMountAction({
        configurationId: this.configurationId,
        deviceMountAction: newDeviceMountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add device mount action')
    } finally {
      this.isSaving = false
    }
  }

  async mountPlatform (platform:Platform, mountInfo:any) {
    try {
      if (this.selectedNode && !this.selectedNode.canHaveChildren()) {
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      let parentPlatform = null

      this.isSaving = true

      if (this.selectedNode && this.selectedNode.canHaveChildren()) {
        parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
      }

      const newPlatformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform,
        date: this.selectedDate,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        contact: mountInfo.contact,
        description: mountInfo.description
      })

      await this.addPlatformMountAction({
        configurationId: this.configurationId,
        platformMountAction: newPlatformMountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add platform mount action')
    } finally {
      this.isSaving = false
    }
  }

  setPlatformToMount (platform:Platform, mountInfo: any) {
    this.deviceToMount = null
    this.platformToMount = {
      platform,
      mountInfo
    }
    this.$store.commit('snackbar/setSuccess', 'Selected platform confirmed')
  }

  setDeviceToMount (device:Device, mountInfo:any) {
    this.platformToMount = null

    this.deviceToMount = {
      device,
      mountInfo
    }
    this.$store.commit('snackbar/setSuccess', 'Selected device confirmed')
  }

  get isPlatformSelectedForMount () {
    return this.platformToMount !== null && this.deviceToMount === null
  }

  get isDeviceSelectedForMount () {
    return this.platformToMount === null && this.deviceToMount !== null
  }
}
</script>

<style scoped>

</style>

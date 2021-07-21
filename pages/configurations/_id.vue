<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
    <v-card
      outlined
    >
      <v-tabs-items
        v-model="activeTab"
      >
        <!-- Configuration -->
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <v-row>
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="configuration.label"
                    label="Label"
                    :readonly="readonly"
                    :disabled="readonly"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-combobox
                    v-model="configuration.status"
                    :items="configurationStates"
                    label="Status"
                    :readonly="readonly"
                    :disabled="readonly"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-combobox
                    v-model="configurationProjectName"
                    :items="projectNames"
                    label="Project"
                    :readonly="readonly"
                    :disabled="readonly"
                  />
                </v-col>
              </v-row>
              <v-form
                ref="datesForm"
                v-model="datesAreValid"
                @submit.prevent
              >
                <v-row>
                  <v-col cols="12" md="3">
                    <date-time-picker
                      :value="configuration.startDate"
                      label="Start date"
                      placeholder="e.g. 2000-01-31 12:00"
                      :rules="[rules.startDate]"
                      :readonly="readonly"
                      :disabled="readonly"
                      @input="setStartDateAndValidate"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <date-time-picker
                      :value="configuration.endDate"
                      label="End date"
                      placeholder="e.g. 2001-01-31 12:00"
                      :rules="[rules.endDate]"
                      :readonly="readonly"
                      :disabled="readonly"
                      @input="setEndDateAndValidate"
                    />
                  </v-col>
                </v-row>
              </v-form>
              <v-row>
                <v-col cols="12" md="3">
                  <v-form
                    ref="locationTypeForm"
                    v-model="locationTypeIsValid"
                    @submit.prevent
                  >
                    <v-select
                      v-model="locationType"
                      label="Location type"
                      :rules="[rules.locationType]"
                      :items="['Stationary', 'Dynamic']"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
                  </v-form>
                </v-col>
              </v-row>
              <div v-if="locationType === 'Stationary'">
                <v-row>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model.number.lazy="configuration.location.latitude"
                      label="Latitude (WGS84)"
                      type="number"
                      :readonly="readonly"
                      :disabled="readonly"
                      @wheel.prevent
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model.number.lazy="configuration.location.longitude"
                      label="Longitude (WGS84)"
                      type="number"
                      :readonly="readonly"
                      :disabled="readonly"
                      @wheel.prevent
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model.number="configuration.location.elevation"
                      label="Elevation (m asl)"
                      type="number"
                      :readonly="readonly"
                      :disabled="readonly"
                      @wheel.prevent
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <div id="map-wrap" style="height: 300px">
                      <no-ssr>
                        <l-map :zoom="10" :center="location" style="z-index:0">
                          <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
                          <l-marker :lat-lng="location" />
                        </l-map>
                      </no-ssr>
                    </div>
                  </v-col>
                </v-row>
              </div>
              <div v-if="locationType === 'Dynamic'">
                <v-row>
                  <v-col cols="12" md="3">
                    <DevicePropertyHierarchySelect
                      v-model="configuration.location.latitude"
                      :devices="getAllDevices()"
                      device-select-label="Device that measures latitude"
                      property-select-label="Measured quantity for latitude"
                      :readonly="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <DevicePropertyHierarchySelect
                      v-model="configuration.location.longitude"
                      :devices="getAllDevices()"
                      device-select-label="Device that measures longitude"
                      property-select-label="Measured quantity for longitude"
                      :readonly="readonly"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <DevicePropertyHierarchySelect
                      v-model="configuration.location.elevation"
                      :devices="getAllDevices()"
                      device-select-label="Device that measures elevation"
                      property-select-label="Measured quantity for elevation"
                      :readonly="readonly"
                    />
                  </v-col>
                </v-row>
              </div>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- Platforms and Devices -->
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <v-row>
                <v-col cols="12" md="3">
                  <DateTimePicker
                    :value="selectedDate"
                    placeholder="e.g. 2000-01-31 12:00"
                    label="Configuration at date"
                    :rules="[rules.dateNotNull]"
                    @input="setSelectedDate"
                  />
                </v-col>
                <v-col>
                  <v-select
                    v-model="selectedDate"
                    :item-value="(x) => x.date"
                    :item-text="(x) => x.text"
                    :items="actionDates"
                    label="Dates defined by actions"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="6">
                  <ConfigurationsTreeView
                    ref="treeView"
                    v-model="tree"
                    :selected="selectedNode"
                    @select="setSelectedNode"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <InfoBox v-if="!selectedNode && !readonly">
                    Select a platform on the left side to add devices or platforms to it. To add a device or platform to the root of this configuration, deselect any previously selected device or platform.
                  </InfoBox>
                  <ConfigurationsSelectedItem
                    :value="getSelectedNode"
                    :breadcrumbs="hierarchyNodeNames"
                    :selected-date="selectedDate"
                    :readonly="readonly"
                    :contacts="contacts"
                    @remove="removeSelectedNode"
                    @overwriteExistingMountAction="overwriteExistingMountAction"
                    @addNewMountAction="addNewMountAction"
                  />
                  <ConfigurationsPlatformDeviceSearch
                    v-if="!readonly && (!selectedNode || selectedNode.isPlatform())"
                    :is-platform-used-func="isPlatformInTree"
                    :is-device-used-func="isDeviceInTree"
                    :selected-date="selectedDate"
                    :contacts="contacts"
                    @add-platform="addPlatformNode"
                    @add-device="addDeviceNode"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- Contact -->
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <v-row>
                <v-col cols="3">
                  <ContactSelect v-model="configuration.contacts" label="Add a contact" :readonly="readonly" />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- Actions -->
        <v-tab-item :eager="true">
          <v-card
            flat
          >
            <v-card-text>
              <div v-if="timelineActions.length === 0">
                <p class="text-center">
                  There are no actions for this configuration yet.
                </p>
              </div>
              <v-timeline v-else dense>
                <v-timeline-item
                  v-for="action in timelineActions"
                  :key="action.key"
                  :color="action.color"
                  :icon="action.icon"
                  class="mb-4"
                  small
                >
                  <v-card>
                    <v-card-subtitle class="pb-0">
                      {{ action.date | toUtcDate }}
                    </v-card-subtitle>
                    <v-card-title class="pt-0">
                      {{ action.title }}
                    </v-card-title>
                    <v-card-subtitle>
                      <v-row no-gutters>
                        <v-col cols="11">
                          {{ action.contact.toString() }}
                        </v-col>
                        <v-col
                          align-self="end"
                          class="text-right"
                        >
                          <v-btn
                            icon
                            @click.stop.prevent="showTimelineAction(action.key)"
                          >
                            <v-icon>{{ isTimelineActionShown(action.key) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-card-subtitle>
                    <v-expand-transition>
                      <v-card-text
                        v-show="isTimelineActionShown(action.key)"
                        class="text--primary"
                      >
                        <v-row
                          v-if="action.mountInfo && action.mountInfo.parentPlatform"
                          dense
                        >
                          <v-col cols="12" md="4">
                            <label>Mounted on</label>
                            {{ action.mountInfo.parentPlatform.shortName }}
                          </v-col>
                        </v-row>
                        <v-row
                          v-if="action.mountInfo"
                          dense
                        >
                          <v-col cols="12" md="3">
                            <label>Offset x</label>
                            {{ action.mountInfo.offsetX }}
                          </v-col>
                          <v-col cols="12" md="3">
                            <label>Offset y</label>
                            {{ action.mountInfo.offsetY }}
                          </v-col>
                          <v-col cols="12" md="3">
                            <label>Offset z</label>
                            {{ action.mountInfo.offsetZ }}
                          </v-col>
                        </v-row>
                        <v-row dense>
                          <v-col>
                            <label>Description</label>
                            {{ action.description }}
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-expand-transition>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
      <v-btn
        v-if="!editMode && isLoggedIn"
        fab
        fixed
        bottom
        right
        color="secondary"
        @click="onEditButtonClick"
      >
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import ContactSelect from '@/components/ContactSelect.vue'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsDemoTreeView from '@/components/ConfigurationsDemoTreeView.vue'
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import InfoBox from '@/components/InfoBox.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { IMountActions } from '@/models/IMountActions'
import { buildConfigurationTree, byDateOldestLast, mountDevice, mountPlatform, unmount } from '@/modelUtils/mountHelpers'
import { Platform } from '@/models/Platform'
import { Project } from '@/models/Project'

import { DynamicLocation, LocationType, StationaryLocation } from '@/models/Location'
import { Configuration } from '@/models/Configuration'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'

import { getParentByClass } from '@/utils/domHelper'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

const toUtcDate = (dt: DateTime) => {
  return dt.toUTC().toFormat('yyyy-MM-dd TT')
}

interface IActionDateWithText {
  date: DateTime
  text: string
}

interface IMountInfo {
  parentPlatform: Platform | null
  offsetX: number
  offsetY: number
  offsetZ: number
}

interface ITimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  mountInfo : IMountInfo | null
  description: string
}

class PlatformMountTimelineAction implements ITimelineAction {
  private mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Platform-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.platform.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

class DeviceMountTimelineAction implements ITimelineAction {
  private mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Device-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.device.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

class PlatformUnmountTimelineAction implements ITimelineAction {
  private unmountAction: PlatformUnmountAction

  constructor (unmountAction: PlatformUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Platform-unmount-action-' + this.unmountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.platform.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}

class DeviceUnmountTimelineAction implements ITimelineAction {
  private unmountAction: DeviceUnmountAction

  constructor (unmountAction: DeviceUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Device-unmount-action-' + this.unmountAction.device.id + this.unmountAction.date.toString()
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.device.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}

@Component({
  components: {
    DateTimePicker,
    ContactSelect,
    DevicePropertyHierarchySelect,
    ConfigurationsPlatformDeviceSearch,
    ConfigurationsTreeView,
    ConfigurationsDemoTreeView,
    ConfigurationsSelectedItem,
    InfoBox,
    ProgressIndicator
  },
  filters: {
    toUtcDate
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private isLoading: boolean = false
  private isSaving: boolean = false
  private editMode: boolean = false

  private configuration: Configuration = new Configuration()
  private configurationBackup: Configuration | null = null

  private projects: Project[] = []
  private configurationStates: string[] = []
  private contacts: Contact[] = []

  private selectedNode: ConfigurationsTreeNode | null = null
  private today: DateTime = DateTime.utc()
  private selectedDate: DateTime = this.today

  private rules: Object = {
    startDate: this.validateInputForStartDate,
    endDate: this.validateInputForEndDate,
    locationType: this.validateInputForLocationType,
    dateNotNull: this.mustBeProvided('Date')
  }

  private visibleTimelineActions: {[idx: string]: boolean} = {}

  validateInputForStartDate (v: string): boolean | string {
    if (v === null || v === '' || this.configuration.startDate === null) {
      return true
    }
    if (!this.configuration.endDate) {
      return true
    }
    if (this.configuration.startDate <= this.configuration.endDate) {
      return true
    }
    return 'Start date must not be after end date'
  }

  validateInputForEndDate (v: string): boolean | string {
    if (v === null || v === '' || this.configuration.endDate === null) {
      return true
    }
    if (!this.configuration.startDate) {
      return true
    }
    if (this.configuration.endDate >= this.configuration.startDate) {
      return true
    }
    return 'End date must not be before start date'
  }

  validateInputForLocationType (v: string): boolean | string {
    if (v === LocationType.Stationary) {
      return true
    }
    if (v === LocationType.Dynamic) {
      return true
    }
    return 'Location type must be set'
  }

  checkValidationOfAllFields () {
    // run the registered validations and show errors on the page
    this.checkValidationOfDates()
    this.checkValidationOfLocationType()
  }

  checkValidationOfDates () {
    (this.$refs.datesForm as Vue & { validate: () => boolean }).validate()
  }

  checkValidationOfLocationType () {
    (this.$refs.locationTypeForm as Vue & { validate: () => boolean }).validate()
  }

  /**
   * a rule to check that an field is non-empty
   *
   * @param {string} fieldname - the (human readable) label of the field
   * @return {(v: any) => boolean | string} a function that checks whether the field is valid or an error message
   */
  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    return function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
  }

  private datesAreValid: boolean = true
  private locationTypeIsValid: boolean = true

  get formIsValid () : boolean {
    return this.datesAreValid && this.locationTypeIsValid
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  created () {
    this.registerButtonActions()
    this.initializeAppBar()
  }

  mounted () {
    this.$api.configurationStates.findAll().then((foundStates) => {
      this.configurationStates = foundStates
    })
    this.$api.projects.findAll().then((foundProjects) => {
      this.projects = foundProjects
    })
    this.$api.contacts.findAll().then((foundContacts) => {
      this.contacts = foundContacts
    })
    this.isLoading = true
    this.loadConfiguration().then((_configuration) => {
      if (_configuration === null) {
        this.$store.commit('appbar/setTitle', 'Add Configuration')
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading configuration failed')
    }).finally(() => {
      this.isLoading = false
    })
  }

  loadConfiguration (): Promise<Configuration|null> {
    return new Promise((resolve, reject) => {
      const configurationId = this.$route.params.id
      if (!configurationId || configurationId === 'new') {
        this.createBackup()
        this.editMode = true && this.isLoggedIn
        resolve(null)
        return
      }
      this.editMode = false
      this.$api.configurations.findById(configurationId).then((foundConfiguration) => {
        this.configuration = foundConfiguration
        resolve(foundConfiguration)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  beforeDestroy () {
    this.unregisterButtonActions()
    this.$store.dispatch('appbar/setDefaults')
  }

  registerButtonActions () {
    this.$nuxt.$on('AppBarEditModeContent:save-btn-click', () => {
      this.checkValidationOfAllFields()
      if (!this.formIsValid) {
        this.showValidationError()
        return
      }
      this.save().then(() => {
        // when a new configuration was saved, change the URL accordingly
        if (this.configuration.id && this.$route.params.id !== this.configuration.id) {
          this.$router.push('/configurations/' + this.configuration.id)
        }
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      }).catch(() => {
        this.$store.commit('snackbar/setError', 'Save failed')
      })
    })
    this.$nuxt.$on('AppBarEditModeContent:cancel-btn-click', () => {
      this.cancel()
    })
  }

  unregisterButtonActions () {
    this.$nuxt.$off('AppBarEditModeContent:save-btn-click')
    this.$nuxt.$off('AppBarEditModeContent:cancel-btn-click')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Configuration',
        'Platforms and Devices',
        // 'Setup',
        'Contacts',
        'Actions'
      ],
      title: 'Configurations',
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

  save (): Promise<Configuration> {
    return new Promise((resolve, reject) => {
      this.isSaving = true
      this.$api.configurations.save(this.configuration).then((savedConfiguration) => {
        this.configuration = savedConfiguration
        this.configurationBackup = null
        this.editMode = false
        resolve(savedConfiguration)
      }).catch((error) => {
        reject(error)
      }).finally(() => {
        this.isSaving = false
      })
    })
  }

  cancel () {
    this.restoreBackup()
    if (this.configuration.id) {
      this.editMode = false
    } else {
      this.$router.push('/configurations')
    }
  }

  onEditButtonClick () {
    this.createBackup()
    this.editMode = true && this.isLoggedIn
  }

  createBackup () {
    this.configurationBackup = Configuration.createFromObject(this.configuration)
  }

  restoreBackup () {
    if (!this.configurationBackup) {
      return
    }
    this.configuration = this.configurationBackup
    this.configurationBackup = null
  }

  get readonly () {
    return !this.editMode
  }

  get locationType (): string | null {
    switch (true) {
      case (this.configuration.location instanceof StationaryLocation):
        return LocationType.Stationary
      case (this.configuration.location instanceof DynamicLocation):
        return LocationType.Dynamic
      default:
        return null
    }
  }

  set locationType (locationType: string | null) {
    switch (locationType) {
      case LocationType.Stationary:
        if (!(this.configuration.location instanceof StationaryLocation)) {
          this.configuration.location = new StationaryLocation()
        }
        this.checkValidationOfLocationType()
        break
      case LocationType.Dynamic:
        if (!(this.configuration.location instanceof DynamicLocation)) {
          this.configuration.location = new DynamicLocation()
        }
        this.checkValidationOfLocationType()
        break
      default:
        this.configuration.location = null
    }
  }

  get location (): number[] {
    if (!this.configuration.location || !(this.configuration.location instanceof StationaryLocation)) {
      return [0, 0]
    }
    return [
      this.configuration.location.latitude || 0,
      this.configuration.location.longitude || 0
    ]
  }

  get getSelectedNode (): ConfigurationsTreeNode | null {
    return this.selectedNode
  }

  get hierarchyNodeNames (): Object[] {
    if (!this.selectedNode) {
      return []
    }

    const openInNewTab = true
    return this.tree.getPathObjects(this.selectedNode).map((selectedNode) => {
      // we not only handle the names here, but we also allow to have links to our
      // platforms and devices
      const subRoute = selectedNode.isPlatform() ? 'platforms' : 'devices'
      const id = selectedNode.elementId
      const path = subRoute + '/' + id

      let partTarget = {}
      let partLink = {}
      if (openInNewTab) {
        partTarget = {
          target: '_blank'
        }
        partLink = {
          href: path
        }
      } else {
        partLink = {
          to: path
        }
      }

      return {
        text: selectedNode.nameWithoutOffsets,
        ...partLink,
        ...partTarget
      }
    })
  }

  /**
   * returns whether a platform is in the tree or not
   *
   * @param {number} nodeId - the id of the node
   * @return {boolean} wheter the node was found or not
   */
  isPlatformInTree (platform: Platform): boolean {
    const platformId = platform.id
    if (platformId === null) {
      return false
    }
    return !!this.tree.getPlatformById(platformId)
  }

  /**
   * returns whether a device is in the tree or not
   *
   * @param {number} nodeId - the id of the node
   * @return {boolean} wheter the node was found or not
   */
  isDeviceInTree (device: Device): boolean {
    const deviceId = device.id
    if (deviceId === null) {
      return false
    }
    return !!this.tree.getDeviceById(deviceId)
  }

  /**
   * adds a PlatformNode to the tree
   *
   * @param {Platform} platform - the node to add
   */
  addPlatformNode (
    platform: Platform,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    contact: Contact,
    description: string
  ): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    const date: DateTime = this.selectedDate || this.today

    const mountActions = mountPlatform(this.configuration, platform, offsetX, offsetY, offsetZ, contact, description, node, date)
    this.setMountActionsIntoConfiguraton(mountActions)
  }

  /**
   * adds a DeviceNode to the tree
   *
   * @param {Device} device - the node to add
   */
  addDeviceNode (
    device: Device,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    contact: Contact,
    description: string
  ): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    const date: DateTime = this.selectedDate || this.today
    const mountActions = mountDevice(this.configuration, device, offsetX, offsetY, offsetZ, contact, description, node, date)
    this.setMountActionsIntoConfiguraton(mountActions)
  }

  setMountActionsIntoConfiguraton (mountActions: IMountActions) {
    this.configuration.platformMountActions = mountActions.platformMountActions
    this.configuration.platformUnmountActions = mountActions.platformUnmountActions
    this.configuration.deviceMountActions = mountActions.deviceMountActions
    this.configuration.deviceUnmountActions = mountActions.deviceUnmountActions
  }

  /**
   * removes the selected node and sets the selected node to the parent
   */
  removeSelectedNode (_node: ConfigurationsTreeNode, contact: Contact, description: string) {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    if (!node) {
      return
    }

    const parentNode = this.tree.getParent(node)
    let parentNodeId: string | null = null
    if (parentNode) {
      parentNodeId = parentNode.id
    }
    const date = this.selectedDate || this.today
    const mountActions = unmount(this.configuration, node, date, contact, description)
    this.setMountActionsIntoConfiguraton(mountActions)

    if (parentNodeId) {
      const nodeWithTheSameId = this.tree.toArray().find(treeNode => treeNode.id === parentNodeId)
      if (nodeWithTheSameId) {
        this.selectedNode = nodeWithTheSameId
      } else {
        this.selectedNode = null
      }
    } else {
      this.selectedNode = null
    }
  }

  overwriteExistingMountAction (node: ConfigurationsTreeNode, newSettings: any) {
    if (node.isPlatform()) {
      const platformNode = node as PlatformNode
      const platformMountAction = platformNode.unpack()
      platformMountAction.offsetX = newSettings.offsetX
      platformMountAction.offsetY = newSettings.offsetY
      platformMountAction.offsetZ = newSettings.offsetZ
      platformMountAction.contact = newSettings.contact
      platformMountAction.description = newSettings.description
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = deviceNode.unpack()
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.contact = newSettings.contact
      deviceMountAction.description = newSettings.description
    }
  }

  addNewMountAction (node: ConfigurationsTreeNode, newSettings: any) {
    if (node.isPlatform()) {
      const platformNode = node as PlatformNode
      const platformMountAction = PlatformMountAction.createFromObject(platformNode.unpack())
      platformMountAction.offsetX = newSettings.offsetX
      platformMountAction.offsetY = newSettings.offsetY
      platformMountAction.offsetZ = newSettings.offsetZ
      platformMountAction.contact = newSettings.contact
      platformMountAction.description = newSettings.description
      platformMountAction.date = this.selectedDate
      this.configuration.platformMountActions.push(platformMountAction)
      this.selectedNode = new PlatformNode(platformMountAction)
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = DeviceMountAction.createFromObject(deviceNode.unpack())
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.contact = newSettings.contact
      deviceMountAction.description = newSettings.description
      deviceMountAction.date = this.selectedDate
      this.configuration.deviceMountActions.push(deviceMountAction)
      this.selectedNode = new DeviceNode(deviceMountAction)
    }
  }

  /**
   * returns an Array of all devices in the tree
   *
   * @return {Device[]} an Array of Devices
   */
  getAllDevices (): Device[] {
    const result = []
    const alreadyAddedDeviceIds = new Set()
    for (const deviceMountAction of this.configuration.deviceMountActions) {
      const device = deviceMountAction.device
      const deviceId = device.id
      if (!alreadyAddedDeviceIds.has(deviceId)) {
        result.push(device)
        alreadyAddedDeviceIds.add(deviceId)
      }
    }
    return result
  }

  setSelectedNode (node: ConfigurationsTreeNode) {
    this.selectedNode = node
  }

  setStartDateAndValidate (aDate: DateTime | null) {
    this.configuration.startDate = aDate
    if (this.configuration.endDate !== null) {
      this.checkValidationOfDates()
    }
  }

  setEndDateAndValidate (aDate: DateTime | null) {
    this.configuration.endDate = aDate
    if (this.configuration.startDate !== null) {
      this.checkValidationOfDates()
    }
  }

  showValidationError () {
    const invalidElement: Element | null = document.querySelector('.v-input.error--text')
    if (!invalidElement) {
      return
    }
    const parentElem: Element | null = getParentByClass(invalidElement, ['v-window-item'])
    if (!parentElem) {
      return
    }
    let tabIndex: number = -1
    document.querySelectorAll('.v-window-item').forEach((node, index) => {
      if (node === parentElem) {
        tabIndex = index
      }
    })
    if (tabIndex === -1) {
      return
    }
    this.$store.commit('appbar/setActiveTab', tabIndex)
    this.$store.commit('snackbar/setError', 'Please correct your errors.')
  }

  setSelectedDate (date: DateTime | null) {
    if (date) {
      this.selectedDate = date.setZone('utc')
    }
  }

  get configurationProjectName () {
    const uri = this.configuration.projectUri
    const projectIndex = this.projects.findIndex(p => p.uri === uri)
    if (projectIndex > -1) {
      return this.projects[projectIndex].name
    }
    return this.configuration.projectName
  }

  set configurationProjectName (newProjectName: string) {
    this.configuration.projectName = newProjectName
    const projectIndex = this.projects.findIndex(p => p.name === newProjectName)
    if (projectIndex > -1) {
      this.configuration.projectUri = this.projects[projectIndex].uri
    } else {
      this.configuration.projectUri = ''
    }
  }

  get projectNames () {
    return this.projects.map(p => p.name)
  }

  get tree () {
    const date = this.selectedDate || this.today
    const selectedNodeId = this.selectedNode?.id
    const tree = buildConfigurationTree(this.configuration, date)
    if (selectedNodeId) {
      const node = tree.getById(selectedNodeId)
      if (node) {
        this.selectedNode = node
      }
    }
    return tree
  }

  get actionDates (): IActionDateWithText[] {
    const datesWithTexts = []
    for (const platformMountAction of this.configuration.platformMountActions) {
      datesWithTexts.push({
        date: platformMountAction.date,
        text: 'Mount ' + platformMountAction.platform.shortName
      })
    }
    for (const platformUnmountAction of this.configuration.platformUnmountActions) {
      datesWithTexts.push({
        date: platformUnmountAction.date,
        text: 'Unmount ' + platformUnmountAction.platform.shortName
      })
    }
    for (const deviceMountAction of this.configuration.deviceMountActions) {
      datesWithTexts.push({
        date: deviceMountAction.date,
        text: 'Mount ' + deviceMountAction.device.shortName
      })
    }
    for (const deviceUnmountAction of this.configuration.deviceUnmountActions) {
      datesWithTexts.push({
        date: deviceUnmountAction.date,
        text: 'Unmount ' + deviceUnmountAction.device.shortName
      })
    }
    datesWithTexts.push({
      date: this.selectedDate,
      isSelected: true
    })
    datesWithTexts.push({
      date: this.today,
      isNow: true
    })

    const byDates: {[idx: number]: any[]} = {}
    for (const dateObject of datesWithTexts) {
      const key: number = dateObject.date.toMillis()
      if (!byDates[key]) {
        byDates[key] = [dateObject]
      } else {
        byDates[key].push(dateObject)
      }
    }
    const allDates: number[] = [...Object.keys(byDates)].map(x => parseFloat(x))
    allDates.sort()

    const result = []
    for (const key of allDates) {
      const value: any[] = byDates[key]
      const texts = value.filter(e => e.text).map(e => e.text)
      const isNow = value.filter(e => e.isNow).length > 0
      const isSelected = value.filter(e => e.isSelected).length > 0

      let text = String(value[0].date) + ' - '

      if (isNow) {
        text += 'Now'

        if (texts.length > 0) {
          text += ' + ' + texts.length + ' more mount/unmount'
          if (texts.length > 1) {
            text += ' actions'
          } else {
            text += ' action'
          }
        }
      } else if (texts.length > 0) {
        text += texts[0]

        if (texts.length > 1) {
          text += ' + ' + (texts.length - 1) + ' more mount/unmount'
          if (texts.length > 2) {
            text += ' actions'
          } else {
            text += ' action'
          }
        }
      } else if (isSelected) {
        text += 'Selected'
      }

      result.push({
        date: value[0].date,
        text
      })
    }
    return result
  }

  get timelineActions (): ITimelineAction[] {
    const result = []
    for (const platformMountAction of this.configuration.platformMountActions) {
      result.push(new PlatformMountTimelineAction(platformMountAction))
    }
    for (const deviceMountAction of this.configuration.deviceMountActions) {
      result.push(new DeviceMountTimelineAction(deviceMountAction))
    }
    for (const platformUnmountAction of this.configuration.platformUnmountActions) {
      result.push(new PlatformUnmountTimelineAction(platformUnmountAction))
    }
    for (const deviceUnmountAction of this.configuration.deviceUnmountActions) {
      result.push(new DeviceUnmountTimelineAction(deviceUnmountAction))
    }

    result.sort(byDateOldestLast)
    return result
  }

  showTimelineAction (key: string) {
    const show = !!this.visibleTimelineActions[key]
    Vue.set(this.visibleTimelineActions, key, !show)
  }

  isTimelineActionShown (key: string): boolean {
    return this.visibleTimelineActions[key]
  }

  unsetTimelineActionsShown (): void {
    this.visibleTimelineActions = {}
  }

  @Watch('configuration', { immediate: true, deep: true })
  // @ts-ignore
  onConfigurationChanged (val: Configuration) {
    if (val.id) {
      let title = 'Edit Configuration'
      if (val.label) {
        title = val.label
      }
      this.$store.commit('appbar/setTitle', title)
    }
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$store.commit('appbar/setSaveBtnHidden', !editMode)
    this.$store.commit('appbar/setCancelBtnHidden', !editMode)
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

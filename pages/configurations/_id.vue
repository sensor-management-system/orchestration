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
                    <DatePicker
                      :value="configuration.startDate"
                      label="Start date"
                      :rules="[rules.startDate]"
                      :readonly="readonly"
                      @input="setStartDateAndValidate"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <DatePicker
                      :value="configuration.endDate"
                      label="End date"
                      :rules="[rules.endDate]"
                      :readonly="readonly"
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
                <v-col cols="12" md="6">
                  <ConfigurationsDemoTreeView
                    v-if="!configuration.tree.length"
                  />
                  <ConfigurationsTreeView
                    v-else
                    ref="treeView"
                    v-model="configuration.tree"
                    :selected="selectedNode"
                    @select="setSelectedNode"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <InfoBox v-if="!selectedNode && !readonly">
                    Select a platform on the left side to add devices or platforms to it. To add a device or platform to the root of this configuration, deselect any previously selected device or platform.
                  </InfoBox>
                  <ConfigurationsSelectedItem
                    :value="selectedNode"
                    :breadcrumbs="hierarchyNodeNames"
                    :readonly="readonly"
                    @remove="removeSelectedNode"
                  />
                  <ConfigurationsPlatformDeviceSearch
                    v-if="!readonly && (!selectedNode || selectedNode.isPlatform())"
                    :can-add-devices="(selectedNode != null && selectedNode.isPlatform())"
                    :is-platform-used-func="isPlatformInTree"
                    :is-device-used-func="isDeviceInTree"
                    @add-platform="addPlatformNode"
                    @add-device="addDeviceNode"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- Setup -->
        <v-tab-item :eager="true">
          <PlatformConfigurationAttributesExpansionPanels
            v-model="configuration.platformAttributes"
            :readonly="readonly"
          />
          <DeviceConfigurationAttributesExpansionPanels
            v-model="configuration.deviceAttributes"
            :readonly="readonly"
          />
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

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'

import ContactSelect from '@/components/ContactSelect.vue'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import DeviceConfigurationAttributesExpansionPanels from '@/components/DeviceConfigurationAttributesExpansionPanels.vue'
import PlatformConfigurationAttributesExpansionPanels from '@/components/PlatformConfigurationAttributesExpansionPanels.vue'
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsDemoTreeView from '@/components/ConfigurationsDemoTreeView.vue'
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import InfoBox from '@/components/InfoBox.vue'
import DatePicker from '@/components/DatePicker.vue'

import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'
import { Project } from '@/models/Project'

import { StationaryLocation, DynamicLocation, LocationType } from '@/models/Location'
import { Configuration } from '@/models/Configuration'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformNode } from '@/models/PlatformNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

import { DateTime } from 'luxon'
import { stringToDate } from '@/utils/dateHelper'
import { getParentByClass } from '@/utils/domHelper'

@Component({
  components: {
    ContactSelect,
    DevicePropertyHierarchySelect,
    DeviceConfigurationAttributesExpansionPanels,
    PlatformConfigurationAttributesExpansionPanels,
    ConfigurationsPlatformDeviceSearch,
    ConfigurationsTreeView,
    ConfigurationsDemoTreeView,
    ConfigurationsSelectedItem,
    InfoBox,
    DatePicker
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private editMode: boolean = false

  private configuration: Configuration = new Configuration()
  private configurationBackup: Configuration | null = null

  private projects: Project[] = []
  private configurationStates: string[] = []

  private startDateMenu: boolean = false
  private endDateMenu: boolean = false

  private selectedNode: ConfigurationsTreeNode | null = null

  private rules: Object = {
    startDate: this.validateInputForStartDate,
    endDate: this.validateInputForEndDate,
    locationType: this.validateInputForLocationType
  }

  validateInputForStartDate (v: string): boolean | string {
    if (v === null || v === '') {
      return true
    }
    if (!this.configuration.endDate) {
      return true
    }
    if (stringToDate(v) <= this.configuration.endDate) {
      return true
    }
    return 'Start date must not be after end date'
  }

  validateInputForEndDate (v: string): boolean | string {
    if (v === null || v === '') {
      return true
    }
    if (!this.configuration.startDate) {
      return true
    }
    if (stringToDate(v) >= this.configuration.startDate) {
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

  private datesAreValid: boolean = true
  private locationTypeIsValid: boolean = true

  get formIsValid () : boolean {
    return this.datesAreValid && this.locationTypeIsValid
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
    this.loadConfiguration().then((_configuration) => {
      if (_configuration === null) {
        this.$store.commit('appbar/setTitle', 'Add Configuration')
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading configuration failed')
    })
  }

  loadConfiguration (): Promise<Configuration|null> {
    return new Promise((resolve, reject) => {
      const configurationId = this.$route.params.id
      if (!configurationId) {
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
        'Setup',
        'Contacts'
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
      this.$api.configurations.save(this.configuration).then((savedConfiguration) => {
        this.configuration = savedConfiguration
        this.configurationBackup = null
        this.editMode = false
        resolve(savedConfiguration)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  cancel () {
    this.restoreBackup()
    if (this.configuration.id) {
      this.editMode = false
    } else {
      this.$router.push('/search/configurations')
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

  get hierarchyNodeNames (): Object[] {
    if (!this.selectedNode) {
      return []
    }

    const openInNewTab = true
    return this.configuration.tree.getPathObjects(this.selectedNode).map((selectedNode) => {
      // we not only handle the names here, but we also allow to have links to our
      // platforms and devices
      const subRoute = selectedNode.isPlatform() ? 'platforms' : 'devices'
      const id = selectedNode.unpack().id
      const path = '/' + subRoute + '/' + id

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
        text: selectedNode.name,
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
    return !!this.configuration.tree.getPlatformById(platformId)
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
    return !!this.configuration.tree.getDeviceById(deviceId)
  }

  /**
   * adds a PlatformNode to the tree
   *
   * @param {Platform} platform - the node to add
   */
  addPlatformNode (platform: Platform): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    if (!node) {
      this.configuration.tree.push(
        new PlatformNode(platform)
      )
      this.addPlatformConfigurationAttribute(platform)
      return
    }

    if (!node.canHaveChildren()) {
      throw new Error('selected node-type cannot have children')
    }

    (node as PlatformNode).getTree().push(new PlatformNode(platform))
    this.addPlatformConfigurationAttribute(platform)
  }

  addPlatformConfigurationAttribute (platform: Platform): number {
    const index = this.configuration.platformAttributes.findIndex(a => a.platform === platform)
    if (index === -1) {
      /*
       * instead of adding the attribute directly via push,
       * create a copy of the array with the new attribute
       * added to it, so that Vue can register the change
       * with its watchers. See https://vuejs.org/v2/api/#vm-watch
       */
      this.configuration.platformAttributes = [...this.configuration.platformAttributes, new PlatformConfigurationAttributes(platform)]
    }
    return this.configuration.platformAttributes.length
  }

  /**
   * adds a DeviceNode to the tree
   *
   * @param {Device} device - the node to add
   */
  addDeviceNode (device: Device): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    if (!node) {
      this.configuration.tree.push(
        new DeviceNode(device)
      )
      this.addDeviceConfigurationAttribute(device)
      return
    }

    if (!node.canHaveChildren()) {
      throw new Error('selected node-type cannot have children')
    }

    (node as PlatformNode).getTree().push(new DeviceNode(device))
    this.addDeviceConfigurationAttribute(device)
  }

  addDeviceConfigurationAttribute (device: Device): number {
    const index = this.configuration.deviceAttributes.findIndex(a => a.device === device)
    if (index === -1) {
      /*
       * instead of adding the attribute directly via push, create a copy of
       * the array with the new attribute added to it, so that Vue can register
       * the change with its watchers. See https://vuejs.org/v2/api/#vm-watch
       */
      this.configuration.deviceAttributes = [...this.configuration.deviceAttributes, new DeviceConfigurationAttributes(device)]
    }
    return this.configuration.deviceAttributes.length
  }

  /**
   * removes the selected node and sets the selected node to the parent
   */
  removeSelectedNode () {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    if (!node) {
      return
    }

    this.removeConfigurationAttributes(node)

    const parentNode = this.configuration.tree.getParent(node)
    this.configuration.tree.remove(node)
    this.selectedNode = parentNode
  }

  removeConfigurationAttributes (node: ConfigurationsTreeNode) {
    if (node.isPlatform()) {
      // as the platform can have childs in the tree, remove also the attributes of the children
      for (const child of (node as PlatformNode).children) {
        this.removeConfigurationAttributes(child)
      }
      this.removePlatformConfigurationAttribute((node as PlatformNode).unpack())
    } else if (node.isDevice()) {
      this.removeDeviceConfigurationAttribute((node as DeviceNode).unpack())
    }
  }

  removePlatformConfigurationAttribute (platform: Platform): number {
    const index = this.configuration.platformAttributes.findIndex(a => a.platform === platform)
    if (index > -1) {
      /*
       * instead of removing the attribute directly via splice, create a copy
       * of the array and remove the attribute from the copy, so that Vue can
       * register the change with its watchers. See
       * https://vuejs.org/v2/api/#vm-watch
       */
      const newArray: PlatformConfigurationAttributes[] = [...this.configuration.platformAttributes]
      newArray.splice(index, 1)
      this.configuration.platformAttributes = newArray
    }
    return this.configuration.platformAttributes.length
  }

  removeDeviceConfigurationAttribute (device: Device): number {
    const index = this.configuration.deviceAttributes.findIndex(a => a.device === device)
    if (index > -1) {
      /*
       * instead of removing the attribute directly via splice, create a copy
       * of the array and remove the attribute from the copy, so that Vue can
       * register the change with its watchers. See
       * https://vuejs.org/v2/api/#vm-watch
       */
      const newArray: DeviceConfigurationAttributes[] = [...this.configuration.deviceAttributes]
      newArray.splice(index, 1)
      this.configuration.deviceAttributes = newArray
    }
    return this.configuration.deviceAttributes.length
  }

  /**
   * returns an Array of all devices in the tree
   *
   * @return {Device[]} an Array of Devices
   */
  getAllDevices (): Device[] {
    const getDeviceNodesRecursive = (nodes: ConfigurationsTree, devices: DeviceNode[]) => {
      for (const node of nodes) {
        if (node.isDevice()) {
          devices.push(node as DeviceNode)
        }
        if (!node.canHaveChildren()) {
          continue
        }
        getDeviceNodesRecursive((node as PlatformNode).getTree(), devices)
      }
    }
    const deviceNodes: DeviceNode[] = []
    getDeviceNodesRecursive(this.configuration.tree, deviceNodes)
    return deviceNodes.map(n => n.unpack())
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

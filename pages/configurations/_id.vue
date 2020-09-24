<template>
  <div>
    <v-form>
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
                    <v-menu
                      v-if="!readonly"
                      v-model="startDateMenu"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          :value="startDateStringHelper"
                          v-bind="attrs"
                          label="Start date"
                          clearable
                          prepend-icon="mdi-calendar-range"
                          readonly
                          v-on="on"
                          @click:clear="configuration.startDate = null"
                        />
                      </template>
                      <v-date-picker
                        :value="startDateStringHelper"
                        first-day-of-week="1"
                        :show-week="true"
                        :max="endDateStringHelper"
                        @input="startDateStringHelper = $event; startDateMenu = false"
                      />
                    </v-menu>
                    <v-text-field
                      v-else
                      :value="startDateStringHelper"
                      label="Start date"
                      prepend-icon="mdi-calendar-range"
                      readonly
                      disabled
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-menu
                      v-if="!readonly"
                      v-model="endDateMenu"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          :value="endDateStringHelper"
                          v-bind="attrs"
                          label="End date"
                          clearable
                          prepend-icon="mdi-calendar-range"
                          readonly
                          v-on="on"
                          @click:clear="configuration.endDate = null"
                        />
                      </template>
                      <v-date-picker
                        :value="endDateStringHelper"
                        first-day-of-week="1"
                        :show-week="true"
                        :min="startDateStringHelper"
                        @input="endDateStringHelper = $event; endDateMenu = false"
                      />
                    </v-menu>
                    <v-text-field
                      v-else
                      :value="endDateStringHelper"
                      label="End date"
                      prepend-icon="mdi-calendar-range"
                      readonly
                      disabled
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="locationType"
                      label="Location type"
                      :items="['Stationary', 'Dynamic']"
                      :readonly="readonly"
                      :disabled="readonly"
                    />
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
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-text-field
                        v-model.number.lazy="configuration.location.longitude"
                        label="Longitude (WGS84)"
                        type="number"
                        :readonly="readonly"
                        :disabled="readonly"
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-text-field
                        v-model.number="configuration.location.elevation"
                        label="Elevation (m asl)"
                        type="number"
                        :readonly="readonly"
                        :disabled="readonly"
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
                        property-select-label="Property for latitude"
                        :readonly="readonly"
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <DevicePropertyHierarchySelect
                        v-model="configuration.location.longitude"
                        :devices="getAllDevices()"
                        device-select-label="Device that measures longitude"
                        property-select-label="Property for longitude"
                        :readonly="readonly"
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <DevicePropertyHierarchySelect
                        v-model="configuration.location.elevation"
                        :devices="getAllDevices()"
                        device-select-label="Device that measures elevation"
                        property-select-label="Property for elevation"
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
                    <ConfigurationsTreeView
                      ref="treeView"
                      v-model="configuration.tree"
                      :selected="selectedNode"
                      @select="setSelectedNode"
                    />
                  </v-col>
                  <v-col cols="6" md="6">
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
                    <ContactSelect v-model="contacts" label="Add a contact" :readonly="readonly" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-btn
          v-if="!isInEditMode"
          fab
          fixed
          bottom
          right
          color="secondary"
          @click="toggleEditMode"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<style lang="scss">
@import "~/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'

import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'
import ContactSelect from '@/components/ContactSelect.vue'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import DeviceConfigurationAttributesExpansionPanels from '@/components/DeviceConfigurationAttributesExpansionPanels.vue'
import PlatformConfigurationAttributesExpansionPanels from '@/components/PlatformConfigurationAttributesExpansionPanels.vue'
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import InfoBox from '@/components/InfoBox.vue'

import Contact from '@/models/Contact'
import Device from '@/models/Device'
import Platform from '@/models/Platform'

import { StationaryLocation, DynamicLocation } from '@/models/Location'
import { Configuration } from '@/models/Configuration'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformNode } from '@/models/PlatformNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

import { dateToString, stringToDate } from '@/utils/dateHelper'

enum LocationType {
  Stationary = 'Stationary',
  Dynamic = 'Dynamic'
}

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Configuration',
      'Platforms and Devices',
      'Setup',
      'Contacts'
    ]
  }
}

@Component({
  components: {
    ContactSelect,
    DevicePropertyHierarchySelect,
    DeviceConfigurationAttributesExpansionPanels,
    PlatformConfigurationAttributesExpansionPanels,
    ConfigurationsPlatformDeviceSearch,
    ConfigurationsTreeView,
    ConfigurationsSelectedItem,
    InfoBox
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private activeTab: number = 0
  private editMode: boolean = false

  private configuration = new Configuration()

  private startDateMenu: boolean = false
  private endDateMenu: boolean = false

  private contacts: Contact[] = []

  private selectedNode: ConfigurationsTreeNode | null = null

  private tree: ConfigurationsTree = new ConfigurationsTree()

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      this.toggleEditMode()
      // this.$router.push('/configurations')
    })

    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })
  }

  mounted () {
    this.loadConfiguration()
    this.$nextTick(() => {
      if (!this.$route.params.id) {
        this.$nuxt.$emit('AppBarContent:title', 'Add Configuration')
      }
      this.$nuxt.$emit('AppBarContent:save-button-hidden', !this.editMode)
      this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !this.editMode)
    })
  }

  loadConfiguration () {
    const configurationId = this.$route.params.id
    if (configurationId) {
      this.isInEditMode = false
      this.$api.configurations.findById(configurationId).then((foundConfiguration) => {
        this.configuration = foundConfiguration
      }).catch((_error) => {
        this.$store.commit('snackbar/setError', 'Loading configuration failed')
      })
    } else {
      this.isInEditMode = true
    }
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarContent:save-button-click')
    this.$nuxt.$off('AppBarContent:cancel-button-click')
    this.$nuxt.$off('AppBarExtension:change')
  }

  get isInEditMode (): boolean {
    return this.editMode
  }

  save () {
    this.toggleEditMode()
  }

  set isInEditMode (editMode: boolean) {
    this.editMode = editMode
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$nuxt.$emit('AppBarContent:save-button-hidden', !editMode)
    this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !editMode)
  }

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  get readonly () {
    return !this.isInEditMode
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
        break
      case LocationType.Dynamic:
        if (!(this.configuration.location instanceof DynamicLocation)) {
          this.configuration.location = new DynamicLocation()
        }
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
    return this.configuration.tree.getPath(this.selectedNode).map((t: string): Object => { return { text: t } })
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

  get startDateStringHelper (): string {
    return dateToString(this.configuration.startDate)
  }

  set startDateStringHelper (aDate: string) {
    this.configuration.startDate = stringToDate(aDate)
  }

  get endDateStringHelper (): string {
    return dateToString(this.configuration.endDate)
  }

  set endDateStringHelper (aDate: string) {
    this.configuration.endDate = stringToDate(aDate)
  }
}
</script>

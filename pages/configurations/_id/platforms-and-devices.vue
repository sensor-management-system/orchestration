<template>
  <v-card
    flat
  >
    <v-card-text>
      <v-row>
        <v-col cols="12" md="3">
          <DateTimePicker
            v-model="selectedDate"
            placeholder="e.g. 2000-01-31 12:00"
            label="Configuration at date"
            :rules="[rules.dateNotNull]"
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
          <InfoBox v-if="!selectedNode && isLoggedIn">
            Select a platform on the left side to add devices or platforms to it. To add a device or platform to the
            root of this configuration, deselect any previously selected device or platform.
          </InfoBox>
          <ConfigurationsSelectedItem
            :value="getSelectedNode"
            :breadcrumbs="hierarchyNodeNames"
            :selected-date="selectedDateOrFallback"
            :readonly="!isLoggedIn"
            :contacts="contacts"
            @remove="removeSelectedNode"
            @overwriteExistingMountAction="overwriteExistingMountAction"
            @addNewMountAction="addNewMountAction"
          />
          <ConfigurationsPlatformDeviceSearch
            v-if="isLoggedIn && (!selectedNode || selectedNode.isPlatform())"
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
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { Configuration } from '@/models/Configuration'
import { IMountActions } from '@/models/IMountActions'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { buildConfigurationTree, mountDevice, mountPlatform, unmount } from '@/modelUtils/mountHelpers'
import ConfigurationHelper from '@/utils/configurationHelper'
import { IActionDateWithText } from '@/utils/configurationInterfaces'
import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import InfoBox from '@/components/InfoBox.vue'
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'

@Component({
  components: {
    ConfigurationsPlatformDeviceSearch,
    InfoBox,
    ConfigurationsSelectedItem,
    ConfigurationsTreeView,
    DateTimePicker
  }
})
export default class ConfigurationPlatformsAndDevices extends Vue {
  private selectedNode: ConfigurationsTreeNode | null = null
  private today: DateTime = DateTime.utc()
  private selectedDate: DateTime = this.today
  private valueCopy: Configuration = new Configuration()
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  async created () {
    if (this.value) {
      this.valueCopy = Configuration.createFromObject(this.value)
    }
    try {
      await this.$store.dispatch('contacts/loadAllContacts')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    }
  }

  get configuration () {
    return this.valueCopy
  }

  get contacts (): Contact[] {
    return this.$store.state.contacts.allContacts
  }

  private rules: Object = {
    dateNotNull: Validator.mustBeProvided('Date')
  }

  get selectedDateOrFallback () {
    return this.selectedDate || this.today
  }

  get actionDates (): IActionDateWithText[] {
    return ConfigurationHelper.getActionDatesWithTextsByConfiguration(this.configuration, this.selectedDateOrFallback)
  }

  setSelectedNode (node: ConfigurationsTreeNode) {
    this.selectedNode = node
  }

  get tree () {
    const selectedNodeId = this.selectedNode?.id
    const tree = buildConfigurationTree(this.configuration, this.selectedDateOrFallback)
    if (selectedNodeId) {
      const node = tree.getById(selectedNodeId)
      if (node) {
        this.selectedNode = node
      }
    }
    return tree
  }

  get getSelectedNode (): ConfigurationsTreeNode | null {
    return this.selectedNode
  }

  get hierarchyNodeNames (): Object[] {
    return ConfigurationHelper.getHierarchyNodeNamesByTreeAndSelectedNode(this.tree, this.selectedNode)
  }

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
    const mountActions = unmount(this.configuration, node, this.selectedDateOrFallback, contact, description)
    this.setMountActionsIntoConfiguration(mountActions)

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
    ConfigurationHelper.overwriteExistingMountAction(node, newSettings)
  }

  addNewMountAction (node: ConfigurationsTreeNode, newSettings: any) {
    ConfigurationHelper.addNewMountAction(node, newSettings, this.configuration, this.selectedDate, this.selectedNode)
  }

  isPlatformInTree (platform: Platform): boolean {
    const platformId = platform.id
    if (platformId === null) {
      return false
    }
    return !!this.tree.getPlatformById(platformId)
  }

  isDeviceInTree (device: Device): boolean {
    const deviceId = device.id
    if (deviceId === null) {
      return false
    }
    return !!this.tree.getDeviceById(deviceId)
  }

  addPlatformNode (
    platform: Platform,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    contact: Contact,
    description: string
  ): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode

    const mountActions = mountPlatform(this.configuration, platform, offsetX, offsetY, offsetZ, contact, description, node, this.selectedDateOrFallback)
    this.setMountActionsIntoConfiguration(mountActions)
  }

  addDeviceNode (
    device: Device,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    contact: Contact,
    description: string
  ): void {
    const node: ConfigurationsTreeNode | null = this.selectedNode
    const mountActions = mountDevice(this.configuration, device, offsetX, offsetY, offsetZ, contact, description, node, this.selectedDateOrFallback)
    this.setMountActionsIntoConfiguration(mountActions)
  }

  setMountActionsIntoConfiguration (mountActions: IMountActions) {
    this.configuration.platformMountActions = mountActions.platformMountActions
    this.configuration.platformUnmountActions = mountActions.platformUnmountActions
    this.configuration.deviceMountActions = mountActions.deviceMountActions
    this.configuration.deviceUnmountActions = mountActions.deviceUnmountActions

    this.save()
  }

  async save () {
    try {
      this.$store.commit('configurations/setConfiguration', this.valueCopy)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Save successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    }
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChange (val: Configuration): void {
    this.valueCopy = Configuration.createFromObject(val)
  }
}
</script>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
          <InfoBox v-if="!selectedNode && $auth.loggedIn">
            Select a platform on the left side to add devices or platforms to it. To add a device or platform to the
            root of this configuration, deselect any previously selected device or platform.
          </InfoBox>
          <ConfigurationsSelectedItem
            :value="getSelectedNode"
            :breadcrumbs="hierarchyNodeNames"
            :selected-date="selectedDateOrFallback"
            :readonly="!$auth.loggedIn"
            :contacts="contacts"
            :current-user-mail="$auth.user.email"
            @remove="removeSelectedNode"
            @overwriteExistingMountAction="overwriteExistingMountAction"
            @addNewMountAction="addNewMountAction"
          />
          <ConfigurationsPlatformDeviceSearch
            v-if="$auth.loggedIn && (!selectedNode || selectedNode.isPlatform())"
            :is-platform-used-func="isPlatformInTree"
            :is-device-used-func="isDeviceInTree"
            :selected-date="selectedDate"
            :contacts="contacts"
            :current-user-mail="$auth.user.email"
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

  head () {
    return {
      titleTemplate: 'Platforms and Devices - %s'
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

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChange (val: Configuration): void {
    this.valueCopy = Configuration.createFromObject(val)
  }
}
</script>

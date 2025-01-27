<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-card-title class="pl-0">
        Unmount devices or platforms
      </v-card-title>
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
    <v-row>
      <v-col cols="12" md="3">
        <DateTimePicker
          :value="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          @input="setSelectedDate"
        />
      </v-col>
      <v-col>
        <v-select
          :value="selectedDate"
          :item-value="(x) => x.value"
          :item-text="(x) => x.text"
          :items="mountActionDateItems"
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          persistent-hint
          @input="setSelectedDate"
        />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="primary white--text">
            Mounted devices and platforms
          </v-card-title>
          <v-card-text>
            <ConfigurationsTreeView
              v-if="configuration && tree"
              ref="unmountTreeView"
              v-model="selectedNode"
              disable-per-node
              :tree="tree"
              show-detailed-name
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-slide-x-reverse-transition :hide-on-leave="true">
          <div v-show="showError">
            <v-alert v-if="selectedNode?.hasErrors" text type="error">
              <div v-for="(errorMessage, i) in selectedNode?.errors" :key="i" class="error--text mb-2">
                {{ errorMessage }}
              </div>
            </v-alert>
            <v-alert v-else-if="selectedNode?.hasChildErrors" text type="error">
              The following child {{ selectedNode.childrenWithErrors.length > 1 ? 'nodes prevent' : 'node prevents' }}
              unmounting:
              <div v-for="child in selectedNode?.childrenWithErrors" :key="child.id" class="mt-2">
                <expandable-content indent icon-color="error">
                  <template #header>
                    {{ child.name }}
                  </template>
                  <template #default>
                    <v-list-item v-for="(error, i) in child.errors" :key="i" dense class="error--text">
                      {{ error }}
                    </v-list-item>
                  </template>
                </expandable-content>
              </div>
            </v-alert>
          </div>
        </v-slide-x-reverse-transition>
        <v-slide-x-reverse-transition :hide-on-leave="true">
          <div v-show="!showError" v-if="selectedNode && selectedDate && !selectedNode.isConfiguration()">
            <v-alert
              v-if="selectedNodeHasChildren && !dismissRecursiveUnmountAlert"
              text
              type="info"
              dismissible
              @input="dismissRecursiveUnmountAlert = true"
            >
              Unmounting the selected node also unmounts every child node
            </v-alert>
            <div v-for="node in [selectedNode, ...allNestedChildrenList]" :key="node.id">
              <v-alert v-if="getUnmountActionEndDateOfNodeToOverwrite(node) != null" text type="info">
                The previously set unmount date of
                {{ node.nameWithoutOffsets }}
                ({{ dateToDateTimeString(getUnmountActionEndDateOfNodeToOverwrite(node)) }})
                will be overwritten.
              </v-alert>
            </div>
            <v-card>
              <v-card-title>
                {{ unmountTitle }}
              </v-card-title>
              <v-container>
                <ConfigurationsSelectedItemUnmountForm
                  v-if="selectedNode"
                  :node="selectedNode"
                  :contacts="contacts"
                  :current-user-mail="currentUserMail"
                  @unmount="unmount"
                />
              </v-container>
            </v-card>
          </div>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">

import { Component, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  UpdateDeviceMountActionAction,
  UpdatePlatformMountActionAction,
  ConfigurationsState,
  LoadMountingConfigurationForDateAction,
  SetSelectedDateAction,
  LoadConfigurationDynamicLocationActionsAction,
  LoadDeviceMountActionAction,
  LoadPlatformMountActionsAction
} from '@/store/configurations'

import { Contact } from '@/models/Contact'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'
import { dateToDateTimeString } from '@/utils/dateHelper'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExpandableContent from '@/components/shared/ExpandableContent.vue'
import { UnmountActionValidator } from '@/utils/UnmountActionValidator'

@Component({
  components: {
    ExpandableContent,
    BaseExpandableListItem,
    ConfigurationsSelectedItemUnmountForm,
    ConfigurationsTreeView,
    DateTimePicker
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', [
      'configuration',
      'configurationMountingActionsForDate',
      'deviceMountActionsIncludingDeviceInformation',
      'configurationPlatformMountActions',
      'selectedDate',
      'configurationDynamicLocationActions',
      'deviceMountAction']
    ),
    ...mapState('contacts', ['contacts']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('configurations', ['mountActionDateItems'])
  },
  methods: {
    dateToDateTimeString,
    ...mapActions('configurations', [
      'loadMountingConfigurationForDate',
      'updateDeviceMountAction',
      'updatePlatformMountAction',
      'setSelectedDate',
      'loadConfigurationDynamicLocationActions',
      'loadDeviceMountActionsIncludingDeviceInformation',
      'loadDeviceMountAction',
      'loadDeviceMountActions',
      'loadPlatformMountActions'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationUnMountPlatformsAndDevicesPage extends mixins(CheckEditAccess) {
  private selectedNode: ConfigurationsTreeNode | null = null
  private tree: ConfigurationsTree = ConfigurationsTree.fromArray([])

  // vuex definition for typescript check
  private configuration!: ConfigurationsState['configuration']
  private configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  private updateDeviceMountAction!: UpdateDeviceMountActionAction
  private updatePlatformMountAction!: UpdatePlatformMountActionAction
  private loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  private selectedDate!: ConfigurationsState['selectedDate']
  private setSelectedDate!: SetSelectedDateAction
  private configurationDynamicLocationActions!: ConfigurationsState['configurationDynamicLocationActions']
  private loadConfigurationDynamicLocationActions!: LoadConfigurationDynamicLocationActionsAction
  private loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionAction
  private loadPlatformMountActions!: LoadPlatformMountActionsAction
  private deviceMountActionsIncludingDeviceInformation!: DeviceMountAction[]
  private configurationPlatformMountActions!: PlatformMountAction[]

  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  private root: ConfigurationsTreeNode | null = null
  private validator: UnmountActionValidator | null = null
  private dismissRecursiveUnmountAlert = false

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/platforms-and-devices'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  async fetch () {
    await this.loadTreeAndActions()
  }

  async loadTreeAndActions () {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadConfigurationDynamicLocationActions(this.configurationId),
        this.loadTree(),
        this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId),
        this.loadPlatformMountActions(this.configurationId)
      ])
      await this.validateTree()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch resources')
    } finally {
      this.setLoading(false)
    }
  }

  async loadTree () {
    await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
    if (this.configuration) {
      // construct the configuration as the root node of the tree
      const rootMountAction = new ConfigurationMountAction(this.configuration)
      const rootNode = new ConfigurationNode(rootMountAction)
      // as we don't want to alter the Vuex state, we create a new Tree here
      if (this.configurationMountingActionsForDate) {
        rootNode.children = ConfigurationsTree.createFromObject(this.configurationMountingActionsForDate).toArray()
        rootNode.disabled = true
        this.root = rootNode
        this.tree = ConfigurationsTree.fromArray([rootNode])
      }
    }
  }

  validateTree (): void {
    if (!this.root || !this.selectedDate) {
      return
    }
    this.validator = new UnmountActionValidator(
      this.tree,
      this.selectedDate,
      this.deviceMountActionsIncludingDeviceInformation,
      this.configurationPlatformMountActions,
      this.configurationDynamicLocationActions
    )
    this.validator.validateTreeRecursively()
  }

  get selectedNodeHasChildren (): boolean {
    if (!this.selectedNode) {
      return false
    }
    return (this.selectedNode.canHaveChildren() && this.selectedNode.children.length > 0)
  }

  get allNestedChildrenList (): ConfigurationsTreeNode[] {
    if (!this.selectedNode || !this.selectedNodeHasChildren) {
      return []
    }
    return this.selectedNode.getTree().getAllNodesAsList()
  }

  get showError (): boolean {
    return !!this.selectedNode?.hasErrors || !!this.selectedNode?.hasChildErrors
  }

  getUnmountActionEndDateOfNodeToOverwrite (node: ConfigurationsTreeNode) {
    return this.validator?.getUnmountEndDateToOverwrite(node)
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  get unmountTitle (): string {
    return 'Unmount ' + [this.selectedNode, ...this.allNestedChildrenList].map(node => node?.nameWithoutOffsets).join(', ')
  }

  async unmount ({ contact, description }: { contact: Contact, description: string }) {
    if (!this.selectedNode || !this.selectedDate || !this.selectedNode) {
      return
    }
    try {
      this.setLoading(true)
      const node = this.selectedNode
      await this.unmountNodeRecursively({ node, contact, description })
      this.selectedNode = null
      // We need to update the selected date, so that we don't show the unmounted eleement anymore in
      // the tree. The easiest way is to just add one millisecond to the selected date.
      // This way, the unmounted device is no longer visible in the tree, and we can easily unmount
      // multiple devices or platforms before leaving the unmount mode.
      this.setSelectedDate(this.selectedDate.plus({ milliseconds: 1 }))
      await this.loadTreeAndActions()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to unmount node')
    } finally {
      this.setLoading(false)
    }
  }

  async unmountNodeRecursively ({ node, contact, description }: {
    node: ConfigurationsTreeNode,
    contact: Contact,
    description: string
  }) {
    for (const child of node.children) {
      await this.unmountNodeRecursively({ node: child, contact, description })
    }

    if (node.isDevice()) {
      await this.unmountDevice((node as DeviceNode).unpack(), contact, description)
    } else if (node.isPlatform()) {
      await this.unmountPlatform((node as PlatformNode).unpack(), contact, description)
    }
  }

  async unmountDevice (mountAction: DeviceMountAction, endContact: Contact, endDescription: string) {
    const mountActionWithEndDate = DeviceMountAction.createFromObject({
      id: mountAction.id,
      device: mountAction.device,
      parentPlatform: mountAction.parentPlatform,
      parentDevice: mountAction.parentDevice,
      offsetX: mountAction.offsetX,
      offsetY: mountAction.offsetX,
      offsetZ: mountAction.offsetX,
      epsgCode: mountAction.epsgCode,
      x: mountAction.x,
      y: mountAction.y,
      z: mountAction.z,
      elevationDatumName: mountAction.elevationDatumName,
      elevationDatumUri: mountAction.elevationDatumUri,
      beginDate: mountAction.beginDate,
      beginContact: mountAction.beginContact,
      beginDescription: mountAction.beginDescription,
      endDate: this.selectedDate,
      endContact,
      endDescription,
      label: mountAction.label
    })
    await this.updateDeviceMountAction({
      configurationId: this.configurationId,
      deviceMountAction: mountActionWithEndDate
    })
  }

  async unmountPlatform (mountAction: PlatformMountAction, endContact: Contact, endDescription: string) {
    const mountActionWithEndDate = PlatformMountAction.createFromObject({
      id: mountAction.id,
      platform: mountAction.platform,
      parentPlatform: mountAction.parentPlatform,
      offsetX: mountAction.offsetX,
      offsetY: mountAction.offsetX,
      offsetZ: mountAction.offsetX,
      epsgCode: mountAction.epsgCode,
      x: mountAction.x,
      y: mountAction.y,
      z: mountAction.z,
      elevationDatumName: mountAction.elevationDatumName,
      elevationDatumUri: mountAction.elevationDatumUri,
      beginDate: mountAction.beginDate,
      beginContact: mountAction.beginContact,
      beginDescription: mountAction.beginDescription,
      endDate: this.selectedDate,
      endContact,
      endDescription,
      label: mountAction.label
    })
    await this.updatePlatformMountAction({
      configurationId: this.configurationId,
      platformMountAction: mountActionWithEndDate
    })
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: DateTime, _oldValue: DateTime) {
    try {
      this.setLoading(true)
      this.selectedNode = null
      await this.loadTree()
      await this.validateTree()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

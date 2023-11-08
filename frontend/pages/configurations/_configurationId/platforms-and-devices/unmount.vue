<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
              @input="onNodeSelect"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-slide-x-reverse-transition>
          <div v-show="selectedNode && !selectedNode.isConfiguration()">
            <v-card>
              <v-card-title>
                Unmount {{ selectedNode ? selectedNode.nameWithoutOffsets : '' }}
              </v-card-title>
              <v-card-subtitle v-if="!nodeCanBeUnmounted" class="error--text">
                {{ errorMessage }}
              </v-card-subtitle>
              <v-container>
                <ConfigurationsSelectedItemUnmountForm
                  v-if="selectedNode"
                  :node="selectedNode"
                  :contacts="contacts"
                  :current-user-mail="currentUserMail"
                  :readonly="!nodeCanBeUnmounted"
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
  LoadMountingActionsAction
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

import { MountActionValidator } from '@/utils/MountActionValidator'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'

@Component({
  components: { ConfigurationsSelectedItemUnmountForm, ConfigurationsTreeView, DateTimePicker },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActionsForDate', 'selectedDate', 'configurationDynamicLocationActions', 'deviceMountAction']),
    ...mapState('contacts', ['contacts']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('configurations', ['mountActionDateItems'])
  },
  methods: {
    ...mapActions('configurations', [
      'loadMountingConfigurationForDate',
      'updateDeviceMountAction',
      'updatePlatformMountAction',
      'setSelectedDate',
      'loadConfigurationDynamicLocationActions',
      'loadDeviceMountAction',
      'loadMountingActions'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationUnMountPlatformsAndDevicesPage extends mixins(CheckEditAccess) {
  private selectedNode: ConfigurationsTreeNode | null = null
  private tree: ConfigurationsTree = ConfigurationsTree.fromArray([])

  private errorMessage: string = ''
  private nodeCanBeUnmounted: boolean = false

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
  private deviceMountAction!: ConfigurationsState['deviceMountAction']
  private loadDeviceMountAction!: LoadDeviceMountActionAction
  private loadMountingActions!: LoadMountingActionsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

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
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadConfigurationDynamicLocationActions(this.configurationId),
        this.loadMountingActions(this.configurationId),
        this.loadTree()
      ])
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
        this.tree = ConfigurationsTree.fromArray([rootNode])
      }
    }
  }

  async checkIfNodeCanBeUnmounted (node: ConfigurationsTreeNode): Promise<boolean> {
    if (node.isConfiguration()) {
      this.nodeCanBeUnmounted = false
      return false
    }
    if (node.isPlatform()) {
      if (node.canHaveChildren() && node.children.length > 0) {
        this.errorMessage = 'The selected platform still has mounted platforms or devices. Please unmount them first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      if (node.unpack().platform.archived) {
        this.errorMessage = 'The selected platform is archived. Please restore it first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      if (node.unpack().parentPlatform && node.unpack().parentPlatform?.archived) {
        this.errorMessage = 'The parent platform is archived. Please restore it first.'
        this.nodeCanBeUnmounted = false
        return false
      }
    }
    if (node.isDevice()) {
      if (node.canHaveChildren() && node.children.length > 0) {
        this.errorMessage = 'The selected device still has mounted sub devices. Please unmount them first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      if (node.unpack().device.archived) {
        this.errorMessage = 'The selected device is archived. Please restore it first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      if (node.unpack().parentPlatform && node.unpack().parentPlatform?.archived) {
        this.errorMessage = 'The parent platform is archived. Please restore it first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      if (node.unpack().parentDevice && node.unpack().parentDevice?.archived) {
        this.errorMessage = 'The parent device is archived. Please restore it first.'
        this.nodeCanBeUnmounted = false
        return false
      }
      // check device mount actions against dynamic location actions
      // load the full action (with device properties)
      await this.loadDeviceMountAction(node.unpack().id)
      if (this.deviceMountAction) {
        // get all dynamic location actions that use properties of the current device mount action
        const dynamicLocationActions = MountActionValidator.getRelatedDynamicLocationActions(this.deviceMountAction, this.configurationDynamicLocationActions)
        // create a new device mount action with the selected end date
        const newDeviceMountAction = DeviceMountAction.createFromObject(this.deviceMountAction)
        newDeviceMountAction.endDate = this.selectedDate
        const error = MountActionValidator.isDeviceMountActionCompatibleWithMultipleDynamicLocationActions(newDeviceMountAction, dynamicLocationActions)
        if (typeof error === 'object') {
          this.errorMessage = 'The selected device is still referenced by a dynamic location. Please stop it first.'
          this.nodeCanBeUnmounted = false
          return false
        }
      }
    }
    this.nodeCanBeUnmounted = true
    return true
  }

  onNodeSelect (node: ConfigurationsTreeNode | null) {
    if (!node) {
      return
    }
    this.checkIfNodeCanBeUnmounted(node)
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

  async unmount ({ contact, description }: {contact: Contact, description: string}) {
    if (!this.selectedNode || !this.selectedDate) {
      return
    }
    try {
      this.setLoading(true)
      if (this.selectedNode.isDevice()) {
        await this.unmountDevice((this.selectedNode as DeviceNode).unpack(), contact, description)
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      } else if (this.selectedNode.isPlatform()) {
        await this.unmountPlatform((this.selectedNode as PlatformNode).unpack(), contact, description)
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      }
      this.selectedNode = null
      // We need to update the selected date, so that we don't show the unmounted eleement anymore in
      // the tree. The easiest way is to just add one millisecond to the selected date.
      // This way, the unmounted device is no longer visible in the tree, and we can easily unmount
      // multiple devices or platforms before leaving the unmount mode.
      this.setSelectedDate(this.selectedDate.plus({ milliseconds: 1 }))
      await this.loadTree()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to unmount node')
    } finally {
      this.setLoading(false)
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
      beginDate: mountAction.beginDate,
      beginContact: mountAction.beginContact,
      beginDescription: mountAction.beginDescription,
      endDate: this.selectedDate,
      endContact,
      endDescription
    })
    await this.updateDeviceMountAction({ configurationId: this.configurationId, deviceMountAction: mountActionWithEndDate })
  }

  async unmountPlatform (mountAction: PlatformMountAction, endContact: Contact, endDescription: string) {
    // TODO: validate child nodes
    const mountActionWithEndDate = PlatformMountAction.createFromObject({
      id: mountAction.id,
      platform: mountAction.platform,
      parentPlatform: mountAction.parentPlatform,
      offsetX: mountAction.offsetX,
      offsetY: mountAction.offsetX,
      offsetZ: mountAction.offsetX,
      beginDate: mountAction.beginDate,
      beginContact: mountAction.beginContact,
      beginDescription: mountAction.beginDescription,
      endDate: this.selectedDate,
      endContact,
      endDescription
    })
    await this.updatePlatformMountAction({ configurationId: this.configurationId, platformMountAction: mountActionWithEndDate })
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: DateTime, _oldValue: DateTime) {
    try {
      this.setLoading(true)
      await this.loadTree()
      this.onNodeSelect(this.selectedNode)
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>

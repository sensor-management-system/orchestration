<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      v-if="mountInfoAvailable"
      flat
    >
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          :disabled="buttonsDisabled"
          save-btn-text="Apply"
          :to="platformsAndDevicesLink"
          @save="save"
        />
      </v-card-actions>
      <mount-action-edit-form
        ref="editForm"
        :value="deviceMountAction"
        :tree="tree"
        :contacts="contacts"
        :original-action="originalAction"
        @input="update"
        @select="selectNode"
      />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          :disabled="buttonsDisabled"
          save-btn-text="Apply"
          :to="platformsAndDevicesLink"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="mountActionHasChanged"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Watch, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import * as VueRouter from 'vue-router'

import {
  ConfigurationsState,
  LoadMountingConfigurationForDateAction,
  LoadDeviceMountActionAction,
  UpdateDeviceMountActionAction
} from '@/store/configurations'
import { ContactsState, LoadAllContactsAction } from '@/store/contacts'

import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Availability } from '@/models/Availability'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import MountActionEditForm from '@/components/configurations/MountActionEditForm.vue'

@Component({
  components: {
    NavigationGuardDialog,
    SaveAndCancelButtons,
    MountActionEditForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActionsForDate', 'selectedDate']),
    ...mapState('configurations', {
      originalAction: 'deviceMountAction'
    }),
    ...mapState('contacts', ['contacts'])
  },
  methods: {
    ...mapActions('configurations', ['loadMountingConfigurationForDate', 'loadDeviceMountAction', 'updateDeviceMountAction']),
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationEditDeviceMountActionsPage extends mixins(CheckEditAccess) {
  private configuration!: ConfigurationsState['configuration']
  private configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  private selectedDate!: ConfigurationsState['selectedDate']
  private loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  private loadDeviceMountAction!: LoadDeviceMountActionAction
  private updateDeviceMountAction!: UpdateDeviceMountActionAction
  private originalAction!: ConfigurationsState['deviceMountAction']

  private contacts!: ContactsState['contacts']
  private loadAllContacts!: LoadAllContactsAction

  private deviceMountAction: DeviceMountAction | null = null
  private showNavigationWarning: boolean = false
  private to: VueRouter.RawLocation | null = null
  private mountActionHasChanged = false

  private tree: ConfigurationsTree = new ConfigurationsTree()
  private formIsValid: boolean = true
  private beginDateErrorMessage: string = ''
  private endDateErrorMessage: string = ''
  private availabilities: Availability[] = []

  // vuex definition for typescript check
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
    await this.loadActionAndTree()
  }

  async loadActionAndTree (): Promise<void> {
    this.setLoading(true)
    try {
      await Promise.all([
        this.loadDeviceMountAction(this.mountActionId),
        this.loadAllContacts()
      ])
      if (!this.originalAction) {
        throw new Error('could not load mount action')
      }
      this.deviceMountAction = DeviceMountAction.createFromObject(this.originalAction)
      await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
      this.createTreeWithConfigAsRootNode()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of mount action failed')
    } finally {
      this.setLoading(false)
    }
  }

  createTreeWithConfigAsRootNode () {
    if (this.configuration && this.configurationMountingActionsForDate) {
      // construct the configuration as the root node of the tree
      const rootNode = new ConfigurationNode(new ConfigurationMountAction(this.configuration))
      rootNode.disabled = true
      rootNode.children = ConfigurationsTree.createFromObject(this.configurationMountingActionsForDate).toArray()
      this.tree = ConfigurationsTree.fromArray([rootNode])
      this.tree.getAllNodesAsList().forEach((i) => {
        // disable all but the selected node
        if (!i.isDevice() || i.unpack().id !== this.mountActionId) {
          i.disabled = true
        }
      })
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get mountActionId (): string {
    return this.$route.params.actionId
  }

  getMountActionId (): string {
    return this.$route.params.actionId
  }

  update (mountAction: DeviceMountAction) {
    this.mountActionHasChanged = true
    const newNode = new DeviceNode(mountAction)
    const oldNode = this.tree.getAllDeviceNodesAsList().find(i => i.unpack().id === mountAction.id)
    if (oldNode) {
      this.tree.replace(oldNode, newNode)
    }
    this.deviceMountAction = mountAction
    // validate the form again to get the information if it is valid
    this.$nextTick(() => {
      this.formIsValid = (this.$refs.editForm as MountActionEditForm).validateForm()
    })
  }

  async save () {
    if (!this.deviceMountAction) {
      return
    }
    if (!this.formIsValid) {
      return
    }
    this.setLoading(true)
    try {
      await this.updateDeviceMountAction({ configurationId: this.configurationId, deviceMountAction: this.deviceMountAction })
      this.mountActionHasChanged = false
      this.$router.push(this.platformsAndDevicesLink)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Saving of mount action failed')
    } finally {
      this.setLoading(false)
    }
  }

  get platformsAndDevicesLink (): VueRouter.RawLocation {
    const backLink: VueRouter.RawLocation = {
      path: '/configurations/' + this.configurationId + '/platforms-and-devices'
    }
    if (this.deviceMountAction) {
      backLink.query = {
        deviceMountAction: this.deviceMountAction.id
      }
    }
    return backLink
  }

  get mountInfoAvailable (): boolean {
    return !!(this.deviceMountAction && this.tree.length)
  }

  get buttonsDisabled (): boolean {
    return this.tree.length === 0 || !this.formIsValid
  }

  selectNode (node: ConfigurationsTreeNode | null) {
    if (!node) {
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
      return
    }
    const actionId = node.unpack().id
    this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices/' + (node.isDevice() ? 'device-mount-actions/' : 'platform-mount-actions/') + actionId + '/edit')
  }

  beforeRouteUpdate (to: VueRouter.RawLocation, _from: VueRouter.RawLocation, next: any) {
    if (this.mountActionHasChanged && this.editable) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }

  @Watch('$route')
  async onRouteChange (newRoute: VueRouter.Route, oldRoute: VueRouter.Route) {
    if (newRoute.params.actionId !== oldRoute.params.actionId) {
      await this.loadActionAndTree()
    }
  }
}
</script>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
        :value="platformMountAction"
        :tree="tree"
        :contacts="contacts"
        @input="update"
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
import { Component, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import { RawLocation } from 'vue-router'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  ConfigurationsState,
  LoadMountingConfigurationForDateAction,
  LoadPlatformMountActionAction,
  UpdatePlatformMountActionAction
} from '@/store/configurations'
import { ContactsState, LoadAllContactsAction } from '@/store/contacts'

import { PlatformMountAction } from '@/models/PlatformMountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { Availability } from '@/models/Availability'

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
    ...mapState('contacts', ['contacts'])
  },
  methods: {
    ...mapActions('configurations', ['loadMountingConfigurationForDate', 'loadPlatformMountAction', 'updatePlatformMountAction']),
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationEditPlatformMountActionsPage extends mixins(CheckEditAccess) {
  configuration!: ConfigurationsState['configuration']
  configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  selectedDate!: ConfigurationsState['selectedDate']
  loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  loadPlatformMountAction!: LoadPlatformMountActionAction
  updatePlatformMountAction!: UpdatePlatformMountActionAction
  setLoading!: SetLoadingAction

  contacts!: ContactsState['contacts']
  loadAllContacts!: LoadAllContactsAction

  private platformMountAction: PlatformMountAction | null = null
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private mountActionHasChanged = false

  private tree: ConfigurationsTree = new ConfigurationsTree()
  private formIsValid: boolean = false
  private beginDateErrorMessage: string = ''
  private endDateErrorMessage: string = ''
  private availabilities: Availability[] = []

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
    this.setLoading(true)
    try {
      await Promise.all([
        this.loadPlatformMountAction(this.mountActionId),
        this.loadAllContacts()
      ])
      const loadedPlatformMountAction = this.$store.state.configurations.platformMountAction
      if (!loadedPlatformMountAction) {
        throw new Error('could not load mount action')
      }
      this.platformMountAction = PlatformMountAction.createFromObject(loadedPlatformMountAction)
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
      rootNode.children = ConfigurationsTree.createFromObject(this.configurationMountingActionsForDate).toArray()
      this.tree = ConfigurationsTree.fromArray([rootNode])
      this.tree.getAllNodesAsList().forEach((i) => {
        // disable all but the selected node
        if (!i.isPlatform() || i.unpack().id !== this.mountActionId) {
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

  update (mountAction: PlatformMountAction) {
    this.mountActionHasChanged = true
    const newNode = new PlatformNode(mountAction)
    const oldNode = this.tree.getAllPlatformNodesAsList().find(i => i.unpack().id === mountAction.id)
    if (oldNode) {
      this.tree.replace(oldNode, newNode)
    }
    this.platformMountAction = mountAction
    // validate the form again to get the information if it is valid
    this.$nextTick(() => {
      this.formIsValid = (this.$refs.editForm as MountActionEditForm).validateForm()
    })
  }

  async save () {
    if (!this.platformMountAction) {
      return
    }
    if (!this.formIsValid) {
      return
    }
    this.setLoading(true)
    try {
      await this.updatePlatformMountAction({ configurationId: this.configurationId, platformMountAction: this.platformMountAction })
      this.mountActionHasChanged = false
      this.$router.push(this.platformsAndDevicesLink)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Saving of mount action failed')
    } finally {
      this.setLoading(false)
    }
  }

  get platformsAndDevicesLink (): RawLocation {
    const backLink: RawLocation = {
      path: '/configurations/' + this.configurationId + '/platforms-and-devices'
    }
    if (this.platformMountAction) {
      backLink.query = {
        platformMountAction: this.platformMountAction.id
      }
    }
    return backLink
  }

  get mountInfoAvailable (): boolean {
    return !!(this.platformMountAction && this.tree.length)
  }

  get buttonsDisabled (): boolean {
    return this.tree.length === 0 || !this.formIsValid
  }

  beforeRouteLeave (to: RawLocation, _from: RawLocation, next: any) {
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
}
</script>

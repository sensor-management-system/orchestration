<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
          v-model="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
        />
      </v-col>
      <v-col>
        <v-select
          v-model="selectedDate"
          :item-value="(x) => x.value"
          :item-text="(x) => x.text"
          :items="mountActionDateItems"
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          persistent-hint
        />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-container>
            <v-card-title>Mounted devices and platforms</v-card-title>
            <ConfigurationsTreeView
              v-if="configuration && tree"
              ref="unmountTreeView"
              v-model="selectedNode"
              :tree="tree"
            />
          </v-container>
        </v-card>
      </v-col>
      <v-col>
        <v-slide-x-reverse-transition>
          <div v-show="selectedNode && !selectedNode.isConfiguration()">
            <v-card>
              <v-card-title>Submit unmount form</v-card-title>
              <v-card-subtitle v-if="!nodeCanBeUnmounted(selectedNode)" class="error--text">
                The selected node still has active children. Please unmount them first.
              </v-card-subtitle>
              <v-container>
                <ConfigurationsSelectedItemUnmountForm
                  v-if="selectedNode"
                  :node="selectedNode"
                  :contacts="contacts"
                  :current-user-mail="currentUserMail"
                  :readonly="!nodeCanBeUnmounted(selectedNode)"
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
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import {
  UpdateDeviceMountActionAction,
  UpdatePlatformMountActionAction,
  ConfigurationsState,
  LoadMountingConfigurationForDateAction
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

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'

@Component({
  components: { ProgressIndicator, ConfigurationsSelectedItemUnmountForm, ConfigurationsTreeView, DateTimePicker },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActionsForDate']),
    ...mapState('contacts', ['contacts']),
    ...mapGetters('configurations', ['mountActionDateItems'])
  },
  methods: {
    ...mapActions('configurations', [
      'loadMountingConfigurationForDate',
      'updateDeviceMountAction',
      'updatePlatformMountAction'
    ])
  }
})
export default class ConfigurationUnMountPlatformsAndDevicesPage extends Vue {
  private selectedDate = DateTime.utc()
  private selectedNode: ConfigurationsTreeNode | null = null
  private tree: ConfigurationsTree = ConfigurationsTree.fromArray([])

  private isSaving = false
  private isLoading = false

  // vuex definition for typescript check
  configuration!: ConfigurationsState['configuration']
  configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  updateDeviceMountAction!: UpdateDeviceMountActionAction
  updatePlatformMountAction!: UpdatePlatformMountActionAction
  loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction

  async fetch () {
    try {
      this.isLoading = true
      await this.loadTree()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch resources')
    } finally {
      this.isLoading = false
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
        this.tree = ConfigurationsTree.fromArray([rootNode])
      }
    }
  }

  nodeCanBeUnmounted (node: ConfigurationsTreeNode | null): boolean {
    if (node === null) {
      return true
    }
    if (node.isConfiguration()) {
      return false
    }
    if (node.isPlatform() && node.canHaveChildren() && node.children.length > 0) {
      return false
    }
    return true
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
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
      this.isSaving = true
      if (this.selectedNode.isDevice()) {
        await this.unmountDevice((this.selectedNode as DeviceNode).unpack(), contact, description)
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      } else if (this.selectedNode.isPlatform()) {
        await this.unmountPlatform((this.selectedNode as PlatformNode).unpack(), contact, description)
        this.$store.commit('snackbar/setSuccess', 'Save successful')
      }
      this.selectedNode = null
      await this.loadTree()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to unmount node')
    } finally {
      this.isSaving = false
    }
  }

  async unmountDevice (mountAction: DeviceMountAction, endContact: Contact, endDescription: string) {
    const mountActionWithEndDate = DeviceMountAction.createFromObject({
      id: mountAction.id,
      device: mountAction.device,
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
      this.isLoading = true
      await this.loadTree()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>

<style scoped>

</style>

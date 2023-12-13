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
    <v-alert text type="info" dismissible>
      Here you can see the setup of platforms and devices mounted for the configuration at a specific point in time. Feel free to select a different day to see the setup on that specific date, showing historical or future mounts.
      The selection will also be used as default entry for the mount and un-mount dialogs.
    </v-alert>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/platforms-and-devices/mount'"
      >
        Mount Platform or Device
      </v-btn>
      <v-btn
        v-if="editable"
        color="secondary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/platforms-and-devices/unmount'"
      >
        -Un-mount Platform or Device
      </v-btn>
    </v-card-actions>
    <v-row>
      <v-col cols="12" md="3">
        <DateTimePicker
          :value="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          hint=""
          @input="setSelectedDate"
        />
      </v-col>
      <v-col>
        <v-select
          :value="selectedDate"
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
              ref="treeView"
              v-model="selectedNode"
              :tree="tree"
              show-detailed-name
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <div class="sticky">
          <v-slide-x-reverse-transition>
            <v-card v-if="selectedNode">
              <configurations-tree-title :selected-node="selectedNode" />
              <v-card-text>
                <ConfigurationsTreeNodeDetail
                  v-if="selectedNode"
                  :node="selectedNode"
                  :editable="editable"
                  :deletable="isSelectedNodeDeletable"
                  @delete="isDeleteDialogShown = true"
                />
                <delete-dialog
                  v-if="selectedNode"
                  v-model="isDeleteDialogShown"
                  title="Delete the Mount Action?"
                  :disabled="isLoading"
                  @cancel="isDeleteDialogShown = false"
                  @delete="deleteSelectedNode"
                >
                  <em>Please only delete mounts if you are sure that the {{ selectedNodeType }} is <strong> not being used effectively</strong> and <strong>no other software</strong> is referencing the mounted {{ selectedNodeType }}.</em>
                </delete-dialog>
              </v-card-text>
            </v-card>
          </v-slide-x-reverse-transition>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, InjectReactive, ProvideReactive } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import {
  LoadMountingActionsAction,
  LoadMountingConfigurationForDateAction,
  SetSelectedDateAction,
  ConfigurationsState,
  DeleteDeviceMountActionAction,
  DeletePlatformMountActionAction,
  LoadConfigurationDynamicLocationActionsAction
} from '@/store/configurations'

import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'

import { MountActionValidator } from '@/utils/MountActionValidator'
import { IOffsets } from '@/utils/configurationInterfaces'
import { sumOffsets } from '@/utils/configurationsTreeHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsTreeNodeDetail from '@/components/configurations/ConfigurationsTreeNodeDetail.vue'
import ConfigurationsTreeTitle from '@/components/configurations/ConfigurationsTreeTitle.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'

@Component({
  components: {
    ConfigurationsTreeNodeDetail,
    ConfigurationsTreeTitle,
    ConfigurationsTreeView,
    DateTimePicker,
    DeleteDialog
  },
  computed: {
    ...mapState('configurations', [
      'selectedDate',
      'configuration',
      'configurationMountingActions',
      'configurationMountingActionsForDate',
      'configurationDynamicLocationActions'
    ]),
    ...mapGetters('configurations', ['mountActionDateItems']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', [
      'setSelectedDate',
      'loadMountingActions',
      'loadMountingConfigurationForDate',
      'deleteDeviceMountAction',
      'deletePlatformMountAction',
      'loadConfigurationDynamicLocationActions'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationShowPlatformsAndDevicesPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private selectedNode: ConfigurationsTreeNode | null = null
  private tree: ConfigurationsTree = new ConfigurationsTree()

  private isDeleteDialogShown: boolean = false

  @ProvideReactive()
    calculatedOffsets: IOffsets | null = null

  // vuex definition for typescript check
  private configuration!: ConfigurationsState['configuration']
  private loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  private loadMountingActions!: LoadMountingActionsAction
  private configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  private configurationMountingActions!: ConfigurationsState['configurationMountingActions']
  private selectedDate!: ConfigurationsState['selectedDate']
  private setSelectedDate!: SetSelectedDateAction
  private deleteDeviceMountAction!: DeleteDeviceMountActionAction
  private deletePlatformMountAction!: DeletePlatformMountActionAction
  private configurationDynamicLocationActions!: ConfigurationsState['configurationDynamicLocationActions']
  private loadConfigurationDynamicLocationActions!: LoadConfigurationDynamicLocationActionsAction
  setLoading!: SetLoadingAction

  created () {
    if (this.$route.query.date) {
      this.setSelectedDate(DateTime.fromISO(this.$route.query.date.toString(), { zone: 'utc' }))
    }
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadMountingActions(this.configurationId),
        this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate }),
        this.loadConfigurationDynamicLocationActions(this.configurationId)
      ])
      this.createTreeWithConfigAsRootNode()
      this.setSelectedNodeFromUrlParam()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.setLoading(false)
    }
  }

  createTreeWithConfigAsRootNode () {
    if (this.configuration && this.configurationMountingActionsForDate) {
      // construct the configuration as the root node of the tree
      const rootNode = new ConfigurationNode(new ConfigurationMountAction(this.configuration))
      rootNode.children = this.configurationMountingActionsForDate.toArray()
      this.tree = ConfigurationsTree.fromArray([rootNode])
    }
  }

  setSelectedNodeFromUrlParam () {
    if (this.$route.query.deviceMountAction) {
      const selected = this.tree.getAllDeviceNodesAsList().find(i => i.unpack().id === this.$route.query.deviceMountAction)
      if (selected) {
        this.selectedNode = selected
      }
    }
    if (this.$route.query.platformMountAction) {
      const selected = this.tree.getAllPlatformNodesAsList().find(i => i.unpack().id === this.$route.query.platformMountAction)
      if (selected) {
        this.selectedNode = selected
      }
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isSelectedNodeDeletable (): boolean {
    if (!this.selectedNode) {
      return false
    }
    if (this.selectedNode.canHaveChildren() && this.selectedNode.children.length) {
      return false
    }
    const action = this.selectedNode.unpack()
    // check if dynamic location actions exist that use the device's properties
    if ('isDeviceMountAction' in action && action.isDeviceMountAction()) {
      if (this.getRelatedDynamicLocationActions().length) {
        return false
      }
    }
    return true
  }

  async deleteSelectedNode (): Promise<void> {
    if (!this.selectedNode) {
      return
    }
    const action = this.selectedNode.unpack()
    this.setLoading(true)
    try {
      if ('isDeviceMountAction' in action && action.isDeviceMountAction()) {
        await this.deleteDeviceMountAction(action.id)
      }
      if ('isPlatformMountAction' in action && action.isPlatformMountAction()) {
        await this.deletePlatformMountAction(action.id)
      }
      this.$store.commit('snackbar/setSuccess', 'Mount Action deleted.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Mount Action could not be deleted.')
    } finally {
      this.setLoading(false)
      this.selectedNode = null
      this.isDeleteDialogShown = false
      this.$router.replace({
        query: {}
      })
      this.$fetch()
    }
  }

  getRelatedDynamicLocationActions (): DynamicLocationAction[] {
    if (!this.selectedNode) {
      return []
    }
    const action = this.selectedNode.unpack()
    if (!('isDeviceMountAction' in action) || !action.isDeviceMountAction()) {
      return []
    }
    // filter all dynamic location actions, that are within the original time range
    return MountActionValidator.getRelatedDynamicLocationActions(action, this.configurationDynamicLocationActions)
  }

  get selectedNodeType (): string {
    if (!this.selectedNode) {
      return ''
    }
    const action = this.selectedNode.unpack()
    if ('isDeviceMountAction' in action && action.isDeviceMountAction()) {
      return 'device'
    }
    if ('isPlatformMountAction' in action && action.isPlatformMountAction()) {
      return 'platform'
    }
    return ''
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: DateTime, _oldValue: DateTime) {
    try {
      this.setLoading(true)
      await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
      this.createTreeWithConfigAsRootNode()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('selectedNode')
  onSelectedNodeChanged (value: ConfigurationsTreeNode | null) {
    if (value === null) {
      this.calculatedOffsets = null
      return
    }
    if (value.isConfiguration()) {
      return
    }
    const parents = this.tree.getParents(value)
    this.calculatedOffsets = sumOffsets([...parents, value])
  }
}
</script>
<style scoped>
.sticky {
  position: sticky;
  top: 112px;
}
</style>

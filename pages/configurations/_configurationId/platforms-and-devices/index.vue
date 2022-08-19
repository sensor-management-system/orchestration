<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
      v-model="isLoading"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/platforms-and-devices/mount'"
      >
        Mount Platform or Device
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
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
          v-model="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          hint=""
        />
      </v-col>
      <v-col>
        <v-select
          v-model="selectedDate"
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
          <v-card-title class="primary white--text">
            Mounted devices and platforms
          </v-card-title>
          <v-card-text>
            <ConfigurationsTreeView
              v-if="configuration && tree"
              ref="treeView"
              v-model="selectedNode"
              :tree="tree"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-slide-x-reverse-transition>
          <v-card v-if="selectedNode">
            <configurations-tree-title :selected-node="selectedNode" />
            <v-card-text>
              <ConfigurationsTreeNodeDetail
                v-if="selectedNode"
                :node="selectedNode"
              />
            </v-card-text>
          </v-card>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { LoadMountingActionsAction, LoadMountingConfigurationForDateAction, ConfigurationsState } from '@/store/configurations'

import { ConfigurationMountingAction } from '@/models/ConfigurationMountingAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsTreeNodeDetail from '@/components/configurations/ConfigurationsTreeNodeDetail.vue'
import ConfigurationsTreeTitle from '@/components/configurations/ConfigurationsTreeTitle.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ConfigurationsTreeNodeDetail, ConfigurationsTreeTitle, ConfigurationsTreeView, DateTimePicker, ProgressIndicator },
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActions', 'configurationMountingActionsForDate']),
    ...mapGetters('configurations', ['mountActionDateItems'])
  },
  methods: mapActions('configurations', ['loadMountingActions', 'loadMountingConfigurationForDate'])
})
export default class ConfigurationShowPlatformsAndDevicesPage extends Vue {
  private selectedNode: ConfigurationsTreeNode | null = null
  private selectedDate: DateTime = DateTime.utc()
  private tree: ConfigurationsTree = ConfigurationsTree.fromArray([])

  private isLoading: boolean = false

  // vuex definition for typescript check
  configuration!: ConfigurationsState['configuration']
  loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  loadMountingActions!: LoadMountingActionsAction
  configurationMountingActionsForDate!: ConfigurationsTree
  configurationMountingActions!: ConfigurationMountingAction[]

  async created () {
    try {
      this.isLoading = true
      await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
      this.createTreeWithConfigAsRootNode()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.isLoading = false
    }
  }

  createTreeWithConfigAsRootNode () {
    if (this.configuration) {
      // construct the configuration as the root node of the tree
      const rootNode = new ConfigurationNode(this.configuration)
      rootNode.children = this.configurationMountingActionsForDate.toArray()
      this.tree = ConfigurationsTree.fromArray([rootNode])
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: DateTime, _oldValue: DateTime) {
    try {
      this.isLoading = true
      await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
      this.createTreeWithConfigAsRootNode()
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

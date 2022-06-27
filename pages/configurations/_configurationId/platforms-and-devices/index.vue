<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
        />
      </v-col>
      <v-col>
        <v-select
          v-model="selectedDate"
          :item-value="(x) => x.timepoint"
          :item-text="(x) => x.label"
          :items="configurationMountingActions"
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
            <v-treeview
              :items="tree"
              :active.sync="selectListSingelton"
              item-key="action.id"
              item-text="entity.attributes.short_name"
              activatable
              hoverable
              rounded
              return-object
            >
              <template #label="{item}">
                <div v-if="item.action.type==='device_mount_action'">
                  Mount - {{ item.entity.attributes.short_name }}
                </div>
                <div v-if="item.action.type==='platform_mount_action'">
                  Mount - {{ item.entity.attributes.short_name }}
                </div>
                <div
                  v-if="item.action.type==='device_unmount_action'"
                  style="text-decoration: line-through"
                >
                  UnMount - {{ item.entity.attributes.short_name }}
                </div>
                <div
                  v-if="item.action.type==='platform_unmount_action'"
                  style="text-decoration: line-through"
                >
                  UnMount - {{ item.entity.attributes.short_name }}
                </div>
              </template>
              <template #prepend="{ item }">
                <v-icon v-if="item.entity.type==='platform'">
                  mdi-rocket-outline
                </v-icon>
                <v-icon v-else>
                  mdi-network-outline
                </v-icon>
              </template>
            </v-treeview>
            <!--            <ConfigurationsTreeView-->
            <!--              v-if="configuration"-->
            <!--              ref="treeView"-->
            <!--              v-model="selectedNode"-->
            <!--              :items="tree"-->
            <!--            />-->
          </v-container>
        </v-card>
      </v-col>
      <v-col>
        <v-slide-x-reverse-transition>
          <div v-show="selectedNode">
            <v-card-title>Selected node information</v-card-title>
            <pre>
              {{ selectedNode }}
            </pre>
            <!--            <ConfigurationsTreeNodeDetail-->
            <!--              v-if="selectedNode"-->
            <!--              :node="selectedNode"-->
            <!--            />-->
          </div>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { Configuration } from '@/models/Configuration'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsTreeNodeDetail from '@/components/configurations/ConfigurationsTreeNodeDetail.vue'

@Component({
  components: { ConfigurationsTreeNodeDetail, ConfigurationsTreeView, DateTimePicker },
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActions'])
  },
  methods: mapActions('configurations', ['getMountingConfigurationForDate'])
})
export default class ConfigurationShowPlatformsAndDevicesPage extends Vue {
  // private selectedNode: ConfigurationsTreeNode | null = null
  private selectedDate = DateTime.utc()
  private selectListSingelton = []
  private tree = []
  // vuex definition for typescript check
  configuration!: Configuration
  getMountingConfigurationForDate!: (id: string, timepoint: DateTime) => []

  async created () {
    this.tree = await this.getMountingConfigurationForDate(this.configurationId, this.selectedDate)
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get selectedNode () {
    return this.selectListSingelton[0] ?? null
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: string, _oldValue: string) {
    this.tree = await this.getMountingConfigurationForDate(this.configurationId, this.selectedDate)
  }
  // get tree () {
  //
  //   // const selectedNodeId = this.selectedNode?.id
  //   // const tree = buildConfigurationTree(this.configuration, this.selectedDate)
  //   // if (selectedNodeId) {
  //   //   const node = tree.getById(selectedNodeId)
  //   //   if (node) {
  //   //     this.selectedNode = node
  //   //   }
  //   // }
  //   // return tree.toArray()
  // }
}
</script>

<style scoped>

</style>

<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row justify="center">
      <v-col class="mx-8">
        <v-alert
          border="top"
          colored-border
          type="info"
          elevation="2"
          class="my-4"
        >
          <div>
            Select a platform node (
            <v-icon>mdi-rocket-outline</v-icon>
            ) to add a device or platform to it.
          </div>
          <div>
            To add a device or platform directly to a configuration select the root node.
          </div>
          <div>
            You can deselect by clicking on a selected node.
          </div>
          <div>
            You can't attach a platform to a mounted device (
            <v-icon>mdi-network-outline</v-icon>
            ).
          </div>
        </v-alert>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12">
        <configurations-tree-view
          ref="treeViewStepper"
          v-model="syncedSelectedNode"
          show-detailed-names
          :tree="tree"
          @input="checkEndDateOfDatePicker"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, PropSync } from 'nuxt-property-decorator'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'

@Component({
  components: {
    ConfigurationsTreeView
  }
})
export default class MountWizardNodeSelect extends Vue {
  @PropSync('selectedNode', {
    required: false,
    type: Object
  })
    syncedSelectedNode!: ConfigurationsTreeNode | null

  @Prop({
    required: true,
    type: Object
  }) readonly tree!: ConfigurationsTreeNode[]

  // TODO: fix this validation --> STILL a problem?
  // the form field that needs to be validated is in MountWizardDateSelect (endDate)
  // because we need the end date of the selected node for validation,
  // we have to trigger the date input's validate function from here, whenever the selected node changes
  // but how?
  async checkEndDateOfDatePicker () {
    await this.$nextTick()
    return true
    // return (this.$refs.form as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style scoped>
</style>

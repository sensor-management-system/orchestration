<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-title v-if="selectedNode.isPlatform()">
      <v-icon
        left
      >
        mdi-rocket
      </v-icon>
      {{ selectedNode.node.platform.shortName }}
    </v-card-title>
    <v-card-title v-else-if="selectedNode.isDevice()">
      <v-icon
        left
      >
        mdi-network
      </v-icon>
      {{ selectedNode.node.device.shortName }}
    </v-card-title>
    <v-card-title v-else-if="selectedNode.isConfiguration()">
      <v-icon
        left
      >
        mdi-file-cog
      </v-icon>
      {{ selectedNode.node.configuration.label }}
    </v-card-title>
    <v-card-subtitle
      v-if="selectedNode.isConfiguration()"
      class="pb-0"
    >
      Configuration root
    </v-card-subtitle>
    <v-card-subtitle
      v-else
      class="pb-0"
    >
      Selected node information
    </v-card-subtitle>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

@Component
export default class ConfigurationsTreeTitle extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private selectedNode!: ConfigurationsTreeNode
}
</script>

<style scoped>

</style>

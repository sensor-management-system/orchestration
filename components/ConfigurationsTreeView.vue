<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
    <v-treeview
      :active.sync="selectedNodeSingletonList"
      :items="items"
      activatable
      hoverable
      rounded
      open-all
    >
      <template v-slot:prepend="{ item }">
        <v-icon v-if="item.isPlatform()">
          mdi-rocket-outline
        </v-icon>
        <v-icon v-else>
          mdi-network-outline
        </v-icon>
      </template>
    </v-treeview>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select platforms and devices for a configuration
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'

/**
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsTreeView extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: ConfigurationsTree

  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly selected: ConfigurationsTreeNode | null

  get items (): ConfigurationsTreeNode[] {
    return this.value.toArray()
  }

  get selectedNodeSingletonList (): string[] {
    if (!this.selected || !this.selected.id) {
      return []
    }
    return [this.selected.id]
  }

  set selectedNodeSingletonList (nodeIds: string[]) {
    let node: ConfigurationsTreeNode | null = null
    if (nodeIds.length) {
      node = this.value.getById(nodeIds[0])
    }
    this.$emit('select', node)
  }
}
</script>

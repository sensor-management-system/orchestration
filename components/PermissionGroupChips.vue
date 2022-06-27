<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
  <div
    class="permission-group-chips"
  >
    <span
      v-for="group in shortenedGroups"
      :key="group.id"
    >
      <v-tooltip
        top
        :disabled="group.id !== 'fakeID'"
        open-on-click
      >
        <template #activator="{ on, attrs }">
          <v-chip
            small
            class="mr-1 mb-1"
            v-bind="attrs"
            v-on="on"
          >
            {{ group.name }}
          </v-chip>
        </template>
        <p v-for="(groupName, index) in hiddenGroupNames" :key="index" class="mb-0">{{ groupName }}</p>
      </v-tooltip>
    </span>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { IPermissionGroup, PermissionGroup } from '@/models/PermissionGroup'

@Component
export default class PermissionGroupChips extends Vue {
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly value!: IPermissionGroup[]

  @Prop({
    default: () => false,
    required: false,
    type: Boolean
  })
  readonly collapsible!: Boolean

  get shortenedGroups (): IPermissionGroup[] {
    let shortenedGroups: IPermissionGroup[] = []

    if (this.collapsible && this.value.length > 3) {
      const emptyGroup: PermissionGroup = new PermissionGroup()
      emptyGroup.id = 'fakeID'
      emptyGroup.name = `and ${this.value.length - 2} more…`
      shortenedGroups = [
        this.value[0],
        this.value[1],
        emptyGroup
      ]
    } else {
      shortenedGroups = this.value
    }
    return shortenedGroups
  }

  get hiddenGroupNames (): string[] {
    const groups = this.value
    if (groups.length > 2) {
      return groups.slice(2).map(group => group.name)
    } else {
      return []
    }
  }
}
</script>

<style scoped lang="scss">
.permission-group-chips {
  display: inline-block;
}
</style>

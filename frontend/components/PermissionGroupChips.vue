<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
            <span v-if="$vuetify.breakpoint.smAndUp">{{ group.name | shortenRight(50) }}</span>
            <span v-else>{{ group.name | shortenRight(14) }}</span>
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
import { shortenRight } from '@/utils/stringHelpers'

@Component({
  filters: { shortenRight }
})
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

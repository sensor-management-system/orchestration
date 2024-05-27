<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <tr>
    <td>{{ entityName }}</td>
    <td>{{ entity.name | orDefault }}</td>
    <td>{{ entity.description | orDefault }}</td>
    <td v-if="JSON.stringify(entity.properties) !== '{}'">
      <v-textarea
        :value="JSON.stringify(entity.properties)"
        :rows="3"
        disabled
      />
    </td>
    <td v-else>
      —
    </td>
  </tr>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { TsmdlEntity } from '@/models/TsmdlEntity'

@Component({})
export default class TsmLinkingBasicDataTableEntry extends Vue {
  @Prop({
    required: true
  })
  readonly entityName!: string

  @Prop({
    required: true
  })
  readonly entity!: TsmdlEntity
}
</script>

<style>

</style>

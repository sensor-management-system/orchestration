<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <tr>
    <td>{{ entityName }}</td>

    <td v-if="entity.staLink">
      <v-btn title="Open STA Endpoint" icon :href="entity.staLink" target="_blank">
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </td>
    <td v-else-if="isLoading">
      <v-progress-circular indeterminate />
    </td>
    <td v-else-if="missingStaLinkHint">
      <v-tooltip
        right
      >
        <template #activator="{ on, attrs }">
          <v-icon
            v-bind="attrs"
            v-on="on"
          >
            mdi-link-off
          </v-icon>
        </template>
        {{ missingStaLinkHint }}
      </v-tooltip>
    </td>

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

  @Prop({
    required: false,
    default: false
  })
  readonly isLoading!: boolean

  @Prop({
    required: false
  })
  readonly missingStaLinkHint!: string
}
</script>

<style>

</style>

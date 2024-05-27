<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-divider class="my-1" />
    <v-row
      dense
    >
      <v-col class="text-subtitle-1 font-weight-medium">
        Mount information
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col>
        <slot name="mount" />
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row
      dense
    >
      <v-col class="text-subtitle-1 font-weight-medium">
        Platform information
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Type:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ platform.platformTypeName | orDefault }}
      </v-col>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Manufacturer:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ platform.manufacturerName | orDefault }}
      </v-col>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Model:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ platform.model | orDefault }}
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Serial number:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ platform.serialNumber | orDefault }}
      </v-col>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Inventory number:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ platform.inventoryNumber | orDefault }}
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Description:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
        :title="platform.description.length > 25 ? platform.description : ''"
      >
        {{ platform.description | shortenRight(25, '...') | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          :href="'platforms/' + platform.id"
          target="_blank"
          :disabled="false"
          small
        >
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
          Open in new tab
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'

@Component
export default class PlatformMountListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private platform!: Platform

  private show = false
  private showOverview = false
  private showMount = false
}
</script>

<style scoped>

</style>

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
        Device information
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
        {{ device.deviceTypeName | orDefault }}
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
        {{ device.manufacturerName | orDefault }}
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
        {{ device.model | orDefault }}
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
        {{ device.serialNumber | orDefault }}
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
        {{ device.inventoryNumber | orDefault }}
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
        :title="device.description.length > 25 ? device.description : ''"
      >
        {{ device.description| shortenRight(25, '...') | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          :href="'devices/' + device.id"
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

import { Device } from '@/models/Device'

@Component
export default class DevicesMountListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private device!: Device

  private show = false
  private showOverview = false
  private showMount = false
}
</script>

<style scoped>

</style>

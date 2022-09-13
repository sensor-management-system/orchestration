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

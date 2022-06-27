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
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
    <template #header>
      <div :class="'mr-1 text-caption' + (getType() === NO_TYPE ? ' text--disabled' : '')">
        {{ getType() }}
      </div>
      <status-chip
        :value="getStatus()"
      />
      <visibility-chip
        v-model="device.visibility"
      />
      <permission-group-chips
        v-model="device.permissionGroups"
        collapsible
      />
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <v-btn
        :to="'/devices/' + device.id"
        color="primary"
        text
        small
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #default>
      <span>{{ device.shortName }}</span>
      <v-tooltip v-if="$vuetify.breakpoint.smAndUp" bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="device.manufacturerName !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ device.manufacturerName }}</span>
        </template>
        <span>Manufacturer</span>
      </v-tooltip>
      <v-tooltip v-if="$vuetify.breakpoint.smAndUp" bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="device.model !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ device.model }}</span>
        </template>
        <span>Model number</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <span
            v-if="device.serialNumber !== ''"
            v-bind="attrs"
            class="text--disabled"
            v-on="on"
          >- {{ device.serialNumber }}</span>
        </template>
        <span>Serial number</span>
      </v-tooltip>
    </template>
    <template #expandable>
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Manufacturer:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ getTextOrDefault(device.manufacturerName) }}
        </v-col>
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Model:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ getTextOrDefault(device.model) }}
        </v-col>
      </v-row>
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Serial number:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ getTextOrDefault(device.serialNumber) }}
        </v-col>
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Inventory number:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
          class="nowrap-truncate"
        >
          {{ getTextOrDefault(device.inventoryNumber) }}
        </v-col>
      </v-row>
      <v-row
        no-gutters
      >
        <v-col
          cols="4"
          xs="4"
          sm="3"
          md="2"
          lg="2"
          xl="1"
          class="font-weight-medium"
        >
          Description:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="10"
          lg="10"
          xl="11"
          class="nowrap-truncate"
        >
          {{ getTextOrDefault(device.description) }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'

import { Device } from '@/models/Device'
import { Status } from '@/models/Status'
import { DeviceType } from '@/models/DeviceType'

import StatusChip from '@/components/shared/StatusChip.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'

@Component({
  components: {
    StatusChip,
    VisibilityChip,
    PermissionGroupChips,
    BaseExpandableListItem
  },
  computed: mapGetters('vocabulary', ['getDeviceTypeByUri', 'getEquipmentstatusByUri'])
})
export default class DevicesListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private device!: Device

  public readonly NO_TYPE: string = 'Unknown type'

  // vuex definition for typescript check
  getDeviceTypeByUri!: (uri: string) => DeviceType | undefined
  getEquipmentstatusByUri!: (uri: string) => Status | undefined

  getTextOrDefault = (text: string): string => text || '-'

  getType () {
    if (this.device.deviceTypeName) {
      return this.device.deviceTypeName
    }

    if (this.getDeviceTypeByUri(this.device.deviceTypeUri)) {
      const deviceType: DeviceType | undefined = this.getDeviceTypeByUri(this.device.deviceTypeUri)
      return deviceType!.name
    }
    return this.NO_TYPE
  }

  getStatus () {
    if (this.device.statusName) {
      return this.device.statusName
    }
    if (this.getEquipmentstatusByUri(this.device.statusUri)) {
      const deviceStatus: Status|undefined = this.getEquipmentstatusByUri(this.device.statusUri)
      return deviceStatus!.name
    }
    return ''
  }
}
</script>

<style scoped>

</style>

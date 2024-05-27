<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item
    :expandable-color="device.archived ? 'brown lighten-3' : 'grey lighten-5'"
    :background-color="device.archived ? 'brown lighten-4 ' : 'white'"
  >
    <template v-if="!hideHeader" #header>
      <div class="d-flex flex-wrap">
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
      </div>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <v-btn
        v-if="target=='_blank'"
        small
        @click.stop.prevent="openLink"
      >
        <v-icon
          small
        >
          mdi-open-in-new
        </v-icon>
        Open in new tab
      </v-btn>
      <v-btn
        v-else
        :to="detailLink"
        color="primary"
        text
        small
        @click.stop.prevent
      >
        View
      </v-btn>
    </template>
    <template #default>
      <slot name="additional-actions" />
      <v-tooltip v-if="device.archived" right>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on">
            mdi-archive-lock
          </v-icon>
        </template>
        <span>Archived</span>
      </v-tooltip>
      <slot name="title">
        <extended-item-name
          :value="device"
        />
      </slot>
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
          Persistent Identifier:
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
          <pid-tooltip :value="device.persistentIdentifier" />
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
          {{ device.manufacturerName | orDefault }}
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
          {{ device.model | orDefault }}
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
          {{ device.serialNumber | orDefault }}
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
          {{ device.inventoryNumber | orDefault }}
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
          {{ device.description | orDefault }}
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

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import StatusChip from '@/components/shared/StatusChip.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'

@Component({
  components: {
    BaseExpandableListItem,
    ExtendedItemName,
    PermissionGroupChips,
    PidTooltip,
    StatusChip,
    VisibilityChip
  },
  computed: mapGetters('vocabulary', ['getDeviceTypeByUri', 'getEquipmentstatusByUri'])
})
export default class DevicesListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private device!: Device

  @Prop({
    type: Boolean,
    default: false
  })
  private hideHeader!: boolean

  @Prop({
    default: '_self',
    type: String
  })
  private target!: string

  @Prop({
    default: '',
    type: String
  })
  private from!: string

  public readonly NO_TYPE: string = 'Unknown type'

  // vuex definition for typescript check
  getDeviceTypeByUri!: (uri: string) => DeviceType | undefined
  getEquipmentstatusByUri!: (uri: string) => Status | undefined

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

  get detailLink (): string {
    let params = ''
    if (this.from) {
      params = '?' + (new URLSearchParams({ from: this.from })).toString()
    }
    return `/devices/${this.device.id}${params}`
  }

  openLink () {
    if (this.target === '_self') {
      this.$router.push(this.detailLink)
    } else {
      window.open(this.$router.resolve(this.detailLink).href, this.target)
    }
  }
}
</script>

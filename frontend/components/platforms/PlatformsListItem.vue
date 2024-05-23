<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2024
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
    :expandable-color="platform.archived ? 'brown lighten-3' : 'grey lighten-5'"
    :background-color="platform.archived ? 'brown lighten-4 ' : 'white'"
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
          v-model="platform.visibility"
        />
        <permission-group-chips
          v-model="platform.permissionGroups"
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
      <v-tooltip v-if="platform.archived" right>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on">
            mdi-archive-lock
          </v-icon>
        </template>
        <span>Archived</span>
      </v-tooltip>
      <slot name="title">
        <extended-item-name
          :value="platform"
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
          <pid-tooltip :value="platform.persistentIdentifier" />
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
          {{ platform.manufacturerName | orDefault }}
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
          {{ platform.model | orDefault }}
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
          {{ platform.serialNumber | orDefault }}
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
          {{ platform.inventoryNumber | orDefault }}
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
          {{ platform.description | orDefault }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'

import { GetPlatformTypeByUriGetter, GetEquipmentstatusByUriGetter } from '@/store/vocabulary'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

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
  computed: mapGetters('vocabulary', ['getPlatformTypeByUri', 'getEquipmentstatusByUri'])
})
export default class PlatformsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private platform!: Platform

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
  getPlatformTypeByUri!: GetPlatformTypeByUriGetter
  getEquipmentstatusByUri!: GetEquipmentstatusByUriGetter

  getType () {
    if (this.platform.platformTypeName) {
      return this.platform.platformTypeName
    }

    if (this.getPlatformTypeByUri(this.platform.platformTypeUri)) {
      const platformType: PlatformType|undefined = this.getPlatformTypeByUri(this.platform.platformTypeUri)
      return platformType!.name
    }
    return this.NO_TYPE
  }

  getStatus () {
    if (this.platform.statusName) {
      return this.platform.statusName
    }
    if (this.getEquipmentstatusByUri(this.platform.statusUri)) {
      const platformStatus: Status|undefined = this.getEquipmentstatusByUri(this.platform.statusUri)
      return platformStatus!.name
    }
    return ''
  }

  get detailLink (): string {
    let params = ''
    if (this.from) {
      params = '?' + (new URLSearchParams({ from: this.from })).toString()
    }
    return `/platforms/${this.platform.id}${params}`
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

<style scoped>

</style>

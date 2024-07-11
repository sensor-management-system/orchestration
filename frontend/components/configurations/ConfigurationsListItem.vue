<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item
    :expandable-color="configuration.archived ? 'brown lighten-3' : 'grey lighten-5'"
    :background-color="configuration.archived ? 'brown lighten-4 ' : 'white'"
  >
    <template #header>
      <div class="d-flex flex-wrap">
        <div v-if="configuration.project" class="mr-1 text-caption">
          {{ configuration.project }}
        </div>
        <status-chip
          :value="configuration.status"
        />
        <visibility-chip
          v-model="configuration.visibility"
        />
        <permission-group-chips
          :value="configuration.permissionGroup ? [configuration.permissionGroup] : []"
          collapsible
        />
      </div>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <v-btn
        nuxt
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
      <v-tooltip v-if="configuration.archived" right>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on">
            mdi-archive-lock
          </v-icon>
        </template>
        <span>Archived</span>
      </v-tooltip>
      <span>{{ configuration.label | orDefault('Configuration') }}</span>
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
          <pid-tooltip :value="configuration.persistentIdentifier" />
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
          Start:
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
          {{ configuration.startDate | toUtcDateTimeStringHHMM | orDefault }}
          <span
            v-if="configuration.startDate"
            class="text-caption text--secondary"
          >
            (UTC)
          </span>
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
          End:
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
          {{ configuration.endDate | toUtcDateTimeStringHHMM | orDefault }}
          <span
            v-if="configuration.endDate"
            class="text-caption text--secondary"
          >
            (UTC)
          </span>
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
          Project:
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
          {{ configuration.project | orDefault }}
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
          Campaign:
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
          {{ configuration.campaign | orDefault }}
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
          {{ configuration.description | orDefault }}
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import StatusChip from '@/components/shared/StatusChip.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'

@Component({
  components: {
    BaseExpandableListItem,
    PermissionGroupChips,
    PidTooltip,
    StatusChip,
    VisibilityChip
  }
})
export default class ConfigurationsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly configuration!: Configuration

  @Prop({
    default: '',
    type: String
  })
  private from!: string

  get detailLink (): string {
    let params = ''
    if (this.from) {
      params = '?' + (new URLSearchParams({ from: this.from })).toString()
    }
    return `/configurations/${this.configuration.id}${params}`
  }
}
</script>

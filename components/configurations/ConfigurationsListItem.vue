<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
          :value="[configuration.permissionGroup]"
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
        :to="'/configurations/' + configuration.id"
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
          {{ configuration.startDate | dateToDateTimeString | orDefault }}
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
          {{ configuration.endDate | dateToDateTimeString | orDefault }}
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

import { dateToDateTimeString } from '@/utils/dateHelper'

import StatusChip from '@/components/shared/StatusChip.vue'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'

@Component({
  filters: { dateToDateTimeString },
  components: {
    StatusChip,
    VisibilityChip,
    PermissionGroupChips,
    BaseExpandableListItem
  }
})
export default class ConfigurationsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly configuration!: Configuration
}
</script>

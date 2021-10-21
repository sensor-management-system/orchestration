<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-hover>
    <template #default="{ hover }">
      <v-card
        :elevation="hover ? 6:2"
        class="ma-2"
      >
        <v-card-text
          @click.stop.prevent="toggleExapansion"
        >
          <v-row
            no-gutters
          >
            <v-col>
              <StatusBadge
                :value="configuration.status"
              >
                <div class="text-caption">
                  {{ configuration.projectName || 'no project' }}
                </div>
              </StatusBadge>
            </v-col>
            <v-col
              align-self="end"
              class="text-right"
            >
              <v-menu
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    :disabled="!isUserAuthenticated"
                    dense
                    @click="$emit('showDeleteDialog',configuration)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isUserAuthenticated ? 'red--text' : 'grey--text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isUserAuthenticated ? 'red' : 'grey'"
                        >
                          mdi-delete
                        </v-icon>
                        Delete
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
          <v-row
            no-gutters
          >
            <v-col class="text-subtitle-1">
              {{ getTextOrDefault(configuration.label, 'Configuration') }}
            </v-col>
            <v-col
              align-self="end"
              class="text-right"
            >
              <v-btn
                nuxt
                :to="'/configurations/' + configuration.id"
                color="primary"
                text
                @click.stop.prevent
              >
                View
              </v-btn>
              <v-btn
                icon
                @click.stop.prevent="toggleExapansion"
              >
                <v-icon>{{ isExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-expand-transition>
          <v-card
            v-show="isExpanded"
            flat
            tile
            color="grey lighten-5"
          >
            <v-card-text>
              <v-row
                dense
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
                  {{ configuration.startDate | dateToDateTimeString }}
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
                  {{ configuration.endDate | dateToDateTimeString }}
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </v-card>
    </template>
  </v-hover>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'
import { DynamicLocation, LocationType, StationaryLocation } from '@/models/Location'

import { dateToDateTimeString } from '@/utils/dateHelper'

import StatusBadge from '@/components/StatusBadge.vue'

@Component({
  filters: { dateToDateTimeString },
  components: { StatusBadge }
})
export default class ConfigurationsOverviewCard extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly configuration!: Configuration

  @Prop({
    type: Boolean,
    required: true
  })
  readonly isUserAuthenticated!: boolean

  private isExpanded:boolean=false;

  getLocationType (configuration: Configuration): string {
    if (configuration.location instanceof StationaryLocation) {
      return LocationType.Stationary
    }
    if (configuration.location instanceof DynamicLocation) {
      return LocationType.Dynamic
    }
    return ''
  }

  toggleExapansion () {
    this.isExpanded = !this.isExpanded
  }

  getTextOrDefault = (text: string, defaultValue: string): string => text || defaultValue
}
</script>

<style scoped>

</style>

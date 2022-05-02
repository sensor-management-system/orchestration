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
  <v-hover>
    <template #default="{ hover }">
      <v-card
        :elevation="hover ? 6:2"
        class="ma-2"
      >
        <v-card-text
          @click.stop.prevent="show = !show"
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
              <DotMenu>
                <template #actions>
                  <slot name="dot-menu-items" />
                </template>
              </DotMenu>
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
                @click.stop.prevent="show = !show"
              >
                <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-expand-transition>
          <v-card
            v-show="show"
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
                  {{ configuration.endDate | dateToDateTimeString }}
                  <span
                    v-if="configuration.endDate"
                    class="text-caption text--secondary"
                  >
                    (UTC)
                  </span>
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
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import DotMenu from '@/components/DotMenu.vue'
import { Configuration } from '@/models/Configuration'
import StatusBadge from '@/components/StatusBadge.vue'
import { dateToDateTimeString } from '@/utils/dateHelper'

@Component({
  filters: { dateToDateTimeString },
  components: { DotMenu, StatusBadge }
})
export default class ConfigurationsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly configuration!: Configuration

  private show = false

  getTextOrDefault = (text: string, defaultValue: string): string => text ?? defaultValue
}
</script>

<style scoped>

</style>

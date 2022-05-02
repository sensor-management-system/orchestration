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
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-card-text
        @click.stop.prevent="show = !show"
      >
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{ device.shortName }}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
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
          <v-container>
            <v-card class="mb-2">
              <v-card-text
                @click.stop.prevent="showOverview = !showOverview"
              >
                <v-row
                  no-gutters
                >
                  <v-col class="text-subtitle-1">
                    Device overview
                  </v-col>
                  <v-col
                    align-self="end"
                    class="text-right"
                  >
                    <v-btn
                      icon
                      @click.stop.prevent="showOverview = !showOverview"
                    >
                      <v-icon>{{ showOverview ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-expand-transition>
                <v-card
                  v-show="showOverview"
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
                        class="font-weight-medium"
                      >
                        Manufacturer:
                      </v-col>
                      <v-col
                        cols="8"
                        class="nowrap-truncate"
                      >
                        {{ getTextOrDefault(device.manufacturerName) }}
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
                        {{ getTextOrDefault(device.model) }}
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
                        {{ getTextOrDefault(device.serialNumber) }}
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
                        {{ getTextOrDefault(device.inventoryNumber) }}
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
                      >
                        {{ getTextOrDefault(device.description) }}
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-btn :href="'devices/' + device.id" target="_blank" :disabled="false">
                          <v-icon>
                            mdi-open-in-new
                          </v-icon>
                          Open in new tab
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-expand-transition>
            </v-card>
            <v-card>
              <v-card-text
                @click.stop.prevent="showMount = !showMount"
              >
                <v-row
                  no-gutters
                >
                  <v-col class="text-subtitle-1">
                    Mount
                  </v-col>
                  <v-col
                    align-self="end"
                    class="text-right"
                  >
                    <v-btn
                      icon
                      @click.stop.prevent="showMount = !showMount"
                    >
                      <v-icon>{{ showMount ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-expand-transition>
                <v-card
                  v-show="showMount"
                  flat
                  tile
                  color="grey lighten-5"
                >
                  <v-card-text>
                    <slot name="mount" />
                  </v-card-text>
                </v-card>
              </v-expand-transition>
            </v-card>
          </v-container>
        </v-card>
      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
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

  getTextOrDefault = (text: string): string => text || '-'
}
</script>

<style scoped>

</style>

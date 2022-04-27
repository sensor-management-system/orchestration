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
            {{ platform.shortName }}
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
                    Platform overview
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
                        {{ getTextOrDefault(platform.manufacturerName) }}
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
                        {{ getTextOrDefault(platform.model) }}
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
                        {{ getTextOrDefault(platform.serialNumber) }}
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
                        {{ getTextOrDefault(platform.inventoryNumber) }}
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
                        {{ getTextOrDefault(platform.description) }}
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-btn :href="'platforms/' + platform.id" target="_blank">
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
                    <slot name="mount"></slot>
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
import { Platform } from '@/models/Platform'

@Component
export default class PlatformMountListItem extends Vue {
  @Prop({
    required:true,
    type: Object
  })
  private platform!:Platform
  private show = false
  private showOverview = false
  private showMount = false

  getTextOrDefault = (text: string): string => text || '-'
}
</script>

<style scoped>

</style>

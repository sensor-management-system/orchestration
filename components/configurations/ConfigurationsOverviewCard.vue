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
                  {{ getLocationType(configuration) }}
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
                    dense
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isLoggedIn ? 'text' : 'grey-text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isLoggedIn ? 'black' : 'grey'"
                        >
                          mdi-content-copy
                        </v-icon>
                        Copy
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item
                    :disabled="!isLoggedIn"
                    dense
                    @click="$emit('showDeleteDialog',configuration)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        :class="isLoggedIn ? 'red--text' : 'grey--text'"
                      >
                        <v-icon
                          left
                          small
                          :color="isLoggedIn ? 'red' : 'grey'"
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
                  {{ getTextOrDefault(configuration.projectName, '-') }}
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

  get isLoggedIn () { // TODO entfernen, wenn es ordentliche autorisierung gibt
    return this.$store.getters['oidc/isAuthenticated']
  }

  getTextOrDefault = (text: string, defaultValue: string): string => text || defaultValue
}
</script>

<style scoped>

</style>

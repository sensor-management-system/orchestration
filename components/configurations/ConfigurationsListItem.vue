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

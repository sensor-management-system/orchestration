<template>
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-header class="py-0 pl-0">
        <v-container class="pa-0">
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-subtitle class="pb-0">
                {{ action.date | dateToDateTimeString }}
              </v-card-subtitle>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-title class="pt-0 pb-0">
                {{ action.title }}
              </v-card-title>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-card-subtitle class="pt-0">
                {{ action.contact.toString() }}
              </v-card-subtitle>
            </v-col>
          </v-row>
        </v-container>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-card-text
          class="text--primary"
        >
          <v-row
            v-if="action.mountInfo && action.mountInfo.parentPlatform"
            dense
          >
            <v-col cols="12" md="4">
              <label>Mounted on</label>
              {{ action.mountInfo.parentPlatform.shortName }}
            </v-col>
          </v-row>
          <v-row
            v-if="action.mountInfo"
            dense
          >
            <v-col cols="12" md="3">
              <label>Offset x</label>
              {{ action.mountInfo.offsetX }}
            </v-col>
            <v-col cols="12" md="3">
              <label>Offset y</label>
              {{ action.mountInfo.offsetY }}
            </v-col>
            <v-col cols="12" md="3">
              <label>Offset z</label>
              {{ action.mountInfo.offsetZ }}
            </v-col>
          </v-row>
          <v-row dense>
            <v-col>
              <label>Description</label>
              {{ action.description }}
            </v-col>
          </v-row>
        </v-card-text>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { ITimelineAction } from '@/utils/configurationInterfaces'
import { dateToDateTimeString } from '@/utils/dateHelper'

@Component({
  filters: {
    dateToDateTimeString
  }
})
export default class ConfigurationsTimelineActionCard extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly action!: ITimelineAction
}
</script>

<style scoped>

</style>

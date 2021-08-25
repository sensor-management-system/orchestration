<template>
  <div>
    <v-row v-if="!readonly">
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number.lazy="configuration.location.latitude"
          label="Latitude (WGS84)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number.lazy="configuration.location.longitude"
          label="Longitude (WGS84)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number="configuration.location.elevation"
          label="Elevation (m asl)"
          type="number"
          :readonly="readonly"
          @wheel.prevent
        />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12" md="3">
        <label>Latitude (WGS84)</label>
        {{ configuration.location.latitude }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Longitude (WGS84)</label>
        {{ configuration.location.longitude }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Elevation (m asl)</label>
        {{ configuration.location.elevation }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

@Component
export default class StationaryLocationRow extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({ default: false, type: Configuration }) configuration!: Configuration
}
</script>

<style scoped>

</style>

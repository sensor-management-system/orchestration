<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="compartment"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          label="unit"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="accuracy"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="sampling media"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range min"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range min"
        />
      </v-col>
      <v-col cols="12" md="3" offset="1">
        <v-text-field
          label="label"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="variable"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="failure value"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a sensor property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import { SensorProperty } from '../models/SensorProperty'

/**
 * A class component for a sensor property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class SensorPropertyForm extends Vue {
}
</script>

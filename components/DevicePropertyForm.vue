<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="compartment"
          :value="value.compartment"
          @input="update('compartment', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          label="unit"
          :value="value.unit"
          @input="update('unit', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="accuracy"
          :value="value.accuracy"
          @input="update('accuracy', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="sampling media"
          :value="value.samplingMedia"
          @input="update('samplingMedia', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range min"
          :value="value.measuringRange.min"
          @input="update('measuringRange.min', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range max"
          :value="value.measuringRange.max"
          @input="update('measuringRange.max', $event)"
        />
      </v-col>
      <v-col cols="12" md="3" offset="1">
        <v-text-field
          label="label"
          :value="value.label"
          @input="update('label', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="variable"
          :value="value.variable"
          @input="update('variable', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="failure value"
          :value="value.failureValue"
          @input="update('failureValue', $event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a device property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '../models/DeviceProperty'

/**
 * A class component for a device property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyForm extends Vue {
  @Prop({
    default: () => new DeviceProperty(),
    required: true,
    type: DeviceProperty
  })
  // @ts-ignore
  value!: DeviceProperty

  /**
   * update the internal model at a given key
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires DevicePropertyForm#input
   */
  update (key: string, value: string) {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)
    newObj.setPath(key, value)

    /**
     * input event
     * @event DevicePropertyForm#input
     * @type DeviceProperty
     */
    this.$emit('input', newObj)
  }
}
</script>

<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="Compartment"
          :value="value.compartmentUri"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('compartmentUri', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          label="Unit"
          :value="value.unitUri"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('unitUri', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Accuracy"
          :value="value.accuracy"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('accuracy', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="Sampling media"
          :value="value.samplingMediaUri"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('samplingMediaUri', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="Measuring range min"
          :value="value.measuringRange.min"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.min', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="Measuring range max"
          :value="value.measuringRange.max"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.max', $event)"
        />
      </v-col>
      <v-col cols="12" md="3" offset="1">
        <v-text-field
          label="Label"
          :value="value.label"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('label', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="Property"
          :value="value.propertyUri"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('propertyUri', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Failure value"
          :value="value.failureValue"
          :readonly="readonly"
          :disabled="readonly"
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
  readonly value!: DeviceProperty

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

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

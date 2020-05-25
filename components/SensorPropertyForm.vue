<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="compartment"
          :value="value.compartment"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('compartment', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          label="unit"
          :value="value.unit"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('unit', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="accuracy"
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
          label="sampling media"
          :value="value.samplingMedia"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('samplingMedia', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range min"
          :value="value.measuringRange.min"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.min', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="measuring range max"
          :value="value.measuringRange.max"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.max', $event)"
        />
      </v-col>
      <v-col cols="12" md="3" offset="1">
        <v-text-field
          label="label"
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
          label="variable"
          :value="value.variable"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('variable', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="failure value"
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
 * @file provides a component for a sensor property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { SensorProperty } from '../models/SensorProperty'

/**
 * A class component for a sensor property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class SensorPropertyForm extends Vue {
  @Prop({
    default: () => new SensorProperty(),
    required: true,
    type: SensorProperty
  })
  // @ts-ignore
  value!: SensorProperty

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * update the internal model at a given key
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires SensorPropertyForm#input
   */
  update (key: string, value: string) {
    const newObj: SensorProperty = SensorProperty.createFromObject(this.value)
    newObj.setPath(key, value)

    /**
     * input event
     * @event SensorPropertyForm#input
     * @type SensorProperty
     */
    this.$emit('input', newObj)
  }
}
</script>

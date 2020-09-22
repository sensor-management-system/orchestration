<template>
  <v-row>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetX"
        label="Offset (x)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetX', $event)"
      />
    </v-col>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetY"
        label="Offset (y)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetY', $event)"
      />
    </v-col>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetZ"
        label="Offset (z)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetZ', $event)"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
/**
 * @file provides a component for platform configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'
import { parseFloatOrDefault } from '@/utils/numericsHelper'

/**
 * A class component for platform configuration attributes
 * @extends Vue
 */
@Component
// @ts-ignore
export default class PlatformConfigurationAttributesForm extends Vue {
  @Prop({
    required: true,
    type: PlatformConfigurationAttributes
  })
  // @ts-ignore
  readonly value!: PlatformConfigurationAttributes

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
   * @param {any} value - the value to set
   * @fires PlatformConfigurationAttributesForm#input
   */
  update (key: string, value: any) {
    const newObj: PlatformConfigurationAttributes = PlatformConfigurationAttributes.createFromObject(this.value)

    switch (key) {
      case 'offsetX':
        newObj.offsetX = parseFloatOrDefault(value, 0) as number
        break
      case 'offsetY':
        newObj.offsetY = parseFloatOrDefault(value, 0) as number
        break
      case 'offsetZ':
        newObj.offsetZ = parseFloatOrDefault(value, 0) as number
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event PlatformConfigurationAttributes#input
     * @type PlatformConfigurationAttributes
     */
    this.$emit('input', newObj)
  }
}
</script>

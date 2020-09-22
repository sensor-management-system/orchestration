<template>
  <div>
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
      <v-col
        cols="12"
        md="2"
      >
        <v-menu
          v-model="calibrationDateMenu"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              :value="dateToString(value.calibrationDate)"
              label="Calibration date"
              prepend-icon="mdi-calendar-range"
              readonly
              :disabled="readonly"
              v-bind="attrs"
              v-on="on"
            />
          </template>
          <v-date-picker
            :value="dateToString(value.calibrationDate)"
            :readonly="readonly"
            :disabled="readonly"
            @input="update('calibrationDate', $event); calibrationDateMenu = false"
          />
        </v-menu>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        md="3"
      >
        <DevicePropertySelect
          :value="value.deviceProperties"
          :properties="value.device.properties"
          label="Add one or more properties"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('deviceProperties', $event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for device configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import DevicePropertySelect from '@/components/DevicePropertySelect.vue'

import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { parseFloatOrDefault } from '@/utils/numericsHelper'
import { dateToString, stringToDate } from '@/utils/dateHelper'

/**
 * A class component for device configuration attributes
 * @extends Vue
 */
@Component({
  components: {
    DevicePropertySelect
  }
})
// @ts-ignore
export default class DeviceConfigurationAttributesForm extends Vue {
  private calibrationDateMenu: boolean = false

  @Prop({
    required: true,
    type: DeviceConfigurationAttributes
  })
  // @ts-ignore
  readonly value!: DeviceConfigurationAttributes

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
   * @fires DeviceConfigurationAttributesForm#input
   */
  update (key: string, value: any) {
    const newObj: DeviceConfigurationAttributes = DeviceConfigurationAttributes.createFromObject(this.value)

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
      case 'calibrationDate':
        newObj.calibrationDate = stringToDate(value)
        break
      case 'deviceProperties':
        newObj.deviceProperties = value
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event DeviceConfigurationAttributes#input
     * @type DeviceConfigurationAttributes
     */
    this.$emit('input', newObj)
  }

  dateToString (aDate: Date | null): string {
    return dateToString(aDate)
  }
}
</script>

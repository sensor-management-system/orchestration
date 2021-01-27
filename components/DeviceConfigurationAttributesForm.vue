<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
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
          @wheel.prevent
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
          @wheel.prevent
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
          @wheel.prevent
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
              :value="calibrationDateStringHelper"
              label="Calibration date"
              prepend-icon="mdi-calendar-range"
              readonly
              clearable
              :disabled="readonly"
              v-bind="attrs"
              v-on="on"
              @click:clear="value.calibrationDate = null"
            />
          </template>
          <v-date-picker
            :value="calibrationDateStringHelper"
            :readonly="readonly"
            :disabled="readonly"
            @input="update('calibrationDate', $event); calibrationDateMenu = false"
          />
        </v-menu>
      </v-col>
      <v-col
        cols="12"
        md="2"
      >
        <v-text-field
          :value="value.firemwareVersion"
          label="Firmware version"
          :readonly="readonly"
          :disabled="readonly"
          @change="update('firmwareVersion', $event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component that renders a form for device configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import DevicePropertySelect from '@/components/DevicePropertySelect.vue'

import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { parseFloatOrDefault } from '@/utils/numericsHelper'
import { dateToString, stringToDate } from '@/utils/dateHelper'

/**
 * A class component that renders a form for device configuration attributes
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

  /**
   * a list of DeviceConfigurationAttributes
   */
  @Prop({
    required: true,
    type: DeviceConfigurationAttributes
  })
  // @ts-ignore
  readonly value!: DeviceConfigurationAttributes

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * update a copy of the internal model at a given key and triggers an input event
   *
   * @param {string} key - a path to the property to set
   * @param {any} value - the value to set
   * @fires DeviceConfigurationAttributesForm#input
   */
  update (key: string, value: any) {
    const newObj: DeviceConfigurationAttributes = DeviceConfigurationAttributes.createFromObject(this.value)

    switch (key) {
      case 'offsetX':
        newObj.offsetX = parseFloatOrDefault(value, 0)
        break
      case 'offsetY':
        newObj.offsetY = parseFloatOrDefault(value, 0)
        break
      case 'offsetZ':
        newObj.offsetZ = parseFloatOrDefault(value, 0)
        break
      case 'calibrationDate':
        newObj.calibrationDate = stringToDate(value)
        break
      case 'firmwareVersion':
        newObj.firmwareVersion = String(value)
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event DeviceConfigurationAttributes#input
     * @type {DeviceConfigurationAttributes}
     */
    this.$emit('input', newObj)
  }

  /**
   * returns the calibration date as a string
   *
   * @return {string} the calibration date
   */
  get calibrationDateStringHelper (): string {
    return dateToString(this.value.calibrationDate)
  }
}
</script>

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
  <v-form ref="basicForm">
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          :value="deviceURN"
          label="URN"
          readonly
          disabled
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.persistentIdentifier"
          :readonly="readonly"
          :disabled="readonly"
          label="Persistent identifier (PID)"
          @input="update('persistentIdentifier', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.shortName"
          :readonly="readonly"
          :disabled="readonly"
          label="Short name"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('shortName', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.longName"
          :readonly="readonly"
          :disabled="readonly"
          label="Long name"
          @input="update('longName', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
          :value="deviceStatusName"
          :items="statusNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Status"
          @input="update('statusName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="deviceTypeName"
          :items="deviceTypeNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Device type"
          @input="update('deviceTypeName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="deviceManufacturerName"
          :items="manufacturerNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Manufacturer"
          @input="update('manufacturerName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.model"
          :readonly="readonly"
          :disabled="readonly"
          label="Model"
          @input="update('model', $event)"
        />
      </v-col>
    </v-row>
    <v-divider />
    <v-row>
      <v-col cols="12" md="9">
        <v-textarea
          :value="value.description"
          :readonly="readonly"
          :disabled="readonly"
          label="Description"
          rows="3"
          @input="update('description', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-text-field
          :value="value.website"
          :readonly="readonly"
          :disabled="readonly"
          label="Website"
          placeholder="https://"
          type="url"
          @input="update('website', $event)"
        >
          <template slot="append">
            <a v-if="value.website.length > 0" :href="value.website" target="_blank">
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
        </v-text-field>
      </v-col>
    </v-row>
    <v-divider />
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.serialNumber"
          :readonly="readonly"
          :disabled="readonly"
          label="Serial number"
          @input="update('serialNumber', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.inventoryNumber"
          :readonly="readonly"
          :disabled="readonly"
          label="Inventory number"
          @input="update('inventoryNumber', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-checkbox
          :value="value.dualUse"
          :readonly="readonly"
          :disabled="readonly"
          label="Dual use"
          hint="can be used for military aims"
          :persistent-hint="true"
          color="red darken-3"
          @input="update('dualUse', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

@Component
export default class DeviceBasicDataForm extends mixins(Rules) {
  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private deviceTypes: DeviceType[] = []

  @Prop({
    required: true,
    type: Device
  })
  readonly value!: Device

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  mounted () {
    this.$api.states.findAllPaginated().then((foundStates) => {
      this.states = foundStates
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of states failed')
    })
    this.$api.manufacturer.findAllPaginated().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    })
    this.$api.deviceTypes.findAllPaginated().then((foundDeviceTypes) => {
      this.deviceTypes = foundDeviceTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of device types failed')
    })
  }

  update (key: string, value: string) {
    const newObj = Device.createFromObject(this.value)

    switch (key) {
      case 'persistentIdentifier':
        newObj.persistentIdentifier = value
        break
      case 'shortName':
        newObj.shortName = value
        break
      case 'longName':
        newObj.longName = value
        break
      case 'statusName':
        newObj.statusName = value
        { // for lexical scope
          const statusIndex = this.states.findIndex(s => s.name === value)
          if (statusIndex > -1) {
            newObj.statusUri = this.states[statusIndex].uri
          } else {
            newObj.statusUri = ''
          }
        }
        break
      case 'deviceTypeName':
        newObj.deviceTypeName = value
        {
          const deviceTypeIndex = this.deviceTypes.findIndex(t => t.name === value)
          if (deviceTypeIndex > -1) {
            newObj.deviceTypeUri = this.deviceTypes[deviceTypeIndex].uri
          } else {
            newObj.deviceTypeUri = ''
          }
        }
        break
      case 'manufacturerName':
        newObj.manufacturerName = value
        {
          const manufacturerIndex = this.manufacturers.findIndex(m => m.name === value)
          if (manufacturerIndex > -1) {
            newObj.manufacturerUri = this.manufacturers[manufacturerIndex].uri
          } else {
            newObj.manufacturerUri = ''
          }
        }
        break
      case 'model':
        newObj.model = value
        break
      case 'description':
        newObj.description = value
        break
      case 'website':
        newObj.website = value
        break
      case 'serialNumber':
        newObj.serialNumber = value
        break
      case 'inventoryNumber':
        newObj.inventoryNumber = value
        break
      case 'dualUse':
        newObj.dualUse = value === 'true'
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    this.$emit('input', newObj)
  }

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get statusNames (): string[] {
    return this.states.map(s => s.name)
  }

  get deviceTypeNames (): string[] {
    return this.deviceTypes.map(t => t.name)
  }

  get deviceManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get deviceStatusName () {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.value.statusName
  }

  get deviceTypeName () {
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.uri === this.value.deviceTypeUri)
    if (deviceTypeIndex > -1) {
      return this.deviceTypes[deviceTypeIndex].name
    }
    return this.value.deviceTypeName
  }

  get deviceURN () {
    let partManufacturer = '[manufacturer]'
    let partModel = '[model]'
    let partSerialNumber = '[serial_number]'

    if (this.value.manufacturerUri !== '') {
      const manIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
      if (manIndex > -1) {
        partManufacturer = this.manufacturers[manIndex].name
      } else if (this.value.manufacturerName !== '') {
        partManufacturer = this.value.manufacturerName
      }
    } else if (this.value.manufacturerName !== '') {
      partManufacturer = this.value.manufacturerName
    }

    if (this.value.model !== '') {
      partModel = this.value.model
    }

    if (this.value.serialNumber !== '') {
      partSerialNumber = this.value.serialNumber
    }

    return [partManufacturer, partModel, partSerialNumber].join('_').replace(
      ' ', '_'
    )
  }
}
</script>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-row v-if="!readonly">
      <v-col cols="12" md="3">
        <device-property-hierarchy-select
          :value="configuration.location.latitude"
          :devices="getAllDevices()"
          device-select-label="Device that measures latitude"
          property-select-label="Measured quantity for latitude"
          :readonly="readonly"
          @input="updateLatitude"
        />
      </v-col>
      <v-col cols="12" md="3">
        <device-property-hierarchy-select
          :value="configuration.location.longitude"
          :devices="getAllDevices()"
          device-select-label="Device that measures longitude"
          property-select-label="Measured quantity for longitude"
          :readonly="readonly"
          @input="updateLongitude"
        />
      </v-col>
      <v-col cols="12" md="3">
        <device-property-hierarchy-select
          :value="configuration.location.elevation"
          :devices="getAllDevices()"
          device-select-label="Device that measures elevation"
          property-select-label="Measured quantity for elevation"
          :readonly="readonly"
          @input="updateElevation"
        />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12" md="3">
        <label>Latitude</label>
        <span v-if="configuration.location.latitude">
          {{ configuration.location.latitude.propertyName }}
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <label>Longitude</label>
        <span v-if="configuration.location.longitude">
          {{ configuration.location.longitude.propertyName }}
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <label>Elevation</label>
        <span v-if="configuration.location.elevation">
          {{ configuration.location.elevation.propertyName }}
        </span>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IDynamicLocation } from '@/models/Location'

import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'

@Component({
  components: { DevicePropertyHierarchySelect }
})
export default class DynamicLocationRow extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({ default: false, type: Configuration }) configuration!: Configuration

  getAllDevices (): Device[] {
    const result = []
    const alreadyAddedDeviceIds = new Set()
    for (const deviceMountAction of this.configuration.deviceMountActions) {
      const device = deviceMountAction.device
      const deviceId = device.id
      if (!alreadyAddedDeviceIds.has(deviceId)) {
        result.push(device)
        alreadyAddedDeviceIds.add(deviceId)
      }
    }
    return result
  }

  updateLatitude (property: DeviceProperty | null) {
    this.updateLocation('latitude', property)
  }

  updateLongitude (property: DeviceProperty | null) {
    this.updateLocation('longitude', property)
  }

  updateElevation (property: DeviceProperty | null) {
    this.updateLocation('elevation', property)
  }

  updateLocation (target: keyof IDynamicLocation, property: DeviceProperty | null) {
    const configurationCopy = Configuration.createFromObject(this.configuration)
    if (!configurationCopy.location) {
      return
    }
    if (target in configurationCopy.location) {
      configurationCopy.location[target] = property
    }
    this.$emit('input', configurationCopy)
  }
}
</script>

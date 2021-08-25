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

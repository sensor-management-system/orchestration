<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-form
    ref="DynamicLocationActionDeviceForm"
  >
    <v-row>
      <v-col cols="12" md="4">
        <device-property-hierarchy-select
          :value="value.x"
          :devices="availableDevices"
          :device-select-rules="[rules.required, deviceNotArchived]"
          :property-select-rules="[rules.required]"
          class="required"
          device-select-label="Device that measures x"
          property-select-label="Measured quantity for x"
          @input="update(constList.x, $event)"
        />
      </v-col>
      <v-col cols="12" md="4">
        <device-property-hierarchy-select
          :value="value.y"
          :devices="availableDevices"
          :device-select-rules="[rules.required, deviceNotArchived]"
          :property-select-rules="[rules.required]"
          class="required"
          device-select-label="Device that measures y"
          property-select-label="Measured quantity for y"
          @input="update(constList.y, $event)"
        />
      </v-col>
      <v-col cols="12" md="4">
        <device-property-hierarchy-select
          :value="value.z"
          :devices="availableDevices"
          :device-select-rules="[deviceNotArchived]"
          device-select-label="Device that measures z"
          property-select-label="Measured quantity for z"
          @input="update(constList.z, $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import { Rules } from '@/mixins/Rules'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { ActiveDevicesWithPropertiesForDateGetter } from '@/store/configurations'

@Component({
  components: { DevicePropertyHierarchySelect },
  computed: {
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate', 'unavailableDevicesWithReasonsForDates'])
  }
})
export default class DynamicLocationActionDeviceForm extends mixins(Rules) {
  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: DynamicLocationAction
  })
  readonly value!: DynamicLocationAction

  private temporarlyStoredActiveDevices: Device[] = []
  private constList = {
    x: 'x',
    y: 'y',
    z: 'z'
  }

  // vuex definition for typescript check
  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter

  get availableDevices () {
    if (!this.value.beginDate) {
      return this.temporarlyStoredActiveDevices
    }
    this.temporarlyStoredActiveDevices = this.activeDevicesWithPropertiesForDate(this.value.beginDate, this.value.endDate)
    return this.activeDevicesWithPropertiesForDate(this.value.beginDate, this.value.endDate)
  }

  deviceNotArchived (device: Device | null) {
    if (!device) {
      return true
    }
    if (device.archived) {
      return 'The device must not be archived'
    }
    return true
  }

  update (key: string, value: any): void {
    const newObj = DynamicLocationAction.createFromObject(this.value)

    switch (key) {
      case this.constList.x:
        newObj.x = value as DeviceProperty | null
        break
      case this.constList.y:
        newObj.y = value as DeviceProperty | null
        break
      case this.constList.z:
        newObj.z = value as DeviceProperty | null
        break
    }
    this.$emit('input', newObj)
  }

  public validateForm (): boolean {
    return (this.$refs.DynamicLocationActionDeviceForm as Vue & { validate: () => boolean }).validate()
  }

  isPropertyAvailable (property: DeviceProperty | null) {
    if (!property) {
      return true
    }
    return this.availableDevices.some((device: Device) => {
      return device.properties.filter(deviceProperty => deviceProperty.id === property.id).length > 0
    })
  }

  private resetPropertyIfNotAvailable () {
    const newObj = DynamicLocationAction.createFromObject(this.value)
    let mustBeEmitted = false
    if (!this.isPropertyAvailable(this.value.x)) {
      mustBeEmitted = true
      newObj.x = null
    }
    if (!this.isPropertyAvailable(this.value.y)) {
      mustBeEmitted = true
      newObj.y = null
    }
    if (!this.isPropertyAvailable(this.value.z)) {
      mustBeEmitted = true
      newObj.z = null
    }

    if (mustBeEmitted) {
      this.$emit('input', newObj)
    }
  }

  @Watch('value')
  onValueChanged (newVal: DynamicLocationAction, oldVal: DynamicLocationAction) {
    if (newVal.beginDate !== oldVal.beginDate || newVal.endDate !== oldVal.endDate) {
      this.resetPropertyIfNotAvailable()
    }
  }
}
</script>

<style scoped>

</style>

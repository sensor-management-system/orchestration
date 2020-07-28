<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllDeviceTypes"
    add-label="Add a device type"
    color="red"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select device types
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import DeviceType from '@/models/DeviceType'
import CVService from '@/services/CVService'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

type DeviceTypeLoaderFunction = () => Promise<DeviceType[]>

/**
 * A class component to select device types
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class DeviceTypeSelect extends Vue {
  @Prop({
    default: () => [] as DeviceType[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: DeviceType[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  get findAllDeviceTypes (): DeviceTypeLoaderFunction {
    return CVService.findAllDeviceTypes
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

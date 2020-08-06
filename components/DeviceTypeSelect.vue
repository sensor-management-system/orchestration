<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllDeviceTypes"
    :label="label"
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

import EntitySelect from '@/components/EntitySelect.vue'

import DeviceType from '@/models/DeviceType'

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

  @Prop({
    required: true,
    type: String
  })
  readonly label!: string

  get findAllDeviceTypes (): DeviceTypeLoaderFunction {
    return () => { return this.$api.deviceTypes.findAll() }
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="getAvailableDeviceProperties"
    :label="label"
    color="green"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select device properties
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { DeviceProperty } from '@/models/DeviceProperty'

type DevicePropertysLoaderFunction = () => Promise<DeviceProperty[]>

/**
 * A class component to select deviceProperties
 * @extends Vue
 */
@Component({
  components: { EntitySelect }
})
// @ts-ignore
export default class DevicePropertySelect extends Vue {
  private deviceProperties: DeviceProperty[] = []

  @Prop({
    default: () => [] as DeviceProperty[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: DeviceProperty[]

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
  // @ts-ignore
  readonly label!: string

  @Prop({
    default: () => [] as DeviceProperty[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly properties!: DeviceProperty[]

  get getAvailableDeviceProperties () : DevicePropertysLoaderFunction {
    return () => new Promise((resolve) => {
      resolve(
        this.properties
      )
    })
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

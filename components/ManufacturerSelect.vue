<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllManufacturers"
    :label="label"
    color="brown"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select manufacturers
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import CVService from '@/services/CVService'

import Manufacturer from '@/models/Manufacturer'

type ManufacturersLoaderFunction = () => Promise<Manufacturer[]>

/**
 * A class component to select manufacturers
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class ManufacturerSelect extends Vue {
  @Prop({
    default: () => [] as Manufacturer[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Manufacturer[]

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
  readonly label!: String

  get findAllManufacturers (): ManufacturersLoaderFunction {
    return CVService.findAllManufacturers
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

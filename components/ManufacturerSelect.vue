<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllManufacturers"
    add-label="Add a manufacturer"
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

import Manufacturer from '../models/Manufacturer'
import CVService from '../services/CVService'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

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
  value!: Manufacturer[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

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

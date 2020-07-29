<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllPlatformTypes"
    :label="label"
    color="red"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select platform types
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import PlatformType from '@/models/PlatformType'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

type PlatformTypeLoaderFunction = () => Promise<PlatformType[]>

/**
 * A class component to select platform types
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class PlatformTypeSelect extends Vue {
  @Prop({
    default: () => [] as PlatformType[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: PlatformType[]

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

  get findAllPlatformTypes (): PlatformTypeLoaderFunction {
    return () => { return this.$api.platformTypes.findAll() }
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

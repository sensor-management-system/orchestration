<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllPlatformTypes"
    add-label="Add a platform type"
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
import Api from '@/services/Api'

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

  get findAllPlatformTypes (): PlatformTypeLoaderFunction {
    return () => {
      return new Api().cv.platformTypes.findAll()
    }
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllStates"
    :label="label"
    color="green"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select states
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { Status } from '@/models/Status'

type StatesLoaderFunction = () => Promise<Status[]>

/**
 * A class component to select states
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class StatusSelect extends Vue {
  @Prop({
    default: () => [] as Status[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Status[]

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

  get findAllStates (): StatesLoaderFunction {
    return () => { return this.$api.states.findAll() }
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllStates"
    add-label="Add a status"
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

import Status from '@/models/Status'
import CVService from '@/services/CVService'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

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

  get findAllStates (): StatesLoaderFunction {
    return CVService.findAllStates
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

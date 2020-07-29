<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllContacts"
    :label="label"
    color="indigo"
    avatar-icon="mdi-account-circle"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select contacts
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import Contact from '../models/Contact'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

type ContactsLoaderFunction = () => Promise<Contact[]>

/**
 * A class component to select contacts
 * @extends Vue
 */
@Component({
  components: { EntitySelect }
})
// @ts-ignore
export default class ContactSelect extends Vue {
  private contacts: Contact[] = []

  @Prop({
    default: () => [] as Contact[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Contact[]

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

  get findAllContacts () : ContactsLoaderFunction {
    return () => { return this.$api.contacts.findAll() }
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }
}
</script>

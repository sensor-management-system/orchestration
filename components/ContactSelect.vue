<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllContacts"
    add-label="Add a contact"
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
import SmsService from '../services/SmsService'

// @ts-ignore
import EntitySelect from '@/components/EntitySelect'

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
  value!: Contact[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  get findAllContacts () : () => Promise<Contact[]> {
    return SmsService.findAllContacts
  }

  get wrappedValue () {
    return this.value
  }

  set wrappedValue (newValue) {
    this.$emit('input', newValue)
  }

  /**
   * fetches all available contacts from the SmsService
   *
   * @async
   */
  async fetch () {
    this.contacts = await SmsService.findAllContacts()
  }
}
</script>

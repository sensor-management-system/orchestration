<template>
  <div>
    <v-autocomplete
      v-if="!readonly"
      :items="allContactsExceptSelected"
      :item-text="(x) => x"
      :item-value="(x) => x.id"
      label="add a contact"
      @change="addContact"
    />
    <v-chip
      v-for="contact in selectedContacts"
      :key="contact.id"
      class="ma-2"
      color="indigo"
      text-color="white"
      :close="!readonly"
      @click:close="removeContact(contact.id)"
    >
      <v-avatar left>
        <v-icon>mdi-account-circle</v-icon>
      </v-avatar>
      {{ contact }}
    </v-chip>
  </div>
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

/**
 * A class component to select contacts
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ContactSelect extends Vue {
  private contacts: Contact[] = []

  @Prop({
    default: () => [] as Contact[],
    required: true,
    type: Array
  })
  // @ts-ignore
  selectedContacts!: Contact[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * fetches all available contacts from the ContactService
   *
   * @async
   */
  async fetch () {
    this.contacts = await SmsService.findAllContacts()
  }

  /**
   * adds a contact to the devices contact property
   *
   * @param {string} someContactId - the id of the contact to add
   * @fires ContactSelect#update:selectedContacts
   */
  addContact (someContactId: string) {
    const selectedContact: Contact | undefined = this.contacts.find(c => c.id === parseInt(someContactId))
    if (selectedContact) {
      /**
       * Update event
       * @event ContactSelect#update:selectedContacts
       * @type Contact[]
       */
      this.$emit('update:selectedContacts', [
        ...this.selectedContacts,
        selectedContact
      ] as Contact[])
    }
  }

  /**
   * removes a contact from the devices contacts property
   *
   * @param {number} someContactId - the id of the contact to remove
   * @fires ContactSelect#update:selectedContacts
   */
  removeContact (someContactId: number) {
    const contactIndex: number = this.selectedContacts.findIndex(c => c.id === someContactId)
    if (contactIndex > -1) {
      /**
       * Update event
       * @event ContactSelect#update:selectedContacts
       * @type Contact[]
       */
      const selectedContacts = [...this.selectedContacts] as Contact[]
      selectedContacts.splice(contactIndex, 1)
      this.$emit('update:selectedContacts', selectedContacts)
    }
  }

  /**
   * returns all contacts except the ones that have already been selected
   *
   * @return {Contact[]} an array of contacts
   */
  get allContactsExceptSelected (): Contact[] {
    return this.contacts.filter(c => !this.selectedContacts.find(rc => rc.id === c.id))
  }
}
</script>

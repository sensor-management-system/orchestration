<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="apply"
          :to="'/contacts/' + contactId"
          @save="save"
        />
      </v-card-actions>
      <ContactBasicDataForm
        v-if="contactCopy"
        ref="basicForm"
        v-model="contactCopy"
        :readonly="false"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          save-btn-text="apply"
          :to="'/contacts/' + contactId"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, mixins, Vue, Watch } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'

import { SetTitleAction } from '@/store/appbar'
import { ContactsState, LoadContactAction, SaveContactAction } from '@/store/contacts'

import { Contact } from '@/models/Contact'

import ContactBasicDataForm from '@/components/ContactBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

@Component({
  components: {
    SaveAndCancelButtons,
    ContactBasicDataForm
  },
  middleware: ['auth'],
  computed: mapState('contacts', ['contact']),
  methods: {
    ...mapActions('contacts', ['saveContact', 'loadContact']),
    ...mapActions('appbar', ['setTitle']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ContactEditPage extends mixins(CheckEditAccess) {
  private contactCopy: Contact = new Contact()

  // vuex definition for typescript check
  contact!: ContactsState['contact']
  saveContact!: SaveContactAction
  loadContact!: LoadContactAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/contacts/' + this.contactId
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this contact.'
  }

  created () {
    if (this.contact) {
      this.contactCopy = Contact.createFromObject(this.contact)
    }
  }

  get contactId () {
    return this.$route.params.contactId
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      await this.saveContact(this.contactCopy)
      this.loadContact(this.contactId)
      this.$router.push('/contacts/' + this.contactId)
    } catch (e: any) {
      const msg = new ErrorMessageDispatcher()
        .forCase({
          // 409 is a conflict
          status: 409,
          // and a message with mail as source of the error points
          // to our unique constraint
          predicate: sourceLowerCaseIncludes('mail'),
          text: 'User with E-mail exists already'
        })
        .defaultText('Saving of contact failed')
        .dispatch(e)

      this.$store.commit('snackbar/setError', msg)
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('contact', {
    immediate: true,
    deep: true
  })
  onContactChanged (value: Contact | null) {
    if (value) {
      this.contactCopy = Contact.createFromObject(value)
    }
  }
}
</script>

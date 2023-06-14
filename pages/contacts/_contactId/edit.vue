<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
    />
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
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

@Component({
  components: {
    SaveAndCancelButtons,
    ContactBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('contacts', ['contact']),
  methods: {
    ...mapActions('contacts', ['saveContact', 'loadContact']),
    ...mapActions('appbar', ['setTitle'])
  }
})
export default class ContactEditPage extends mixins(CheckEditAccess) {
  private isLoading: boolean = false
  private contactCopy: Contact = new Contact()

  // vuex definition for typescript check
  contact!: ContactsState['contact']
  saveContact!: SaveContactAction
  loadContact!: LoadContactAction
  setTitle!: SetTitleAction

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
      this.isLoading = true
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
      this.isLoading = false
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

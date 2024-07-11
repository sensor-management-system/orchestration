<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="redirect ? redirect : '/contacts'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <ContactBasicDataForm
        ref="basicForm"
        v-model="contact"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="redirect ? redirect : '/contacts'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import { mapActions } from 'vuex'

import { SetDefaultsAction, SetTitleAction, SetShowBackButtonAction } from '@/store/appbar'
import { SaveContactAction } from '@/store/contacts'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

import ContactBasicDataForm from '@/components/ContactBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

@Component({
  components: {
    SaveAndCancelButtons,
    ContactBasicDataForm
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('contacts', ['saveContact']),
    ...mapActions('appbar', ['setDefaults', 'setTitle', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ContactNewPage extends mixins(Rules) {
  private contact: Contact = new Contact()

  private redirect: string = ''

  // vuex definition for typescript check
  initContactsNewAppBar!: () => void
  saveContact!: SaveContactAction
  setDefaults!: SetDefaultsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  created () {
    /** this page accepts the query parameter 'redirect' as a html encoded URI
      * and sends the user back to this page after a new contact has been created.
      * it is currently used in /devices/contacts/new and /platforms/contacts/new
      * it also checks if the redirect starts with http to prevent linking to external pages
    */
    const backLink = this.$route.query.redirect as string
    if (backLink && !backLink.startsWith('http')) {
      this.redirect = backLink
    }
    this.initializeAppBar()
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTitle('New Contact')
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    const redirect: string | (string | null)[] = this.$route.query.redirect

    try {
      this.setLoading(true)
      const savedContact = await this.saveContact(this.contact)
      this.$store.commit('snackbar/setSuccess', 'Contact created')
      // sends the user back to the previous contact creation page
      if (redirect && savedContact.id) {
        this.$router.push(redirect + '?contact=' + encodeURI(savedContact.id))
      } else {
        this.$router.push('/contacts/' + savedContact.id)
      }
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
        .defaultText('Creation of contact failed')
        .dispatch(e)
      this.$store.commit('snackbar/setError', msg)
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

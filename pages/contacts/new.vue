<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/contacts"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
      <ContactBasicDataForm
        ref="basicForm"
        v-model="contact"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          to="/contacts"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

import ContactBasicDataForm from '@/components/ContactBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ContactBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth']
})
export default class ContactNewPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private contact: Contact = new Contact()
  private isLoading: boolean = false

  mounted () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  onSaveButtonClicked (): void {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    if (!this.$auth.loggedIn) {
      this.$store.commit('snackbar/setError', 'You need to be logged in to save the contact')
      return
    }
    this.isLoading = true
    this.$api.contacts.save(this.contact).then((savedContact) => {
      this.isLoading = false
      this.$store.commit('snackbar/setSuccess', 'Contact created')
      this.$router.push('/contacts/' + savedContact.id + '')
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      title: 'Add Contact'
    })
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

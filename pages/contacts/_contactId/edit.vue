<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
        <v-btn
          v-if="$auth.loggedIn"
          small
          nuxt
          :to="'/contacts/' + contactId"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          apply
        </v-btn>
      </v-card-actions>
      <ContactBasicDataForm
        v-if="formContact"
        ref="basicForm"
        v-model="formContact"
        :readonly="false"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          nuxt
          :to="'/contacts/' + contactId"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          apply
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'



import ContactBasicDataForm from '@/components/ContactBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions, mapState } from 'vuex'

@Component({
  components: {
    ContactBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed:mapState('contacts',['contact']),
  methods:mapActions('contacts',['updateContact','saveContact'])
})
export default class ContactEditPage extends Vue {
  private isLoading: boolean = false

  get formContact(){
    if(this.contact){
      return this.contact;
    }
    return new Contact()
  }
  set formContact(val){
    this.updateContact(val);
  }

  onSaveButtonClicked () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    this.isLoading = true
    this.save().then((contact) => {
      this.isLoading = false
      this.$emit('input', contact)
      this.$router.push('/contacts/' + this.contactId)
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Saving of contact failed')
    })
  }

  save (): Promise<Contact> {
    return new Promise((resolve, reject) => {
      this.saveContact(this.formContact).then((savedContact) => {
        resolve(savedContact)
      }).catch((_error) => {
        reject(_error)
      })
    })
  }

  get contactId () {
    return this.$route.params.contactId
  }

  // @Watch('value', { immediate: true, deep: true })
  // // @ts-ignore
  // onContactChanged (val: Contact) {
  //   if (val.id) {
  //     this.$store.commit('appbar/setTitle', val?.toString() || 'Edit contact')
  //   }
  //   this.contactCopy = Contact.createFromObject(val)
  // }
}
</script>

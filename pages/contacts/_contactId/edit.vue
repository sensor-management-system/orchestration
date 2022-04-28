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
        <SaveAndCancelButtons
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
          save-btn-text="apply"
          :to="'/contacts/' + contactId"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, Vue} from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import ContactBasicDataForm from '@/components/ContactBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions, mapState } from 'vuex'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    ContactBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed:mapState('contacts',['contact']),
  methods:{
    ...mapActions('contacts',['saveContact','loadContact']),
    ...mapActions('appbar',['initContactsContactIdEditAppBar'])
  }
})
export default class ContactEditPage extends Vue {
  private isLoading: boolean = false
  private contactCopy: Contact = new Contact()

  created(){
    this.initContactsContactIdEditAppBar(this.contact.toString())
    this.contactCopy = Contact.createFromObject(this.contact)
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
      const updatedContact = await this.saveContact(this.contactCopy)
      this.loadContact(this.contactId)
      this.$router.push('/contacts/' + this.contactId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Saving of contact failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>

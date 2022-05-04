<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <contact-role-form
      :existing-contact-roles="value"
      :contacts="allContacts"
      :cv-contact-roles="allContactRoles"
      :cancel-to="'/platforms/' + platformId + '/contacts'"
      :editable="$auth.loggedIn"
      @add-contact="addContact"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { CvContactRole } from '@/models/CvContactRole'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ContactRoleForm from '@/components/contacts/ContactRoleForm.vue'

@Component({
  components: {
    ContactRoleForm,
    ProgressIndicator
  },
  middleware: ['auth']
})
export default class PlatformAddContactPage extends Vue {
  @Prop({
    type: Array,
    required: false,
    default: () => [] as ContactRole[]
  })
  // existing contact roles
  private readonly value!: ContactRole[]

  private allContacts: Contact[] = []
  private allContactRoles: CvContactRole[] = []

  private isLoading: boolean = false
  private isSaving: boolean = false

  async fetch () {
    try {
      this.isLoading = true
      // We can run both queries in parallel.
      // And the page currently handles the server interaction
      // (and not the form component).
      const allContactsPromise = this.$api.contacts.findAll()
      const allContactRolesPromise = this.$api.cvContactRoles.findAll()
      this.allContacts = await allContactsPromise
      this.allContactRoles = await allContactRolesPromise
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contact information')
    } finally {
      this.isLoading = false
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async addContact (newContactRole: ContactRole) {
    if (this.$auth.loggedIn) {
      this.isSaving = true
      try {
        const newContactRoleId = await this.$api.platforms.addContact(this.platformId, newContactRole)
        // the current one has no id so far, so we will set it here
        newContactRole.id = newContactRoleId
        const result = [...this.value, newContactRole]
        this.$emit('input', result)
        this.$router.push('/platforms/' + this.platformId + '/contacts')
      } catch (_error) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.isSaving = false
      }
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }
}
</script>

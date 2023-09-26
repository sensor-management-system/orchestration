<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <contact-role-assignment-form
      :contacts="contacts"
      :contact="selectedContact"
      :cv-contact-roles="cvContactRoles"
      :existing-contact-roles="platformContactRoles"
      @cancel="$router.push('/platforms/' + platformId + '/contacts')"
      @input="assignContact"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ContactsState, LoadAllContactsAction } from '@/store/contacts'
import {
  PlatformsState,
  LoadPlatformContactRolesAction,
  AddPlatformContactRoleAction
} from '@/store/platforms'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import ContactRoleAssignmentForm from '@/components/shared/ContactRoleAssignmentForm.vue'

@Component({
  components: {
    ContactRoleAssignmentForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('platforms', ['platformContactRoles']),
    ...mapState('contacts', ['contacts']),
    ...mapState('vocabulary', ['cvContactRoles']),
    ...mapState('progressindicator', ['isLoading'])

  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('platforms', ['loadPlatformContactRoles', 'addPlatformContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformAddContactPage extends mixins(CheckEditAccess) {
  private selectedContact: Contact | null = null

  // vuex definition for typescript check
  platformContactRoles!: PlatformsState['platformContactRoles']
  contacts!: ContactsState['contacts']
  loadAllContacts!: LoadAllContactsAction
  loadPlatformContactRoles!: LoadPlatformContactRolesAction
  addPlatformContactRole!: AddPlatformContactRoleAction
  loadCvContactRoles!: LoadCvContactRolesAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/contacts'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadAllContacts()

      const redirectContactId = this.$route.query.contact
      if (redirectContactId) {
        this.selectedContact = this.contacts.find(contact => contact.id === redirectContactId) as Contact
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  async assignContact (contactRole: ContactRole | null) {
    if (this.editable && contactRole) {
      try {
        this.setLoading(true)
        await this.addPlatformContactRole({
          platformId: this.platformId,
          contactRole
        })
        this.loadPlatformContactRoles(this.platformId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/platforms/' + this.platformId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.setLoading(false)
      }
    }
  }
}
</script>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <contact-role-assignment-form
      :contacts="contacts"
      :contact="selectedContact"
      :cv-contact-roles="cvContactRoles"
      :existing-contact-roles="siteContactRoles"
      @cancel="$router.push('/sites/' + siteId + '/contacts')"
      @input="assignContact"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ContactsState, LoadAllContactsAction } from '@/store/contacts'
import { LoadSiteContactRolesAction, AddSiteContactRoleAction, SitesState } from '@/store/sites'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ContactRoleAssignmentForm from '@/components/shared/ContactRoleAssignmentForm.vue'

@Component({
  components: {
    ProgressIndicator,
    ContactRoleAssignmentForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('sites', ['siteContactRoles']),
    ...mapState('contacts', ['contacts']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('sites', ['loadSiteContactRoles', 'addSiteContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles'])
  }
})
export default class SiteAssignContactPage extends mixins(CheckEditAccess) {
  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  // vuex definition for typescript check
  siteContactRoles!: SitesState['siteContactRoles']
  contacts!: ContactsState['contacts']
  loadSiteContactRoles!: LoadSiteContactRolesAction
  addSiteContactRole!: AddSiteContactRoleAction
  loadAllContacts!: LoadAllContactsAction
  loadCvContactRoles!: LoadCvContactRolesAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/sites/' + this.siteId + '/contacts'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this site.'
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await this.loadAllContacts()

      const redirectContactId = this.$route.query.contact
      if (redirectContactId) {
        this.selectedContact = this.contacts.find(contact => contact.id === redirectContactId) as Contact
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
    } finally {
      this.isLoading = false
    }
  }

  get siteId (): string {
    return this.$route.params.siteId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async assignContact (contactRole: ContactRole | null) {
    if (this.editable && contactRole) {
      try {
        this.isSaving = true
        await this.addSiteContactRole({
          siteId: this.siteId,
          contactRole
        })
        this.loadSiteContactRoles(this.siteId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/sites/' + this.siteId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.isSaving = false
      }
    }
  }
}
</script>

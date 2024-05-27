<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import ContactRoleAssignmentForm from '@/components/shared/ContactRoleAssignmentForm.vue'

@Component({
  components: {
    ContactRoleAssignmentForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('sites', ['siteContactRoles']),
    ...mapState('contacts', ['contacts']),
    ...mapState('vocabulary', ['cvContactRoles']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('sites', ['loadSiteContactRoles', 'addSiteContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteAssignContactPage extends mixins(CheckEditAccess) {
  private selectedContact: Contact | null = null

  // vuex definition for typescript check
  siteContactRoles!: SitesState['siteContactRoles']
  contacts!: ContactsState['contacts']
  loadSiteContactRoles!: LoadSiteContactRolesAction
  addSiteContactRole!: AddSiteContactRoleAction
  loadAllContacts!: LoadAllContactsAction
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
    return 'You\'re not allowed to edit this site / lab.'
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

  get siteId (): string {
    return this.$route.params.siteId
  }

  async assignContact (contactRole: ContactRole | null) {
    if (this.editable && contactRole) {
      try {
        this.setLoading(true)
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
        this.setLoading(false)
      }
    }
  }
}
</script>

<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <contact-role-assignment-form
      :contacts="contacts"
      :contact="selectedContact"
      :cv-contact-roles="cvContactRoles"
      :existing-contact-roles="deviceContactRoles"
      @cancel="$router.push('/devices/' + deviceId + '/contacts')"
      @input="assignContact"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ContactsState, LoadAllContactsAction } from '@/store/contacts'
import { LoadDeviceContactRolesAction, AddDeviceContactRoleAction, DevicesState } from '@/store/devices'
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
    ...mapState('devices', ['deviceContactRoles']),
    ...mapState('contacts', ['contacts']),
    ...mapState('vocabulary', ['cvContactRoles']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('devices', ['loadDeviceContactRoles', 'addDeviceContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceAssignContactPage extends mixins(CheckEditAccess) {
  private selectedContact: Contact | null = null

  // vuex definition for typescript check
  deviceContactRoles!: DevicesState['deviceContactRoles']
  contacts!: ContactsState['contacts']
  loadDeviceContactRoles!: LoadDeviceContactRolesAction
  addDeviceContactRole!: AddDeviceContactRoleAction
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
    return '/devices/' + this.deviceId + '/contacts'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
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

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async assignContact (contactRole: ContactRole | null) {
    if (this.editable && contactRole) {
      try {
        this.setLoading(true)
        await this.addDeviceContactRole({
          deviceId: this.deviceId,
          contactRole
        })
        this.loadDeviceContactRoles(this.deviceId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/devices/' + this.deviceId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.setLoading(false)
      }
    }
  }
}
</script>

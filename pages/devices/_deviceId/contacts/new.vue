<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-form ref="contactRoleForm" @submit.prevent>
      <v-row>
        <v-col
          cols="12"
          md="5"
        >
          <v-autocomplete
            ref="assignContactSelection"
            v-model="selectedContact"
            :items="contacts"
            :item-text="(x) => x"
            :item-value="(x) => x.id"
            label="Assign contact"
            return-object
            @change="validateForm"
          />
        </v-col>
        <v-col
          cols="12"
          md="5"
        >
          <v-autocomplete
            ref="assignRoleSelection"
            v-model="selectedRole"
            :items="cvContactRoles"
            :item-text="(x) => x"
            :item-value="(x) => x.id"
            label="Assign role"
            return-object
            :rules="[roleAndContactNotDuplicated]"
          />
        </v-col>
        <v-col
          cols="12"
          md="2"
          align-self="center"
        >
          <v-btn
            v-if="editable"
            small
            color="primary"
            :disabled="assignButtonDisabled"
            @click="assignContact"
          >
            Assign
          </v-btn>
          <v-btn
            small
            text
            nuxt
            :to="'/devices/' + deviceId + '/contacts'"
          >
            Cancel
          </v-btn>
        </v-col>
        <v-col align-self="center" class="text-right">
          <v-btn
            small
            nuxt
            color="accent"
            :to="'/contacts/new?redirect=' + redirectUrl"
          >
            New Contact
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { ContactsState } from '@/store/contacts'
import { LoadDeviceContactRolesAction, AddDeviceContactRoleAction, DevicesState } from '@/store/devices'
import { LoadCvContactRolesAction } from '@/store/vocabulary'

import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { CvContactRole } from '@/models/CvContactRole'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceContactRoles']),
    ...mapState('contacts', ['contacts']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('devices', ['loadDeviceContactRoles', 'addDeviceContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles'])
  }
})
export default class DeviceAssignContactPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private selectedContact: Contact | null = null
  private selectedRole: CvContactRole | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  // vuex definition for typescript check
  deviceContactRoles!: DevicesState['deviceContactRoles']
  contacts!: ContactsState['contacts']
  loadDeviceContactRoles!: LoadDeviceContactRolesAction
  addDeviceContactRole!: AddDeviceContactRoleAction
  loadAllContacts!: () => void
  loadCvContactRoles!: LoadCvContactRolesAction

  created () {
    if (!this.editable) {
      this.$router.replace('/devices/' + this.deviceId + '/contacts', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this device.')
      })
    }
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await Promise.all([
        // TODO: Check if we should remove it here as it is also loaded in the other component
        this.loadAllContacts(),
        this.loadCvContactRoles(),
        this.loadDeviceContactRoles(this.deviceId)
      ])

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

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get assignButtonDisabled (): boolean {
    return this.selectedContact == null || this.selectedRole == null
  }

  roleAndContactNotDuplicated (selectedRole: CvContactRole | null): boolean | string {
    if (this.selectedContact == null || selectedRole == null) {
      // if one of them are null, we don't need to validate further (the button is just disabled)
      return true
    }
    const found = this.deviceContactRoles.find(existingContact => existingContact?.contact?.id === this.selectedContact?.id && existingContact.roleUri === selectedRole.uri)
    if (!found) {
      return true
    }
    return this.selectedContact.toString() + ' is already deposited as ' + selectedRole.name
  }

  /**
   * the current URL is used to redirect the user back to this page after creating a new contact
   */
  get redirectUrl (): string {
    return encodeURI(this.$route.path)
  }

  validateForm (): boolean {
    return (this.$refs.contactRoleForm as Vue & { validate: () => boolean }).validate()
  }

  async assignContact () {
    if (this.editable && this.selectedContact && this.selectedRole) {
      if (!this.validateForm()) {
        this.$store.commit('snackbar/setError', 'Please correct your input')
        return
      }
      try {
        this.isSaving = true
        await this.addDeviceContactRole({
          deviceId: this.deviceId,
          contactRole: ContactRole.createFromObject({
            id: null,
            contact: this.selectedContact,
            roleName: this.selectedRole.name,
            roleUri: this.selectedRole.uri
          })
        })
        this.loadDeviceContactRoles(this.deviceId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/devices/' + this.deviceId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.isSaving = false
      }
    }
  }
}
</script>

<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
    <v-row>
      <v-col
        cols="12"
        md="5"
      >
        <v-autocomplete
          ref="assignContactSelection"
          v-model="selectedContact"
          :items="allExceptSelected"
          :item-text="(x) => x"
          :item-value="(x) => x.id"
          label="Assign contact"
          return-object
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
          :disabled="selectedContact == null"
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
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadDeviceContactsAction, AddDeviceContactAction, DevicesState } from '@/store/devices'

import { Contact } from '@/models/Contact'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('contacts', ['contactsByDifference']),
    ...mapState('devices', ['deviceContacts'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('devices', ['loadDeviceContacts', 'addDeviceContact'])
  }
})
export default class DeviceAssignContactPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  // vuex definition for typescript check
  deviceContacts!: DevicesState['deviceContacts']
  loadDeviceContacts!: LoadDeviceContactsAction
  addDeviceContact!: AddDeviceContactAction
  loadAllContacts!: () => void
  contactsByDifference!: (contactsToSubtract: Contact[]) => Contact[]

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
        this.loadAllContacts(),
        this.loadDeviceContacts(this.deviceId)
      ])

      const redirectContactId = this.$route.query.contact
      if (redirectContactId) {
        this.selectedContact = this.allExceptSelected.find(contact => contact.id === redirectContactId) as Contact
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

  get allExceptSelected (): Contact[] {
    return this.contactsByDifference(this.deviceContacts)
  }

  /**
   * the current URL is used to redirect the user back to this page after creating a new contact
   */
  get redirectUrl (): string {
    return encodeURI(this.$route.path)
  }

  async assignContact () {
    if (this.selectedContact && this.selectedContact.id && this.$auth.loggedIn) {
      try {
        this.isSaving = true
        await this.addDeviceContact({
          deviceId: this.deviceId,
          contactId: this.selectedContact.id
        })
        this.loadDeviceContacts(this.deviceId)
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

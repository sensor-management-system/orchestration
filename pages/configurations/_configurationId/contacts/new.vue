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
    <contact-role-assignment-form
      :contacts="contacts"
      :contact="selectedContact"
      :cv-contact-roles="cvContactRoles"
      :existing-contact-roles="configurationContactRoles"
      @cancel="$router.push('/configurations/' + configurationId + '/contacts')"
      @input="assignContact"
    />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue, Watch } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'

import { LoadConfigurationContactRolesAction, AddConfigurationContactRoleAction, ConfigurationsState } from '@/store/configurations'
import { ContactsState, LoadAllContactsAction } from '@/store/contacts'
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
    ...mapState('contacts', ['contacts']),
    ...mapState('configurations', ['configurationContactRoles']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('configurations', ['loadConfigurationContactRoles', 'addConfigurationContactRole']),
    ...mapActions('vocabulary', ['loadCvContactRoles'])
  }
})
export default class ConfigurationAssignContactPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  // vuex definition for typescript check
  configurationContactRoles!: ConfigurationsState['configurationContactRoles']
  contacts!: ContactsState['contacts']
  loadConfigurationContactRoles!: LoadConfigurationContactRolesAction
  loadAllContacts!: LoadAllContactsAction
  loadCvContactRoles!: LoadCvContactRolesAction
  addConfigurationContactRole!: AddConfigurationContactRoleAction

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

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async assignContact (contactRole: ContactRole | null) {
    if (this.editable && contactRole) {
      try {
        this.isSaving = true
        await this.addConfigurationContactRole({
          configurationId: this.configurationId,
          contactRole
        })
        this.loadConfigurationContactRoles(this.configurationId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/configurations/' + this.configurationId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.isSaving = false
      }
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/configurations/' + this.configurationId + '/contacts', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }
}
</script>

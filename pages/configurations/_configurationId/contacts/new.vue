<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
          :items="allExceptSelected"
          :item-text="(x) => x"
          :item-value="(x) => x.id"
          label="New contact"
          @change="select"
        />
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
      >
        <v-btn
          v-if="$auth.loggedIn"
          small
          color="primary"
          :disabled="selectedContact == null"
          @click="addContact"
        >
          Add
        </v-btn>
        <v-btn
          small
          text
          nuxt
          :to="'/configurations/' + configurationId + '/contacts'"
        >
          Cancel
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Contact } from '@/models/Contact'

@Component({
  components: { ProgressIndicator },
  middleware: ['auth']
})
export default class PlatformAddContactPage extends Vue {
  private alreadyUsedContacts: Contact[] = []
  private allContacts: Contact[] = []
  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  @Prop({
    default: () => [] as Contact[],
    required: true,
    type: Array
  })
  readonly value!: Contact[]

  created () {
    this.alreadyUsedContacts = [...this.value] as Contact[]
  }

  mounted () {
    this.isLoading = true
    this.$api.contacts.findAll().then((foundContacts) => {
      this.allContacts = foundContacts
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
    }).finally(() => {
      this.isLoading = false
    })
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get allExceptSelected (): Contact[] {
    return this.allContacts.filter(c => !this.alreadyUsedContacts.find(rc => rc.id === c.id))
  }

  select (newContactId: string): void {
    const idx = this.allContacts.findIndex((c: Contact) => c.id === newContactId)
    if (idx > -1) {
      this.selectedContact = this.allContacts[idx]
    } else {
      this.selectedContact = null
    }
  }

  addContact () {
    if (this.selectedContact && this.selectedContact.id && this.$auth.loggedIn) {
      this.isSaving = true
      this.$store.dispatch('contacts/addContactToConfiguration', {
        configurationId: this.configurationId,
        contactId: this.selectedContact.id
      }).then(() => {
        this.$router.push('/configurations/' + this.configurationId + '/contacts')
      }).catch(() => {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      }).finally(() => {
        this.isSaving = false
      })
    }
  }
}
</script>

<style scoped>

</style>

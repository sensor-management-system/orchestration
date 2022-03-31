<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
    <v-row>
      <v-col
        cols="12"
        md="5"
      >
        <v-autocomplete :items="allExceptSelected" :item-text="(x) => x" :item-value="(x) => x.id" label="New contact" @change="select" />
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
          :to="'/platforms/' + platformId + '/contacts'"
        >
          Cancel
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  },
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
      this.isLoading = false
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
      this.isLoading = false
    })
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  addContact (): void {
    if (this.selectedContact && this.selectedContact.id && this.$auth.loggedIn) {
      this.isSaving = true
      this.$api.platforms.addContact(this.platformId, this.selectedContact.id).then(() => {
        this.isSaving = false
        this.alreadyUsedContacts.push(this.selectedContact as Contact)
        this.$emit('input', this.alreadyUsedContacts)
        this.$router.push('/platforms/' + this.platformId + '/contacts')
      }).catch(() => {
        this.isSaving = false
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      })
    }
  }

  select (newContactId: string): void {
    const idx = this.allContacts.findIndex((c: Contact) => c.id === newContactId)
    if (idx > -1) {
      this.selectedContact = this.allContacts[idx]
    } else {
      this.selectedContact = null
    }
  }

  get allExceptSelected (): Contact[] {
    return this.allContacts.filter(c => !this.alreadyUsedContacts.find(rc => rc.id === c.id))
  }

  get platformId (): string {
    return this.$route.params.platformId
  }
}
</script>

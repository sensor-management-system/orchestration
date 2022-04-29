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
        <v-autocomplete
          :items="allExceptSelected"
          :item-text="(x) => x"
          label="New contact"
          v-model="selectedContact"
          return-object
        />
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
      >
        <v-btn
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

import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Contact } from '@/models/Contact'
import { mapActions, mapGetters, mapState } from 'vuex'

@Component({
  components: {
    ProgressIndicator
  },
  middleware: ['auth'],
  computed:{
    ...mapGetters('contacts',['contactsByDifference']),
    ...mapState('platforms',['platformContacts'])
  },
  methods:{
    ...mapActions('contacts',['loadAllContacts']),
    ...mapActions('platforms',['loadPlatformContacts','addPlatformContact'])
  }
})
export default class PlatformAddContactPage extends Vue {
  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  async created () {
    try {
      this.isLoading=true
      await this.loadAllContacts()
      await this.loadPlatformContacts(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
    } finally {
      this.isLoading = false
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get allExceptSelected (): Contact[] {
    return this.contactsByDifference(this.platformContacts);
  }

  async addContact (): void {
    if (this.selectedContact && this.selectedContact.id) {
      try {
        this.isSaving = true
        await this.addPlatformContact({
          platformId: this.platformId,
          contactId: this.selectedContact.id
        })
        this.loadPlatformContacts(this.platformId)
        this.$store.commit('snackbar/setSuccess', 'New Contact added')
        this.$router.push('/platforms/' + this.platformId + '/contacts')
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      } finally {
        this.isSaving = false
      }
    }
  }
}
</script>

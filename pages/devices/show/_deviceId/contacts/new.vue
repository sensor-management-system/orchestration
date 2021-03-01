<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
    <v-row>
      <v-col cols="3">
        <v-autocomplete :items="allExceptSelected" :item-text="(x) => x" :item-value="(x) => x.id" label="New contact" @change="select" />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn :disabled="selectedContact == null" @click="addContact">
          Add
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

@Component({
  components: {
  }
})
export default class DeviceAddContactPage extends Vue {
  private alreadyUsedContacts: Contact[] = []
  private allContacts: Contact[] = []
  private selectedContact: Contact | null = null

  mounted () {
    this.$api.devices.findRelatedContacts(this.deviceId).then((foundContacts) => {
      this.alreadyUsedContacts = foundContacts
    })
    this.$api.contacts.findAll().then((foundContacts) => {
      this.allContacts = foundContacts
    })
  }

  addContact () {
    if (this.selectedContact && this.selectedContact.id) {
      this.$api.devices.addContact(this.deviceId, this.selectedContact.id).then(() => {
        this.$router.push('/devices/show/' + this.deviceId + '/contacts')
      })
    }
  }

  select (newContactId: string) {
    const idx = this.allContacts.findIndex((c: Contact) => c.id === newContactId)
    if (idx > -1) {
      this.selectedContact = this.allContacts[idx]
    } else {
      this.selectedContact = null
    }
  }

  get allExceptSelected () {
    return this.allContacts.filter(c => !this.alreadyUsedContacts.find(rc => rc.id === c.id))
  }

  get deviceId () {
    return this.$route.params.deviceId
  }
}
</script>

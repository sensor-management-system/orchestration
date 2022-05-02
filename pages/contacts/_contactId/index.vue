<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="$auth.loggedIn"
        >
          <template #actions>
            <DotMenuActionDelete
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
      <ContactBasicData
        v-if="contact"
        v-model="contact"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="$auth.loggedIn"
        >
          <template #actions>
            <DotMenuActionDelete
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
      <ContacsDeleteDialog
        v-model="showDeleteDialog"
        :contact-to-delete="contact"
        @cancel-deletion="closeDialog"
        @submit-deletion="deleteAndCloseDialog"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { mapActions, mapState } from 'vuex'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContactBasicData from '@/components/ContactBasicData.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'

@Component({
  components: { ContacsDeleteDialog, ContactBasicData, DotMenuActionDelete, DotMenu },
  computed: mapState('contacts', ['contact']),
  methods: {
    ...mapActions('contacts', ['deleteContact']),
    ...mapActions('appbar', ['initContactsContactIdIndexAppBar'])
  }
})
export default class ContactIndexPage extends Vue {
  showDeleteDialog = false

  created () {
    this.initContactsContactIdIndexAppBar(this.contact)
  }

  get contactId () {
    return this.$route.params.contactId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    this.closeDialog()

    if (this.contact === null) {
      return
    }
    try {
      await this.deleteContact(this.contact.id)
      this.$router.push('/contacts')
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    }
  }
}
</script>

<style scoped>

</style>

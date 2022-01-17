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
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-card flat>
      <div v-if="isEditPage">
        <NuxtChild
          v-model="contact"
        />
      </div>
      <div v-else>
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
      </div>
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
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import ContactBasicData from '@/components/ContactBasicData.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'

@Component({
  components: {
    ContacsDeleteDialog,
    DotMenuActionDelete,
    DotMenu,
    ContactBasicData,
    ProgressIndicator
  }
})
export default class ContactShowPage extends Vue {
  private contact: Contact = new Contact()
  private isLoading: boolean = true

  private showDeleteDialog: boolean=false;

  created () {
    this.initializeAppBar()
  }

  mounted () {
    this.$api.contacts.findById(this.contactId).then((contact) => {
      this.contact = contact
      this.isLoading = false
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Loading contact failed')
      this.isLoading = false
    })
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      title: 'Show Contact'
    })
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

  deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.contact === null) {
      return
    }

    this.$api.contacts.deleteById(this.contact.id!).then(() => {
      this.$router.push('/contacts')
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    })
  }

  @Watch('contact', { immediate: true, deep: true })
  // @ts-ignore
  onContactChanged (val: Contact) {
    const fallbackText = this.isEditPage ? 'Edit contact' : 'Show contact'
    if (val.id) {
      this.$store.commit('appbar/setTitle', val?.toString() || fallbackText)
    }
  }

  get isEditPage () {
    return this.$route.path === '/contacts/' + this.contactId + '/edit' || this.$route.path === '/contact/' + this.contactId + '/edit/'
  }
}
</script>

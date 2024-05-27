<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <center>
        <v-alert
          v-if="contact && ! editable"
          type="info"
          color="blue"
          colored-border
          border="left"
          elevation="2"
        >
          You are not allowed to edit contact data of other users.
        </v-alert>
      </center>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="deletable"
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
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="deletable"
        >
          <template #actions>
            <DotMenuActionDelete
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
      <DeleteDialog
        v-model="showDeleteDialog"
        title="Delete Contact"
        :disabled="isLoading"
        @cancel="closeDialog"
        @delete="deleteAndCloseDialog"
      >
        Do you really want to delete the contact <em>{{ contact.fullName }}</em>?
      </DeleteDialog>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'

import { ContactsState, LoadContactAction, DeleteContactAction } from '@/store/contacts'

import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContactBasicData from '@/components/ContactBasicData.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  components: {
    DeleteDialog,
    ContactBasicData,
    DotMenuActionDelete,
    DotMenu
  },
  computed: {
    ...mapState('contacts', ['contact']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('contacts', ['deleteContact', 'loadContact']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ContactIndexPage extends Vue {
  @InjectReactive()
    editable!: boolean

  @InjectReactive()
    deletable!: boolean

  showDeleteDialog = false

  // vuex definition for typescript check
  contact!: ContactsState['contact']
  deleteContact!: DeleteContactAction
  loadContact!: LoadContactAction
  setLoading!: SetLoadingAction

  async created () {
    // We load the contact in the upper context (that component that
    // include this page here is a child)
    // However, we can't be sure that this was already loaded
    // so we need to load it here in order to show the right name
    this.setLoading(true)
    await this.loadContact(this.contactId)
    this.setLoading(false)
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
    if (this.contact === null || this.contact.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteContact(this.contact.id)
      this.$router.push('/contacts')
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>

<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
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
        >
          <template #append-outer>
            <v-tooltip
              v-if="selectedRole?.definition"
              right
            >
              <template #activator="{ on, attrs }">
                <v-icon
                  color="primary"
                  small
                  v-bind="attrs"
                  v-on="on"
                >
                  mdi-help-circle-outline
                </v-icon>
              </template>
              <span>{{ selectedRole.definition }}</span>
            </v-tooltip>
            <v-btn icon @click="showNewContactRoleDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
          <template #item="data">
            <template v-if="(typeof data.item) !== 'object'">
              <v-list-item-content>{{ data.item }}</v-list-item-content>
            </template>
            <template v-else>
              <v-list-item-content>
                <v-list-item-title>
                  {{ data.item.name }}
                  <v-tooltip
                    v-if="data.item.definition"
                    bottom
                  >
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="primary"
                        small
                        v-bind="attrs"
                        v-on="on"
                      >
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>{{ data.item.definition }}</span>
                  </v-tooltip>
                </v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
      >
        <v-btn
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
          @click="$emit('cancel')"
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
    <contact-role-dialog
      v-model="showNewContactRoleDialog"
      :initial-term="selectedRole ? selectedRole.name : null"
      @aftersubmit="updateRole"
    />
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import ContactRoleDialog from '@/components/shared/ContactRoleDialog.vue'

import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { CvContactRole } from '@/models/CvContactRole'

@Component({
  components: {
    ContactRoleDialog
  }
})
export default class ContactRoleAssignmentForm extends Vue {
  private selectedContact: Contact | null = null
  private selectedRole: CvContactRole | null = null
  private showNewContactRoleDialog = false

  @Prop({
    default: () => [] as Contact[],
    required: false,
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: () => null,
    required: false,
    type: Object
  })
  readonly contact!: Contact | null

  @Prop({
    default: () => [] as CvContactRole[],
    required: false,
    type: Array
  })
  readonly cvContactRoles!: CvContactRole[]

  @Prop({
    default: () => [] as ContactRole[],
    required: false,
    type: Array
  })
  readonly existingContactRoles!: ContactRole[]

  created () {
    if (this.contact) {
      this.selectedContact = this.contact
    }
  }

  updateRole (contactRole: CvContactRole) {
    this.selectedRole = contactRole
  }

  /**
   * the current URL is used to redirect the user back to this page after creating a new contact
   */
  get redirectUrl (): string {
    return encodeURI(this.$route.path)
  }

  roleAndContactNotDuplicated (selectedRole: CvContactRole | null): boolean | string {
    if (this.selectedContact == null || selectedRole == null) {
      return true
    }
    const found = this.existingContactRoles.find(existingContact => existingContact?.contact?.id === this.selectedContact?.id && existingContact.roleUri === selectedRole.uri)
    if (!found) {
      return true
    }
    return this.selectedContact.toString() + ' is already on file as a ' + selectedRole.name
  }

  formIsValid (): boolean {
    return !(this.selectedContact == null || this.selectedRole == null || typeof this.roleAndContactNotDuplicated(this.selectedRole) === 'string')
  }

  get assignButtonDisabled (): boolean {
    return !this.formIsValid()
  }

  validateForm (): boolean {
    return (this.$refs.contactRoleForm as Vue & { validate: () => boolean }).validate()
  }

  assignContact () {
    if (this.selectedContact && this.selectedRole) {
      if (!this.validateForm()) {
        this.$store.commit('snackbar/setError', 'Please correct your input')
        return
      }
      this.$emit('input', ContactRole.createFromObject({
        id: null,
        contact: this.selectedContact,
        roleName: this.selectedRole.name,
        roleUri: this.selectedRole.uri
      }))
    }
  }

  @Watch('contact', {
    immediate: true
  })
  onContactChanged (value: Contact | null) {
    this.selectedContact = value
  }
}
</script>

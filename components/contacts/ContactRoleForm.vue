<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
  <v-form ref="contactRoleForm" class="pb-4" @submit.prevent>
    <v-row>
      <v-col
        cols="12"
        md="5"
      >
        <v-autocomplete v-model="selectedContact" :items="contacts" :item-text="(x) => x" label="Contact" @change="validateForm" />
      </v-col>
      <v-col cols="12" md="4">
        <v-autocomplete v-model="selectedRole" :items="cvContactRoles" :item-text="(x) => x" label="Role" :rules="[roleAndContactNotDuplicated]" />
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
          :disabled="addButtonDisabled"
          @click="addContact"
        >
          Add
        </v-btn>
        <v-btn
          small
          text
          nuxt
          :to="cancelTo"
        >
          Cancel
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { CvContactRole } from '@/models/CvContactRole'

@Component({})
export default class ContactRoleForm extends Vue {
  @Prop({
    type: Array,
    required: false
  })
  private readonly existingContactRoles!: ContactRole[]

  @Prop({
    type: Array,
    required: false
  })
  private readonly contacts!: Contact[]

  @Prop({
    type: Array,
    required: false
  })
  private readonly cvContactRoles!: CvContactRole[]

  @Prop({
    type: String,
    required: true
  })
  private readonly cancelTo!: string

  @Prop({
    type: Boolean,
    default: false
  })
  private readonly editable!: boolean

  private selectedContact: Contact | null = null
  private selectedRole: CvContactRole | null = null

  roleContactCombinationAlreadyUsed (selectedRole: CvContactRole | null): boolean {
    if (this.selectedContact == null || selectedRole == null) {
      return false
    }
    // and the last one that we want to check is if the
    // contact & the role is already used
    const isAlreadyUsed = this.existingContactRoles.find(
      cr => cr.contact?.id === this.selectedContact?.id && cr.roleName === selectedRole.name
    ) !== undefined
    return isAlreadyUsed
  }

  roleAndContactNotDuplicated (selectedRole: CvContactRole | null): boolean | string {
    const isAlreadyUsed = this.roleContactCombinationAlreadyUsed(selectedRole)
    if (!isAlreadyUsed) {
      // everything is file
      return true
    }
    return this.selectedContact?.toString() + ' is already deposited as ' + this.selectedRole?.name
  }

  get addButtonDisabled (): boolean {
    if (!this.editable) {
      return true
    }
    if (this.selectedContact == null || this.selectedRole == null) {
      return true
    }
    return false
  }

  validateForm (): boolean {
    return (this.$refs.contactRoleForm as Vue & { validate: () => boolean }).validate()
  }

  addContact (): void {
    if (this.selectedContact && this.selectedContact.id && this.selectedRole && this.editable) {
      if (!this.validateForm()) {
        this.$store.commit('snackbar/setError', 'Please correct your input')
        return
      }
      // ok now the upper component can handle the contact role
      const newContactRole = ContactRole.createFromObject({
        contact: this.selectedContact,
        roleName: this.selectedRole.name,
        roleUri: this.selectedRole.uri,
        // We don't set the id. This will come from the post request.
        id: null
      })
      this.$emit('add-contact', newContactRole)
    }
  }
}
</script>

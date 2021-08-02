<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
  <v-form
    ref="unmountForm"
    @submit.prevent
  >
    <v-card-text>
      <v-row>
        <v-col>
          <v-autocomplete
            v-model="contact"
            :items="contacts"
            label="Contact"
            required
            :readonly="readonly"
            :rules="[rules.required]"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <v-textarea
            v-model="description"
            label="Description"
            rows="3"
            :readonly="readonly"
          />
        </v-col>
      </v-row>
    </v-card-text>
    <div
      v-if="!readonly"
    >
      <v-btn
        color="red"
        text
        data-role="remove-node"
        @click="remove"
      >
        remove
      </v-btn>
    </div>
  </v-form>
</template>
<script lang="ts">
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

@Component
export default class ConfigurationsSelectedItemUnmountForm extends mixins(Rules) {
  private contact: Contact | null = this.currentUserAsMountContact
  private description = ''

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  get currentUserAsMountContact (): Contact | null {
    const currentUserMail = this.$store.getters['oidc/userEmail']
    if (currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === currentUserMail)
      if (userIndex > -1) {
        return this.contacts[userIndex]
      }
    }
    return null
  }

  remove () {
    if (this.validateForm()) {
      this.$emit('remove', {
        contact: this.contact,
        description: this.description
      })
    } else {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
    }
  }

  validateForm (): boolean {
    return (this.$refs.unmountForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

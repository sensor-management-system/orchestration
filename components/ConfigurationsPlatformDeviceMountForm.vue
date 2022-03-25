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
    ref="mountForm"
    @submit.prevent
  >
    <v-row>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          v-model.number="offsetX"
          label="Offset (x)"
          type="number"
          step="any"
          :disabled="readonly"
          required
          :rules="[rules.numericRequired]"
          class="m-annotated"
          @wheel.prevent
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          v-model.number="offsetY"
          label="Offset (y)"
          type="number"
          step="any"
          :disabled="readonly"
          required
          :rules="[rules.numericRequired]"
          class="m-annotated"
          @wheel.prevent
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          v-model.number="offsetZ"
          label="Offset (z)"
          type="number"
          step="any"
          :disabled="readonly"
          required
          :rules="[rules.numericRequired]"
          class="m-annotated"
          @wheel.prevent
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-autocomplete
          v-model="contact"
          :items="contacts"
          label="Contact"
          :disabled="readonly"
          required
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
          :disabled="readonly"
        />
      </v-col>
    </v-row>
    <v-btn
      :disabled="readonly"
      :data-role="dataRoleBtn"
      @click="add"
    >
      mount
    </v-btn>
  </v-form>
</template>
<script lang="ts">

import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

@Component
export default class ConfigurationPlatformDeviceMountForm extends mixins(Rules) {
  private offsetX: number = 0.0
  private offsetY: number = 0.0
  private offsetZ: number = 0.0

  private contact: Contact | null = null
  private description = ''

  @Prop({
    default: () => '',
    required: true,
    type: String
  })
  readonly dataRoleBtn!: string

  @Prop({
    default: () => false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    type: String
  })
  // @ts-ignore
  readonly currentUserMail: string | null

  created () {
    this.contact = this.currentUserAsMountContact
  }

  get currentUserAsMountContact (): Contact | null {
    if (this.currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === this.currentUserMail)
      if (userIndex > -1) {
        return this.contacts[userIndex]
      }
    }
    return null
  }

  add () {
    if (this.validateForm()) {
      this.$emit('add', {
        offsetX: this.offsetX,
        offsetY: this.offsetY,
        offsetZ: this.offsetZ,
        contact: this.contact,
        description: this.description
      })
    } else {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
    }
  }

  validateForm (): boolean {
    return (this.$refs.mountForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style scoped>
/* the m-annotated class is to add the unit (meters) to the fields */
.m-annotated::after {
  content: " m";
  white-space: pre;
}
</style>

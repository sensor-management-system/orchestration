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
  <span>
    <v-form
      ref="mountForm"
      @submit.prevent
    >
      <v-container>
        <v-row class="pb-0">
          <v-col
            cols="12"
            md="3"
          >
            <v-text-field
              v-model.number="offsetX"
              data-role="textfield-offset-x"
              label="Offset (x)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numericRequired]"
              class="m-annotated"
              @wheel.prevent
              @input="add"
            />
          </v-col>
          <v-col
            cols="12"
            md="3"
          >
            <v-text-field
              v-model.number="offsetY"
              data-role="textfield-offset-y"
              label="Offset (y)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numericRequired]"
              class="m-annotated"
              @wheel.prevent
              @input="add"
            />
          </v-col>
          <v-col
            cols="12"
            md="3"
          >
            <v-text-field
              v-model.number="offsetZ"
              data-role="textfield-offset-z"
              label="Offset (z)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numericRequired]"
              class="m-annotated"
              @wheel.prevent
              @input="add"
            />
          </v-col>
        </v-row>
        <v-row class="mt-0 pt-0">
          <v-col>
            <span class="text-caption">Offsets are relative to parent platform/root</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <span>
              <v-autocomplete
                v-model="beginContact"
                data-role="select-begin-contact"
                :items="contacts"
                label="Begin Contact"
                :disabled="readonly"
                required
                :rules="[rules.required]"
                class="required"
                @input="add"
              />
            </span>
          </v-col>
          <v-col v-if="withUnmount">
            <span>

              <v-autocomplete
                v-model="endContact"
                data-role="select-end-contact"
                :items="contacts"
                label="End Contact"
                :disabled="readonly"
                required
                :rules="[rules.required]"
                class="required"
                @input="add"
              />
            </span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea
              v-model="beginDescription"
              data-role="textarea-begin-description"
              label="Begin Description"
              rows="3"
              :disabled="readonly"
              @input="add"
            />
          </v-col>
          <v-col v-if="withUnmount">
            <v-textarea
              v-model="endDescription"
              data-role="textarea-end-description"
              label="End Description"
              rows="3"
              :disabled="readonly"
              @input="add"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </span>
</template>
<script lang="ts">

import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'

@Component
export default class ConfigurationsPlatformDeviceMountForm extends mixins(Rules) {
  private offsetX: number = 0.0
  private offsetY: number = 0.0
  private offsetZ: number = 0.0

  private beginContact: Contact | null = null
  private beginDescription = ''
  private endContact: Contact | null = null
  private endDescription = ''

  @Prop({
    required: true,
    type: Object
  })
  readonly entity!: Platform | Device

  @Prop({
    default: () => false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly withUnmount!: boolean

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
    this.beginContact = this.currentUserAsMountContact
    this.endContact = this.withUnmount ? this.currentUserAsMountContact : null
    this.add()
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

  get entityType (): string {
    return this.entity.type
  }

  get entityIDString (): string {
    return `${this.entityType}-${this.entity?.id}`
  }

  add () {
    if (this.validateForm()) {
      this.$emit('add', {
        entity: this.entity,
        offsetX: this.offsetX,
        offsetY: this.offsetY,
        offsetZ: this.offsetZ,
        beginContact: this.beginContact,
        beginDescription: this.beginDescription,
        endContact: this.endContact,
        endDescription: this.endDescription
      })
    } else {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
    }
  }

  validateForm (): boolean {
    if (this.$refs.mountForm !== undefined) {
      return (this.$refs.mountForm as Vue & { validate: () => boolean }).validate()
    } else {
      return true
    }
  }
}
</script>

<style scoped>
/* @import "@/assets/styles/_forms.scss"; */

/* the m-annotated class is to add the unit (meters) to the fields */
.m-annotated::after {
  content: " m";
  white-space: pre;
}
</style>

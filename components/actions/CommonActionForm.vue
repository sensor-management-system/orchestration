<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
      <v-col cols="12" md="12">
        <v-textarea
          v-model="description"
          label="Description"
          rows="3"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-form
          ref="contactForm"
          v-model="contactIsValid"
          @submit.prevent
        >
          <v-autocomplete
            v-model="contact"
            :items="contacts"
            label="Contact"
            clearable
            required
            :item-text="(x) => x.toString()"
            :item-value="(x) => x"
            :rules="rules"
          />
        </v-form>
      </v-col>
      <v-col cols="12" md="1" align-self="center">
        <v-btn small @click="selectCurrentUserAsContact">
          {{ labelForSelectMeButton }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-select
          v-model="actionAttachments"
          multiple
          chips
          clearable
          deletable-chips
          label="Attachments"
          prepend-icon="mdi-paperclip"
          no-data-text="There are no attachments for this device"
          :items="attachments"
          :item-text="(x) => x.label"
          :item-value="(x) => x"
          :disabled="!attachments.length"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a set of common form fields for actions
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { IActionCommonDetails, ActionCommonDetails } from '@/models/ActionCommonDetails'

/**
 * A class component for a set of common form fields for actions
 * @extends Vue
 */
@Component
// @ts-ignore
export default class CommonActionForm extends Vue {
  private contacts: Contact[] = []
  private readonly labelForSelectMeButton = 'Add current user'
  private contactIsValid = true

  /**
   * an IActionCommonDetails like object
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: IActionCommonDetails

  /**
   * a list of available attachments
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly attachments!: Attachment[]

  /**
   * rules
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly rules!: ((v: any) => boolean | string)[]

  @Prop({
    type: String
  })
  // @ts-ignore
readonly currentUserMail: string|null

  async fetch () {
    try {
      this.contacts = await this.$api.contacts.findAll()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    }
  }

  get description (): string {
    return this.value.description
  }

  /**
   * sets the new description
   *
   * @param {string} value - the description to set
   * @fires CommonActionForm#input
   */
  set description (value: string) {
    const actionCopy = ActionCommonDetails.createFromObject(this.value)
    actionCopy.description = value
    /**
     * descriptionChange event
     * @event CommonActionForm#input
     * @type {string}
     */
    this.$emit('input', actionCopy)
  }

  get contact (): Contact | null {
    return this.value.contact
  }

  /**
   * sets the new contact
   *
   * @param {Contact | null} value - the contact to set
   * @fires CommonActionForm#input
   */
  set contact (value: Contact | null) {
    const actionCopy = ActionCommonDetails.createFromObject(this.value)
    actionCopy.contact = value || null
    /**
     * contactChange event
     * @event CommonActionForm#input
     * @type {Contact}
     */
    this.$emit('input', actionCopy)
  }

  get actionAttachments (): Attachment[] {
    return this.value.attachments
  }

  /**
   * sets the new list of attachments
   *
   * @param {Attachment[]} value - the list of attachments to set
   * @fires CommonActionForm#input
   */
  set actionAttachments (value: Attachment[]) {
    const actionCopy = ActionCommonDetails.createFromObject(this.value)
    actionCopy.attachments = value
    /**
     * attachments event
     * @event CommonActionForm#input
     * @type {Attachment[]}
     */
    this.$emit('input', actionCopy)
  }

  /**
   * selects the current (loggined) user from the list of users and adds the
   * user to the action
   *
   */
  selectCurrentUserAsContact () {
    if (this.currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === this.currentUserMail)
      if (userIndex > -1) {
        this.contact = this.contacts[userIndex]
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  /**
   * returns whether the form is valid based on the defined rules
   *
   * @return {boolean} whether the form is valid or not
   */
  isValid (): boolean {
    return (this.$refs.contactForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

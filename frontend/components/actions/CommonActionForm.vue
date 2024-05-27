<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
            class="required"
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
    <v-row
      v-if="!hideAttachments"
    >
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
          :item-text="attachmentText"
          :item-value="(x) => x"
          :disabled="!attachments.length"
        >
          <template #item="{ item, attrs, on }">
            <v-list-item v-slot="{ active }" v-bind="attrs" v-on="on">
              <v-list-item-action>
                <v-checkbox :ripple="false" :input-value="active" />
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-subtitle
                  v-if="item.isUpload && item.createdAt"
                  class="text--secondary text-caption"
                >
                  uploaded at {{ item.createdAt | dateToDateTimeStringHHMM }}
                </v-list-item-subtitle>
                <v-list-item-title>
                  {{ item.label }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-select>
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
import { IActionCommonDetailsLike, ActionCommonDetails } from '@/models/ActionCommonDetails'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

/**
 * A class component for a set of common form fields for actions
 * @extends Vue
 */
@Component({
  filters: {
    dateToDateTimeStringHHMM
  }
})
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
  readonly value!: IActionCommonDetailsLike

  /**
   * a list of available attachments
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly attachments!: Attachment[]

  /**
   * rules
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly rules!: ((v: any) => boolean | string)[]

  @Prop({
    default: '',
    required: false,
    type: String
  })
  readonly currentUserMail!: string | null

  @Prop({
    default: false,
    type: Boolean,
    required: false
  })
  readonly hideAttachments!: boolean

  async fetch () {
    try {
      this.contacts = await this.$api.contacts.findAll()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    }
  }

  get description (): string {
    return this.value.description || ''
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
    return this.value.contact || null
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
    return this.value.attachments || []
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

  attachmentText (attachment: Attachment): string {
    if (attachment.isUpload && attachment.createdAt) {
      return attachment.label + ', uploaded at ' + dateToDateTimeStringHHMM(attachment.createdAt)
    }
    return attachment.label
  }
}
</script>
<style lang="scss">
@import '@/assets/styles/_forms.scss';
</style>

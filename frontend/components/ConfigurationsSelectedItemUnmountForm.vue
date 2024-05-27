<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
            :disabled="readonly"
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
    </v-card-text>
    <v-row
      v-if="!readonly"
      dense
    >
      <v-col
        class="text-right"
      >
        <v-btn
          color="red"
          text
          data-role="remove-node"
          small
          @click="unmount"
        >
          unmount
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

@Component
export default class ConfigurationsSelectedItemUnmountForm extends mixins(Rules) {
  private contact: Contact | null = null
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

  unmount () {
    if (!this.validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.$emit('unmount', {
      contact: this.contact,
      description: this.description
    })
  }

  validateForm (): boolean {
    return (this.$refs.unmountForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

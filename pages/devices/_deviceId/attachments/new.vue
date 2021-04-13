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
  <v-form ref="attachmentsForm" class="pl-10" @submit.prevent>
    <v-row>
      <v-col cols="12" md="3">
        <v-radio-group
          v-model="attachmentType"
          label="Type"
          row
        >
          <v-radio label="File" value="file" />
          <v-radio label="Url" value="url" />
        </v-radio-group>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-file-input
          v-if="attachmentType === 'file'"
          v-model="file"
          :accept="mimeTypeList"
          label="File"
          required
          class="required"
          :rules="[rules.required]"
          show-size
        />
        <v-text-field
          v-if="attachmentType === 'url'"
          v-model="attachment.url"
          label="URL"
          type="url"
          placeholder="http://"
          required
          class="required"
          :rules="[rules.required, rules.validUrl]"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="attachment.label"
          label="Label"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-spacer />
        <v-btn
          v-if="isLoggedIn"
          ref="cancelButton"
          text
          small
          :to="'/devices/' + deviceId + '/attachments'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
          color="green"
          small
          data-role="add-attachment"
          @click="add()"
        >
          {{ attachmentType === 'url' ? 'Add' : 'Upload' }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { Rules } from '@/mixins/Rules'

import { Attachment } from '@/models/Attachment'

@Component({
  components: {}
})
export default class AttachmentAddPage extends mixins(Rules) {
  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null

  mounted () {
    const cancelButton = this.$refs.cancelButton as Vue
    // due to the active route (and the button being a router link)
    // this button has the active class
    // however, we don't want this special behaviour for this button
    cancelButton.$el.classList.remove('v-btn--active')
  }

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return Object.keys(Attachment.mimeTypes).join(',')
  }

  add () {
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    this.$emit('showsave', true)
    this.$api.deviceAttachments.add(this.deviceId, this.attachment).then((newAttachment: Attachment) => {
      this.$emit('showsave', false)
      this.$emit('input', newAttachment)
      this.$router.push('/devices/' + this.deviceId + '/attachments')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    })
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>

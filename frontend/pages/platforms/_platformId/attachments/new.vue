<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <div>
    <v-form ref="attachmentsForm" class="pb-2" @submit.prevent>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/platforms/' + platformId + '/attachments'"
          @save="add"
        />
      </v-card-actions>
      <v-card-text>
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
          <v-col cols="12">
            <v-file-input
              v-if="attachmentType === 'file'"
              v-model="file"
              :accept="mimeTypeList"
              label="File"
              required
              class="required"
              :rules="[rules.required, uploadRules.maxSize, uploadRules.mimeTypeAllowed]"
              show-size
            />
            <v-text-field
              v-if="attachmentType === 'url'"
              v-model="attachment.url"
              label="URL"
              type="url"
              placeholder="https://"
              required
              class="required"
              :rules="[rules.required, rules.validUrl]"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="attachment.label"
              label="Label"
              required
              class="required"
              :rules="[rules.required]"
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/platforms/' + platformId + '/attachments'"
          @save="add"
        />
      </v-card-actions>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { AddPlatformAttachmentAction, LoadPlatformAttachmentsAction } from '@/store/platforms'

import UploadConfig from '@/config/uploads'

import { IUploadResult } from '@/services/sms/UploadApi'

import { Attachment } from '@/models/Attachment'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'

@Component({
  components: { SaveAndCancelButtons },
  middleware: ['auth'],
  methods: {
    ...mapActions('platforms', ['addPlatformAttachment', 'loadPlatformAttachments']),
    ...mapActions('files', ['uploadFile']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformAttachmentAddPage extends mixins(Rules, UploadRules, CheckEditAccess) {
  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null

  // vuex definition for typescript check
  uploadFile!: (file: File) => Promise<IUploadResult>
  addPlatformAttachment!: AddPlatformAttachmentAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  setLoading!: SetLoadingAction
  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return UploadConfig.allowedMimeTypes.join(',')
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  async add () {
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    let theFailureCanBeFromUpload = true

    try {
      this.setLoading(true)

      if (this.attachmentType !== 'url' && this.file !== null) {
        // Due to the validation we can be sure that the file is not null
        const uploadResult = await this.uploadFile(this.file)
        this.attachment.url = uploadResult.url
        theFailureCanBeFromUpload = false
      }
      await this.addPlatformAttachment({ platformId: this.platformId, attachment: this.attachment })
      await this.loadPlatformAttachments(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    } catch (error: any) {
      this.handleError(theFailureCanBeFromUpload, error)
    } finally {
      this.setLoading(false)
    }
  }

  private handleError (theFailureCanBeFromUpload: boolean, error: any) {
    let message = 'Failed to save an attachment'

    if (theFailureCanBeFromUpload && error.response?.data?.errors?.length) {
      const errorDetails = error.response.data.errors[0]
      if (errorDetails.source && errorDetails.title) {
        // In this case something ala 'Unsupported Media Type: application/exe is Not Permitted'
        message = errorDetails.title + ': ' + errorDetails.source
      }
    }
    this.$store.commit('snackbar/setError', message)
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

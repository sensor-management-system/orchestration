<!--
SPDX-FileCopyrightText: 2020 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
        :to="'/platforms/' + platformId + '/attachments'"
        @save="add"
      />
    </v-card-actions>
    <AttachmentCreateForm ref="attachmentsForm" v-model="attachmentCreateFormData" />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        ref="cancelButton"
        text
        small
        nuxt
        :to="'/platforms/' + platformId + '/attachments'"
      >
        Cancel
      </v-btn>
      <v-btn
        v-if="editable"
        color="accent"
        small
        data-role="add-attachment"
        @click="add()"
      >
        {{ attachmentType === 'url' ? 'Add' : 'Upload' }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddPlatformAttachmentAction,
  LoadPlatformAttachmentsAction,
  AddPlatformImageAction,
  LoadPlatformAction
} from '@/store/platforms'

import { IUploadResult } from '@/services/sms/UploadApi'

import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import AttachmentCreateForm, { AttachmentCreationFormDTO } from '@/components/shared/AttachmentCreateForm.vue'

@Component({
  components: { AttachmentCreateForm, SaveAndCancelButtons },
  middleware: ['auth'],
  methods: {
    ...mapActions('platforms', ['addPlatformAttachment', 'loadPlatformAttachments', 'loadPlatform', 'addPlatformImage']),
    ...mapActions('files', ['uploadFile']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformAttachmentAddPage extends mixins(CheckEditAccess, AttachmentsMixin) {
  private attachmentCreateFormData: AttachmentCreationFormDTO = {
    attachment: new Attachment(),
    attachmentType: 'file',
    file: null,
    imageWillBeCreated: false
  }

  get attachment (): Attachment {
    return this.attachmentCreateFormData.attachment
  }

  get attachmentType (): string {
    return this.attachmentCreateFormData.attachmentType
  }

  get file (): File|null {
    return this.attachmentCreateFormData.file
  }

  get imageWillBeCreated (): Boolean {
    return this.attachmentCreateFormData.imageWillBeCreated
  }

  // vuex definition for typescript check
  uploadFile!: (file: File) => Promise<IUploadResult>
  addPlatformAttachment!: AddPlatformAttachmentAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  loadPlatform!: LoadPlatformAction
  addPlatformImage!: AddPlatformImageAction
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

  get platformId (): string {
    return this.$route.params.platformId
  }

  async add () {
    if (!(this.$refs.attachmentsForm as AttachmentCreateForm & { validateForm: () => boolean }).validateForm()) {
      return
    }

    (this.$refs.attachmentsForm as AttachmentCreateForm & { resetValidation: () => boolean }).resetValidation()

    let theFailureCanBeFromUpload = true

    try {
      this.setLoading(true)

      if (this.attachmentType !== 'url' && this.file !== null) {
        // Due to the validation we can be sure that the file is not null
        const uploadResult = await this.uploadFile(this.file)
        this.attachment.url = uploadResult.url
        theFailureCanBeFromUpload = false
      }
      const newPlatformAttachment = await this.addPlatformAttachment({ platformId: this.platformId, attachment: this.attachment })
      await this.loadPlatformAttachments(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')

      if (this.imageWillBeCreated) {
        const newPlatformImage: Image = Image.createFromObject({
          id: '',
          attachment: newPlatformAttachment,
          // Order index is set to the current timestamp by the API,
          // so the new image will be inserted at the end of existing images
          orderIndex: null
        })
        try {
          await this.addPlatformImage({ platformId: this.platformId, platformImage: newPlatformImage })
          this.loadPlatform({
            platformId: this.platformId,
            includeImages: true
          })
        } catch (error: any) {
          this.$store.commit(
            'snackbar/setError',
            'Failed to add an attachment as image'
          )
        }
      }

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

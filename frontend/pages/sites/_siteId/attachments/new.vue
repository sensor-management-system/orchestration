<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
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
        :to="'/sites/' + siteId + '/attachments'"
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
        :to="'/sites/' + siteId + '/attachments'"
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
import { Component, mixins, Watch } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddSiteAttachmentAction,
  LoadSiteAttachmentsAction,
  AddSiteImageAction,
  LoadSiteAction
} from '@/store/sites'

import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import AttachmentCreateForm, { AttachmentCreationFormDTO } from '@/components/shared/AttachmentCreateForm.vue'
import { IUploadResult } from '@/services/sms/UploadApi'

@Component({
  components: { AttachmentCreateForm, SaveAndCancelButtons },
  middleware: ['auth'],
  methods: {
    ...mapActions('sites', ['addSiteAttachment', 'loadSiteAttachments', 'loadSite', 'addSiteImage']),
    ...mapActions('files', ['uploadFile']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteAttachmentAddPage extends mixins(CheckEditAccess, AttachmentsMixin) {
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
  addSiteAttachment!: AddSiteAttachmentAction
  loadSiteAttachments!: LoadSiteAttachmentsAction
  loadSite!: LoadSiteAction
  addSiteImage!: AddSiteImageAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/sites/' + this.siteId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this site.'
  }

  get siteId (): string {
    return this.$route.params.siteId
  }

  async add () {
    if (!(this.$refs.attachmentsForm as AttachmentCreateForm & { validateForm: () => boolean }).validateForm()) {
      return
    }

    (this.$refs.attachmentsForm as AttachmentCreateForm & { resetValidation: () => boolean }).resetValidation()

    let theFailureCanBeFromUpload = true
    try {
      this.setLoading(true)

      if (this.attachmentType !== 'url') {
        // Due to the validation we can be sure that the file is not null
        const uploadResult = await this.uploadFile(this.file as File)
        this.attachment.url = uploadResult.url
        theFailureCanBeFromUpload = false
      }

      const newSiteAttachment = await this.addSiteAttachment({
        siteId: this.siteId,
        attachment: this.attachment
      })
      this.loadSiteAttachments(this.siteId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')

      if (this.imageWillBeCreated) {
        const newSiteImage: Image = Image.createFromObject({
          id: '',
          attachment: newSiteAttachment,
          // Order index is set to the current timestamp by the API,
          // so the new image will be inserted at the end of existing images
          orderIndex: null
        })
        try {
          await this.addSiteImage({ siteId: this.siteId, siteImage: newSiteImage })
          this.loadSite({ siteId: this.siteId, includeImages: true })
        } catch (error: any) {
          this.$store.commit(
            'snackbar/setError',
            'Failed to add an attachment as image'
          )
        }
      }

      this.$router.push('/sites/' + this.siteId + '/attachments')
    } catch (error: any) {
      this.handleError(error, theFailureCanBeFromUpload)
    } finally {
      this.setLoading(false)
    }
  }

  private handleError (error: any, theFailureCanBeFromUpload: boolean) {
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

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/sites/' + this.siteId + '/attachments', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this site.')
      })
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

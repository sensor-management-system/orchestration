<!--
SPDX-FileCopyrightText: 2020 - 2024
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
    <v-form ref="attachmentsForm" class="pb-2" @submit.prevent>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="editable"
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/configurations/' + configurationId + '/attachments'"
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
            <autocomplete-text-input
              v-model="attachment.label"
              label="Label"
              required
              class="required"
              endpoint="attachment-labels"
              :rules="[rules.required]"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea
              v-model="attachment.description"
              label="Description"
              rows="3"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-checkbox
              v-model="imageWillBeCreated"
              :disabled="!attachmentCanBeUsedAsImage"
              label="Show the attachment as an image on the Basic Data tab."
              :hint="createImageHint"
              persistent-hint
              @change="imageShouldBeCreatedExplicitChoiceChanged"
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          ref="cancelButton"
          text
          small
          nuxt
          :to="'/configurations/' + configurationId + '/attachments'"
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
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins, Watch } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddConfigurationAttachmentAction,
  AddConfigurationImageAction,
  LoadConfigurationAction,
  LoadConfigurationAttachmentsAction
} from '@/store/configurations'

import UploadConfig from '@/config/uploads'

import { IUploadResult } from '@/services/sms/UploadApi'

import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

@Component({
  components: { AutocompleteTextInput, SaveAndCancelButtons },
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['addConfigurationAttachment', 'loadConfigurationAttachments', 'loadConfiguration', 'addConfigurationImage']),
    ...mapActions('files', ['uploadFile']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationAttachmentAddPage extends mixins(Rules, UploadRules, CheckEditAccess, AttachmentsMixin) {
  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null
  private imageShouldBeCreatedExplicitChoice: boolean = true

  // vuex definition for typescript check
  uploadFile!: (file: File) => Promise<IUploadResult>
  addConfigurationAttachment!: AddConfigurationAttachmentAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  setLoading!: SetLoadingAction
  loadConfiguration!: LoadConfigurationAction
  addConfigurationImage!: AddConfigurationImageAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return UploadConfig.allowedMimeTypes.join(',')
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get imageWillBeCreated () {
    return this.imageShouldBeCreatedExplicitChoice && this.attachmentCanBeUsedAsImage
  }

  imageShouldBeCreatedExplicitChoiceChanged (shouldBeCreated: boolean) {
    this.imageShouldBeCreatedExplicitChoice = shouldBeCreated
  }

  async add () {
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    let theFailureCanBeFromUpload = true
    try {
      this.setLoading(true)

      if (this.attachmentType !== 'url') {
        // Due to the validation we can be sure that the file is not null
        const uploadResult = await this.uploadFile(this.file as File)
        this.attachment.url = uploadResult.url
        theFailureCanBeFromUpload = false
      }

      const newConfigurationAttachment = await this.addConfigurationAttachment({
        configurationId: this.configurationId,
        attachment: this.attachment
      })
      this.loadConfigurationAttachments(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')

      if (this.imageWillBeCreated) {
        const newConfigurationImage: Image = Image.createFromObject({
          id: '',
          attachment: newConfigurationAttachment,
          // Order index is set to the current timestamp by the API,
          // so the new image will be inserted at the end of existing images
          orderIndex: null
        })
        try {
          await this.addConfigurationImage({
            configurationId: this.configurationId,
            configurationImage: newConfigurationImage
          })
          this.loadConfiguration(this.configurationId)
        } catch (error: any) {
          this.$store.commit(
            'snackbar/setError',
            'Failed to add an attachment as image'
          )
        }
      }

      this.$router.push('/configurations/' + this.configurationId + '/attachments')
    } catch (error: any) {
      this.handleError(error, theFailureCanBeFromUpload)
    } finally {
      this.setLoading(false)
    }
  }

  get attachmentCanBeUsedAsImage (): boolean {
    if (this.attachmentType === 'file') {
      if (!this.file) { return false }
      return this.validImageExtensions.some(extension => this.file?.name.endsWith(extension))
    }
    return this.validImageExtensions.some(extension => this.attachment.url.endsWith(extension))
  }

  get createImageHint (): string {
    if (this.attachmentType === 'file' && !this.file) { return '' }
    if (this.attachmentType === 'url' && !this.attachment.url) { return '' }
    return this.attachmentCanBeUsedAsImage
      ? 'You can adjust the position or disable it when editing the Basic Data.'
      : 'This attachment can\'t be used for images in the Basic Data Tab.'
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
      this.$router.replace('/configurations/' + this.configurationId + '/attachments', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

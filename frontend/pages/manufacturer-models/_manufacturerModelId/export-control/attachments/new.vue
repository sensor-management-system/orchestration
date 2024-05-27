<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form ref="attachmentsForm" class="pb-2" @submit.prevent>
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          v-if="canHandleExportControl"
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
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
        <v-row>
          <v-col cols="12" md="6">
            <v-radio-group
              v-model="attachment.isExportControlOnly"
              label="Visibility"
              row
            >
              <v-radio label="Internal" :value="true" />
              <v-radio label="Public" :value="false" />
            </v-radio-group>
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
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          v-if="canHandleExportControl"
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
          @save="add"
        />
      </v-card-actions>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters } from 'vuex'

import UploadConfig from '@/config/uploads'

import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { ExportControlAttachment } from '@/models/ExportControlAttachment'
import { CanHandleExportControlGetter } from '@/store/permissions'
import { IUploadResult } from '@/services/sms/UploadApi'
import { SetLoadingAction } from '@/store/progressindicator'
import { AddExportControlAttachmentAction, LoadExportControlAttachmentsAction } from '@/store/manufacturermodels'

@Component({
  computed: {
    ...mapGetters('permissions', ['canHandleExportControl'])
  },
  components: {
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('manufacturermodels', ['addExportControlAttachment', 'loadExportControlAttachments']),
    ...mapActions('files', ['uploadFile']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ExportControlAttachmentAddPage extends mixins(Rules, UploadRules) {
  private attachmentType: string = 'file'
  private attachment: ExportControlAttachment = new ExportControlAttachment()
  private file: File | null = null

  canHandleExportControl!: CanHandleExportControlGetter
  uploadFile!: (file: File) => Promise<IUploadResult>
  setLoading!: SetLoadingAction
  addExportControlAttachment!: AddExportControlAttachmentAction
  loadExportControlAttachments!: LoadExportControlAttachmentsAction

  get mimeTypeList (): string {
    return UploadConfig.allowedMimeTypes.join(',')
  }

  get manufacturerModelId (): string {
    return this.$route.params.manufacturerModelId
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

      await this.addExportControlAttachment({
        manufacturerModelId: this.manufacturerModelId,
        attachment: this.attachment
      })
      this.loadExportControlAttachments(this.manufacturerModelId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')
      this.$router.push('/manufacturer-models/' + this.manufacturerModelId + '/export-control')
    } catch (error: any) {
      this.handelError(error, theFailureCanBeFromUpload)
    } finally {
      this.setLoading(false)
    }
  }

  private handelError (error: any, theFailureCanBeFromUpload: boolean) {
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

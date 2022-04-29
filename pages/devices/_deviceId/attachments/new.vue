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
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-form ref="attachmentsForm" class="pb-2" @submit.prevent>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :save-btn-text="attachmentType === 'url' ? 'Add' : 'Upload'"
          :to="'/devices/' + deviceId + '/attachments'"
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
          :to="'/devices/' + deviceId + '/attachments'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
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
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import UploadConfig from '@/config/uploads'

import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'

import { Attachment } from '@/models/Attachment'
import { mapActions } from 'vuex'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, SaveAndCancelButtons },
  middleware: ['auth'],
  methods: {
    ...mapActions('devices',['addDeviceAttachment','loadDeviceAttachments']),
    ...mapActions('files',['uploadFile'])
  }
})
export default class DeviceAttachmentAddPage extends mixins(Rules, UploadRules) {
  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null
  private isSaving: boolean = false

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return UploadConfig.allowedMimeTypes.join(',')
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async add () {
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    let theFailureCanBeFromUpload = true
    try {

      this.isSaving=true

      if (this.attachmentType !== 'url') {
        // Due to the validation we can be sure that the file is not null
        const uploadResult = await this.uploadFile(this.file as File)
        this.attachment.url = uploadResult.url
        theFailureCanBeFromUpload = false
      }

      await this.addDeviceAttachment({
        deviceId:this.deviceId,
        attachment: this.attachment
      })
      this.loadDeviceAttachments(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New attachment added')
      this.$router.push('/devices/' + this.deviceId + '/attachments')
    } catch (error: any) {
      this.handelError(error,theFailureCanBeFromUpload)
    }finally {
      this.isSaving=false
    }
  }

  private handelError(error:any,theFailureCanBeFromUpload:boolean){
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

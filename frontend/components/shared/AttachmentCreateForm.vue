<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-form ref="form" class="pb-2" @submit.prevent>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="3">
          <v-radio-group
            :value="value.attachmentType"
            label="Type"
            row
            @change="update('attachmentType', $event)"
          >
            <v-radio label="File" value="file" />
            <v-radio label="Url" value="url" />
          </v-radio-group>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-file-input
            v-if="value.attachmentType === 'file'"
            :value="value.file"
            :accept="mimeTypeList"
            label="File"
            required
            class="required"
            :rules="[rules.required, uploadRules.maxSize, uploadRules.mimeTypeAllowed]"
            show-size
            @change="update('file', $event)"
          />
          <v-text-field
            v-if="value.attachmentType === 'url'"
            :value="value.attachment.url"
            label="URL"
            type="url"
            placeholder="https://"
            required
            class="required"
            :rules="[rules.required, rules.validUrl]"
            @input="update('attachment.url', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <autocomplete-text-input
            :value="value.label"
            label="Label"
            required
            class="required"
            endpoint="attachment-labels"
            :rules="[rules.required]"
            @input="update('attachment.label', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-textarea
            :value="value.description"
            label="Description"
            rows="3"
            @input="update('attachment.description', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-checkbox
            :value="value.imageWillBeCreated"
            :disabled="!checkIfImageCanBeCreatedWithFormData(value)"
            label="Show the attachment as an image on the Basic Data tab."
            :hint="createImageHint"
            persistent-hint
            @change="update('imageWillBeCreated', $event)"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, mixins, Prop } from 'nuxt-property-decorator'

import UploadConfig from '@/config/uploads'

import { Attachment } from '@/models/Attachment'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'

import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

export interface AttachmentCreationFormDTO {
  attachmentType: string
  attachment: Attachment
  file: File|null
  imageWillBeCreated: Boolean
}

@Component({
  components: { AutocompleteTextInput }
})
export default class AttachmentCreateForm extends mixins(Rules, UploadRules, AttachmentsMixin) {
  private imageShouldBeCreatedExplicitChoice: boolean = true

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: AttachmentCreationFormDTO

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return UploadConfig.allowedMimeTypes.join(',')
  }

  validateForm (): boolean {
    return (this.$refs.form as Vue & { validate: () => boolean }).validate()
  }

  resetValidation (): boolean {
    return (this.$refs.form as Vue & { resetValidation: () => boolean }).resetValidation()
  }

  checkIfImageCanBeCreatedWithFormData (value: AttachmentCreationFormDTO): boolean {
    if (value.attachmentType === 'file') {
      if (!value.file) {
        return false
      }
      return this.validImageExtensions.some(extension => value.file?.name.endsWith(extension))
    }
    return this.validImageExtensions.some(extension => value.attachment.url.endsWith(extension)) && this.rules.validUrl(value.attachment.url) === true
  }

  get createImageHint (): string {
    if (this.value.attachmentType === 'file' && !this.value.file) {
      return ''
    }
    if (this.value.attachmentType === 'url' && !this.value.attachment.url) {
      return ''
    }
    return this.checkIfImageCanBeCreatedWithFormData(this.value)
      ? 'You can adjust the position or disable it when editing the Basic Data.'
      : 'This attachment can\'t be used for images in the Basic Data Tab.'
  }

  update (key: string, value: any) {
    const newObj: AttachmentCreationFormDTO = {
      attachment: this.value.attachment,
      attachmentType: this.value.attachmentType,
      file: this.value.file,
      imageWillBeCreated: this.value.imageWillBeCreated
    }

    switch (key) {
      case 'attachment.url':
        newObj.attachment.url = value as string
        break
      case 'attachment.label':
        newObj.attachment.label = value as string
        break
      case 'attachment.description':
        newObj.attachment.description = value as string
        break

      case 'file':
        newObj.file = value as File
        break
      case 'attachmentType':
        newObj.attachmentType = value as string
        break
      case 'imageWillBeCreated':
        this.imageShouldBeCreatedExplicitChoice = value as boolean
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    newObj.imageWillBeCreated = this.imageShouldBeCreatedExplicitChoice && this.checkIfImageCanBeCreatedWithFormData(newObj)
    this.$emit('input', newObj)
  }
}
</script>

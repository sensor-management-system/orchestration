<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-form ref="form">
    <v-row>
      <v-col>
        <v-icon>{{ filetypeIcon(value) }}</v-icon>
        <span class="text-caption">
          {{ filename(value) }}
          <span v-if="value.createdAt && value.isUpload">,
            uploaded at {{ value.createdAt | toUtcDateTimeString }}
          </span>
        </span>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-text-field
          :value="value.url"
          :label="value.isUpload ? 'File': 'URL'"
          required
          class="required"
          type="url"
          placeholder="https://"
          :rules="value.isUpload ? [] : [rules.required, rules.validUrl]"
          :disabled="value.isUpload"
          @input="update('url', $event)"
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
          @input="update('label', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea
          :value="value.description"
          label="Description"
          rows="3"
          @input="update('description', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'

import { Rules } from '@/mixins/Rules'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

@Component({
  components: { AutocompleteTextInput }
})
export default class AttachmentBasicDataForm extends mixins(Rules, AttachmentsMixin) {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Attachment

  validateForm (): boolean {
    return (this.$refs.form as Vue & { validate: () => boolean }).validate()
  }

  update (key: string, value: any) {
    const newObj = Attachment.createFromObject(this.value)

    switch (key) {
      case 'url':
        newObj.url = value as string
        break
      case 'label':
        newObj.label = value as string
        break
      case 'description':
        newObj.description = value as string || ''
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', newObj)
  }
}
</script>

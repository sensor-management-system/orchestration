<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
  <v-form ref="attachmentsForm" @submit.prevent>
    <v-row v-if="!readonly">
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
    <v-row v-if="!readonly">
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
    <v-row v-if="!readonly">
      <v-col cols="12" md="4">
        <v-text-field
          v-model="attachment.label"
          label="Label"
        />
      </v-col>
    </v-row>
    <v-row v-if="!readonly">
      <v-col cols="12">
        <v-spacer />
        <v-btn
          color="primary"
          small
          data-role="add-attachment"
          @click="add()"
        >
          {{ attachmentType === 'url' ? 'Add' : 'Upload' }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-list
          two-line
          subheader
        >
          <v-subheader v-if="value.length" inset>
            Attachments
          </v-subheader>

          <AttachmentListItem
            v-for="(item, index) in value"
            :key="getUrlIndex(item)"
            v-model="value[index]"
            :readonly="readonly"
          >
            <template
              v-if="!readonly"
              v-slot:action
            >
              <v-btn
                icon
                color="error"
                data-role="delete-attachment"
                @click="remove(index)"
              >
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </template>
          </AttachmentListItem>
        </v-list>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
/**
 * @file provides a component for a listing of attachments
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'
import { Rules } from '@/mixins/Rules'

import AttachmentListItem from '@/components/AttachmentListItem.vue'

import { Attachment } from '@/models/Attachment'

/**
 * A class component for a list of Attachments and an upload form
 * @extends Vue
 */
@Component({
  components: { AttachmentListItem }
})
// @ts-ignore
export default class AttachmentList extends mixins(Rules) {
  /**
   * an Array of Attachments
   */
  @Prop({
    default: () => [] as Attachment[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Attachment[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'
  private file: File | null = null

  /**
   * adds a new Attachment instance
   *
   * @fires AttachmentList#input
   */
  add () {
    // see https://stackoverflow.com/a/52109899/86224
    if (!(this.$refs.attachmentsForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsForm as Vue & { resetValidation: () => boolean }).resetValidation()

    /**
     * fires an input event
     * @event AttachmentList#input
     * @type {Attachment[]}
     */
    this.$emit('input', [
      ...this.value,
      this.attachment
    ] as Attachment[])

    this.attachment = new Attachment()
    this.file = null
  }

  /**
   * removes an Attachment instance
   *
   * @param {number} index - the index of the attachment to remove
   * @fires AttachmentList#input
   */
  remove (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as Attachment[]
      properties.splice(index, 1)
      /**
       * fires an input event
       * @event AttachmentList#input
       * @type {Attachment[]}
       */
      this.$emit('input', properties)
    }
  }

  /**
   * returns a list of MimeTypes, seperated by ,
   *
   * @return {string} a list of MimeTypes
   */
  get mimeTypeList (): string {
    return Object.keys(Attachment.mimeTypes).join(',')
  }

  /**
   * returns a unique index for the attachment in the list
   *
   * @param {Attachment} item - the attachment for that the index shall be created
   * @return {string} the index in the form url + '#' + <count of url in the list if gt 0>
   */
  getUrlIndex (item: Attachment) {
    const cnt: number = this.value.filter((attachment: Attachment): boolean => item.url === attachment.url).indexOf(item)
    return cnt > 0 ? item.url + '#' + cnt : item.url
  }
}
</script>

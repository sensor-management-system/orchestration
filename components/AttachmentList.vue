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
import { Attachment } from '../models/Attachment'

// @ts-ignore
import AttachmentListItem from './AttachmentListItem.vue'

/**
 * A class component for a list of Attachments and an upload form
 * @extends Vue
 */
@Component({
  components: { AttachmentListItem }
})
// @ts-ignore
export default class AttachmentList extends mixins(Rules) {
  @Prop({
    default: () => [] as Attachment[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Attachment[]

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
     * Update event
     * @event AttachmentList#input
     * @type Attachment[]
     */
    this.$emit('input', [
      ...this.value,
      this.attachment
    ] as Attachment[])

    this.attachment = new Attachment()
    this.file = null
  }

  /**
   * removes as Attachment instance
   *
   * @param {number} index - the index of the property to remove
   * @fires AttachmentList#input
   */
  remove (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as Attachment[]
      properties.splice(index, 1)
      /**
       * Update event
       * @event AttachmentList#input
       * @type Attachment[]
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

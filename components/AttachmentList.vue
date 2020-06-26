<template>
  <v-form ref="attachmentsForm">
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
          :accept="mimeTypeList"
          label="File"
          required
          class="required"
          :rules="rules.required ? [rules.required] : []"
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
          :rules="rules.required ? [rules.required] : []"
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
          @click="add()"
        >
          Upload
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
            :key="'attachment-' + index"
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'
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
export default class AttachmentList extends Vue {
  @Prop({
    default: () => [] as Attachment[],
    required: true,
    type: Array
  })
  // @ts-ignore
  value!: Attachment[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  @Prop({
    default: {},
    required: false,
    type: Object
  })
  // @ts-ignore
  rules!: Object

  private attachment: Attachment = new Attachment()
  private attachmentType: string = 'file'

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

  get mimeTypeList (): string {
    return Object.keys(Attachment.mimeTypes).join(',')
  }
}
</script>

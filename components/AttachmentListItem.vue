<template>
  <v-list-item>
    <v-list-item-avatar>
      <v-icon large>
        {{ filetype }}
      </v-icon>
    </v-list-item-avatar>
    <v-list-item-content>
      <v-list-item-subtitle>
        {{ filename }}, uploaded at {{ uploadedDateTime }}
      </v-list-item-subtitle>
      <v-list-item-title v-if="readonly">
        <a :href="value.url" target="_blank">{{ value.label }}</a>
      </v-list-item-title>
      <v-list-item-title v-else>
        <v-text-field
          :value="value.label"
          @input="update('label', $event)"
        />
      </v-list-item-title>
    </v-list-item-content>
    <v-list-item-action
      v-if="!readonly"
    >
      <v-btn
        icon
        color="primary"
        :href="value.url"
      >
        <v-icon>
          mdi-link
        </v-icon>
      </v-btn>
    </v-list-item-action>
    <v-list-item-action>
      <slot name="action" />
    </v-list-item-action>
  </v-list-item>
</template>

<script lang="ts">
/**
 * @file provides a component for an attachment
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Attachment } from '../models/Attachment'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AttachmentListItem extends Vue {
  @Prop({
    required: true,
    type: Attachment
  })
  // @ts-ignore
  value!: Attachment

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  get filename (): string {
    const UNKNOWN_FILENAME = 'unknown filename'

    if (this.value.url === '') {
      return UNKNOWN_FILENAME
    }
    const paths = this.value.url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  get uploadedDateTime (): string {
    return '2020-06-17 16:35 (TODO)'
  }

  get filetype (): string {
    let extension = ''
    const paths = this.filename.split('.')
    if (paths.length) {
      // @ts-ignore
      extension = paths.pop().toLowerCase()
    }
    switch (extension) {
      case 'png':
      case 'jpg':
      case 'jpeg':
        return 'mdi-image'
      case 'pdf':
        return 'mdi-file-pdf-box'
      case 'doc':
      case 'docx':
      case 'odt':
        return 'mdi-text-box'
      default:
        return 'mdi-paperclip'
    }
  }

  /**
   * update the internal model at a given key
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires AttachmentListItem#input
   */
  update (key: string, value: string) {
    const newObj: Attachment = Attachment.createFromObject(this.value)
    newObj.setPath(key, value)

    /**
     * input event
     * @event AttachmentListItem#input
     * @type Attachment
     */
    this.$emit('input', newObj)
  }
}
</script>

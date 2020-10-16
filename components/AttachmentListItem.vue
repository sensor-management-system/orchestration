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
        target="_blank"
      >
        <v-icon>
          mdi-open-in-new
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

import { Attachment } from '@/models/Attachment'

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
  readonly value!: Attachment

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

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

    switch (key) {
      case 'url':
        newObj.url = value
        break
      case 'label':
        newObj.label = value
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event AttachmentListItem#input
     * @type Attachment
     */
    this.$emit('input', newObj)
  }
}
</script>

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
  <v-card class="mb-2">
    <v-list-item>
      <v-list-item-avatar>
        <v-icon large>
          {{ filetypeIcon }}
        </v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-subtitle>
          {{ filename }}, uploaded at {{ uploadedDateTime }}
        </v-list-item-subtitle>
        <v-list-item-title>
          <v-text-field
            v-model="valueCopy.label"
          />
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action-text>
        <v-row>
          <v-col align-self="end" class="text-right">
            <v-btn
              icon
              color="primary"
              :href="valueCopy.url"
              target="_blank"
            >
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </v-btn>
            <v-btn
              text
              small
              :to="'/devices/' + deviceId + '/attachments'"
            >
              Cancel
            </v-btn>
            <v-btn
              color="green"
              small
              @click.prevent.stop="save"
            >
              Apply
            </v-btn>
          </v-col>
        </v-row>
      </v-list-item-action-text>
    </v-list-item>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component
// @ts-ignore
export default class AttachmentEditPage extends Vue {
  private valueCopy: Attachment = new Attachment()

  /**
   * an Attachment
   */
  @Prop({
    required: true,
    type: Attachment
  })
  // @ts-ignore
  readonly value!: Attachment

  created () {
    this.valueCopy = Attachment.createFromObject(this.value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  /**
   * returns the timestamp of the upload date
   *
   * @TODO this must be implemented when the file API is ready
   * @return {string} a readable timestamp
   */
  get uploadedDateTime (): string {
    return '2020-06-17 16:35 (TODO)'
  }

  /**
   * returns a filename from a full filepath
   *
   * @return {string} the filename
   */
  get filename (): string {
    const UNKNOWN_FILENAME = 'unknown filename'

    if (this.valueCopy.url === '') {
      return UNKNOWN_FILENAME
    }
    const paths = this.valueCopy.url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  save () {
    this.$emit('showsave', true)
    this.$api.deviceAttachments.update(this.deviceId, this.valueCopy).then((savedAttachment: Attachment) => {
      this.$emit('showsave', false)
      this.$emit('input', savedAttachment)
      this.$router.push('/devices/' + this.deviceId + '/attachments')
    }).catch(() => {
      this.$emit('showsave', false)
      this.$store.commit('snackbar/setError', 'Failed to save measured quantity')
    })
  }
}
</script>

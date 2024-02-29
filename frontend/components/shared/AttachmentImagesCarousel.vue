<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-carousel
          v-model="visibleImageIndex"
          :title="visibleImage?.attachment?.description ?? ''"
          height="320"
          hide-delimiters
          show-arrows-on-hover
          :show-arrows="value.length > 1"
        >
          <v-carousel-item
            v-for="(image, i) in value"
            :key="i"
            contain
            :src="getUrlForAttachment(image.attachment)"
          />
        </v-carousel>
      </v-col>
      <v-col
        v-if="visibleImage?.attachment?.label"
        class="text-center mt-0 pt-0"
      >
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-label
              v-bind="attrs"
              v-on="visibleImage?.attachment?.description ? on : null"
            >
              {{ visibleImage.attachment?.label }}
            </v-label>
          </template>
          {{ visibleImage.attachment.description }}
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Prop, Component } from 'nuxt-property-decorator'

import { Image, IAttachmentWithUrl } from '@/models/Image'
import { Attachment } from '@/models/Attachment'

@Component
export default class AttachmentImagesCarousel extends Vue {
  private urlsForAttachments: IAttachmentWithUrl[] = []

  private visibleImageIndex: number = 0

  @Prop({
    default: [],
    required: false,
    type: Array
  })
  private value!: Image[]

  @Prop({
    required: true,
    type: Function
  })
  private downloadAttachment!: (attachmentUrl: string) => Promise<Blob>

  async created () {
    await this.setUrlsForAttachments()
  }

  async setUrlsForAttachments () {
    for (const image of this.value) {
      if (image.attachment?.url === null) {
        continue
      }
      const attachment = image.attachment!

      try {
        const url: string | null = attachment.isUpload
          ? await this.downloadAttachment(attachment!.url).then(blob => window.URL.createObjectURL(blob))
          : attachment.url
        if (url) {
          this.urlsForAttachments.push({ attachment, url })
        }
      } catch (_) {
        this.$store.commit('snackbar/setError', 'Downloading attachment failed')
        break
      }
    }
  }

  get visibleImage (): Image | null {
    return this.value[this.visibleImageIndex] ?? null
  }

  getUrlForAttachment (attachment: Attachment): string {
    if (!attachment.id) {
      return ''
    }
    return (
      this.urlsForAttachments.find(
        entry => entry.attachment.id === attachment.id
      )?.url ?? ''
    )
  }
}
</script>

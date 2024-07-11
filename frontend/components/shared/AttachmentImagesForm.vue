<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row align="center">
      <v-col cols="12" md="6">
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="attachmentToAdd"
              :label="
                attachmentsToAddExist
                  ? 'Add an image to preview'
                  : 'No images to add'
              "
              :disabled="!attachmentsToAddExist"
              :items="attachmentsToAddAsImage"
              item-text="label"
              item-value="id"
              @input="addPreviewImageByAttachmentId"
            />
          </v-col>

          <v-col v-if="images && images.length > 0">
            <v-label>Preview images</v-label>
            <v-list max-height="250" class="overflow-y-auto">
              <v-list-item-group :value="visibleImageIndex">
                <v-hover
                  v-for="(image, i) in images"
                  v-slot="{ hover }"
                  :key="i"
                >
                  <v-list-item @click="setVisibleImageIndex(i)">
                    <v-list-item-icon>
                      {{ i + 1 }}
                    </v-list-item-icon>
                    <v-row align="center">
                      <v-col>
                        {{ image.attachment.label }}
                      </v-col>
                      <v-col class="text-right">
                        <span v-if="hover">
                          <v-btn
                            fab
                            x-small
                            light
                            title="Move up"
                            :disabled="i === 0"
                            @click.stop="moveImageAtIndexToLeft(i)"
                          >
                            <v-icon> mdi-chevron-up </v-icon>
                          </v-btn>

                          <v-btn
                            fab
                            x-small
                            light
                            title="Move down"
                            :disabled="i === images.length - 1"
                            @click.stop="moveImageAtIndexToRight(i)"
                          >
                            <v-icon> mdi-chevron-down </v-icon>
                          </v-btn>

                          <v-btn
                            fab
                            x-small
                            light
                            title="Remove from preview"
                            @click="removeImageAtIndex(i)"
                          >
                            <v-icon> mdi-delete </v-icon>
                          </v-btn>
                        </span>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-hover>
              </v-list-item-group>
            </v-list>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12" md="5" lg="4">
        <v-hover v-if="images && images.length > 0" cols="6">
          <v-carousel
            v-model="visibleImageIndex"
            height="200"
            hide-delimiter-background
            :show-arrows="false"
            @change="setVisibleImageIndex"
          >
            <v-carousel-item
              v-for="(image, i) in images"
              :key="i"
              contain
              :src="getUrlForAttachment(image.attachment)"
              @error="setAttachmentError(image.attachment)"
            >
              <ImageNotAvailable v-if="hasAttachmentError(image.attachment)" />
            </v-carousel-item>
          </v-carousel>
        </v-hover>

        <v-label v-else>
          Select images from attachments to preview them.
        </v-label>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import { Image, IAttachmentWithUrl } from '@/models/Image'
import { Attachment, IAttachment } from '@/models/Attachment'
import ImageNotAvailable from '@/components/shared/ImageNotAvailable.vue'

@Component({
  components: { ImageNotAvailable }
})
export default class AttachmentImagesForm extends Vue {
  @Prop({
    default: [],
    required: false,
    type: Array
  })
  private value!: Image[]

  @Prop({
    default: [],
    required: false,
    type: Array
  })
  private attachments!: Attachment[]

  @Prop({
    default: () => ['png', 'jpg', 'jpeg', 'svg', 'gif', 'webp'],
    required: false,
    type: Array
  })
  private validImageExtensions!: string[]

  @Prop({
    required: true,
    type: Function
  })
  private downloadAttachment!: (attachmentUrl: string) => Promise<Blob>

  @Prop({
    required: true,
    type: Function
  })
  private proxyUrl!: (attachmentUrl: string) => Promise<string>

  private urlsForAttachments: IAttachmentWithUrl[] = []
  private visibleImageIndex = 0
  private attachmentToAdd = null
  private fab = false
  private attachmentErrors: {[idx: string]: boolean} = {}

  @Watch('value', { immediate: true, deep: true })
  async setUrlsForAttachments () {
    for (const image of this.value) {
      if (image.attachment !== null && !this.urlsForAttachments.map(entry => entry.attachment.id).includes(image.attachment.id)) {
        await this.addUrlForAttachment(image.attachment)
      }
    }
  }

  // currently we are filtering images by relying on the extension
  get renderableAttachments (): Attachment[] {
    return this.attachments.filter(attachment =>
      this.validImageExtensions.some(suffix =>
        attachment.url.toLowerCase().endsWith(`.${suffix.toLowerCase()}`)
      )
    )
  }

  get attachmentsToAddAsImage (): Attachment[] {
    return this.renderableAttachments.filter(
      a => !this.images.map(i => i.attachment?.id).includes(a.id)
    )
  }

  async addUrlForAttachment (attachment: IAttachment) {
    if (!attachment?.url) {
      return
    }

    const urlAlreadyIncluded = this.urlsForAttachments
      .map(entry => entry.attachment.id)
      .includes(attachment.id)
    if (urlAlreadyIncluded) {
      return
    }

    try {
      const url: string | null = attachment.isUpload
        ? await this.downloadAttachment(attachment!.url).then(blob => window.URL.createObjectURL(blob))
        : await this.proxyUrl(attachment.url)
      if (url) {
        this.urlsForAttachments.push({ attachment, url })
      }
    } catch (_) {
      this.$store.commit('snackbar/setError', 'Downloading attachment failed')
    }
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

  removeImageAtIndex (index: number) {
    this.images.splice(index, 1)
    this.attachmentToAdd = null
    this.orderImages()
  }

  moveImageAtIndexToRight (index: number) {
    const imageToSwap = this.images[index]
    Vue.set(this.images, index, this.images[index + 1])
    Vue.set(this.images, index + 1, imageToSwap)

    this.visibleImageIndex = index + 1
    this.orderImages()
  }

  moveImageAtIndexToLeft (index: number) {
    const imageToSwap = this.images[index]
    Vue.set(this.images, index, this.images[index - 1])
    Vue.set(this.images, index - 1, imageToSwap)

    this.visibleImageIndex = index - 1
    this.orderImages()
  }

  addPreviewImageByAttachmentId (id: string) {
    const attachmentToAdd: Attachment | undefined =
      this.attachmentsToAddAsImage.find(a => a.id === id)
    if (!attachmentToAdd) {
      return
    }

    this.images.push(this.createImageByAttachment(attachmentToAdd))
    this.visibleImageIndex = this.images.length - 1

    this.addUrlForAttachment(attachmentToAdd)
    this.orderImages()
  }

  createImageByAttachment (attachment: Attachment) {
    const newImage: Image = new Image()
    newImage.attachment = attachment
    return newImage
  }

  get images (): Image[] {
    return this.value
  }

  set images (value: Image[]) {
    this.$emit('input', value)
  }

  setAttachmentError (attachment: Attachment) {
    if (!attachment.id) { return }
    Vue.set(this.attachmentErrors, attachment.id, true)
  }

  hasAttachmentError (attachment: Attachment): boolean {
    if (!attachment.id) { return true }
    return this.attachmentErrors[attachment.id]
  }

  setVisibleImageIndex (value: number) {
    this.visibleImageIndex = value
  }

  get attachmentsToAddExist (): boolean {
    return this.attachmentsToAddAsImage.length > 0
  }

  orderImages () {
    const ordered = this.images
    for (const i in ordered) {
      ordered[i].orderIndex = parseInt(i) + 1
    }
    this.images = ordered
  }
}
</script>

<style scoped>
.word-break-text {
  word-break: break-word;
}
</style>

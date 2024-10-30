<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-hover v-slot="{ hover }">
            <div style="position: relative;">
              <v-carousel
                v-model="visibleImageIndex"
                :title="visibleImage?.attachment?.description ?? ''"
                height="320"
                :hide-delimiters="value.length <= 1 || !hover"
                show-arrows-on-hover
                hide-delimiter-background
                :show-arrows="value.length > 1"
              >
                <v-carousel-item
                  v-for="(image, i) in value"
                  :key="i"
                  contain
                  :src="getUrlForAttachment(image.attachment)"
                  @error="setAttachmentError(image.attachment)"
                >
                  <ImageNotAvailable v-if="hasAttachmentError(image.attachment)" />
                </v-carousel-item>
              </v-carousel>

              <v-fade-transition>
                <v-btn
                  v-if="hover"
                  fab
                  small
                  :elevation="0"
                  class="fullscreenButton ma-5"
                  @click="fullscreenImageUrl = getUrlForAttachment(visibleImage?.attachment)"
                >
                  <v-icon>mdi-fullscreen</v-icon>
                </v-btn>
              </v-fade-transition>
            </div>
          </v-hover>
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

    <ImageFullscreenView
      v-model="fullscreenImageUrl"
    />
  </div>
</template>

<script lang="ts">
import { Vue, Prop, Component, Watch } from 'nuxt-property-decorator'

import { Image, IAttachmentWithUrl } from '@/models/Image'
import { Attachment } from '@/models/Attachment'
import ImageNotAvailable from '@/components/shared/ImageNotAvailable.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'
import ImageFullscreenView from '@/components/shared/ImageFullscreenView.vue'

@Component({
  components: {
    ImageFullscreenView,
    ExpandableText,
    ImageNotAvailable
  }
})
export default class AttachmentImagesCarousel extends Vue {
  private urlsForAttachments: IAttachmentWithUrl[] = []
  private fullscreenImageUrl: string|null = null
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

  @Prop({
    required: true,
    type: Function
  })
  private proxyUrl!: (attachmentUrl: string) => Promise<string>

  private attachmentErrors: { [idx: string]: boolean } = {}

  setAttachmentError (attachment: Attachment) {
    if (!attachment.id) {
      return
    }
    Vue.set(this.attachmentErrors, attachment.id, true)
  }

  hasAttachmentError (attachment: Attachment): boolean {
    if (!attachment.id) {
      return true
    }
    return this.attachmentErrors[attachment.id]
  }

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
          : await this.proxyUrl(attachment.url)
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

  @Watch('value', { deep: true })
  onImagesChange () {
    this.urlsForAttachments = []
    this.setUrlsForAttachments()
  }
}
</script>

<style>
.v-carousel__controls__item.v-btn.v-btn--icon {
  background-color: #E3F2FD;
  opacity: .7;
  height: 20px;
  width: 20px;
  border-radius: 0;
  margin: 0 3px;
  transition: all .2s;
}

.v-carousel__controls__item.v-btn.v-btn--icon.v-btn--active {
  background-color: #1976D2;
  transition: all .2s;
  opacity: 1;
}

.v-carousel__controls__item.v-btn.v-btn--icon:not(.v-btn--active):hover {
  background-color: #D3E2ED;
  transition: all .2s;
  opacity: 1;
}

.v-carousel__controls__item .v-btn__content .v-icon {
  display: none;
}

.fullscreenButton {
  position: absolute;
  top: 0;
  right: 0;
}
</style>

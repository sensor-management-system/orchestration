<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-card-text
    v-if="value.length > 0"
    class="grey lighten-5 text--primary pt-2"
  >
    <label>Attachments</label>
    <div v-for="(attachment, index) in value" :key="index">
      <span class="text-caption">
        <template v-if="isPublic || !attachment.isUpload">
          <a :href="attachment.url" target="_blank">
            {{ attachment.label }}&nbsp;<v-icon small>mdi-open-in-new</v-icon>
          </a>
        </template>
        <template v-else>
          <span>
            {{ attachment.label }}&nbsp;<v-icon small @click="openAttachment(attachment)">mdi-link-lock</v-icon>
          </span>
        </template>
      </span>
    </div>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'

@Component
export default class AttachmentsBlock extends Vue {
  @Prop({
    default: () => [],
    type: Array

  })
  readonly value!: Attachment[]

  @Prop({
    type: Boolean,
    default: false
  })
  readonly isPublic!: Boolean

  openAttachment (attachment: Attachment) {
    this.$emit('open-attachment', attachment)
  }
}
</script>

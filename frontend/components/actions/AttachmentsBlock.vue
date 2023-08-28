<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
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

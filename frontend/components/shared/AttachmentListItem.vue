<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Rubankumar Moorthy (FZJ, r.moorthy@fz-juelich.de)
- Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
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
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-card-text
        class="py-2 px-3"
      >
        <div class="d-flex align-center">
          <span class="text-caption">
            <ExpandableText v-model="attachment.url" :shorten-at="60" more-icon="mdi-unfold-more-vertical" less-icon="mdi-unfold-less-vertical" />
            <span v-if="attachment.createdAt && attachment.isUpload">
              uploaded at {{ attachment.createdAt | toUtcDateTimeString }}
            </span>
          </span>
          <v-spacer />
          <DotMenu>
            <template #actions>
              <slot name="dot-menu-items" />
            </template>
          </DotMenu>
        </div>
        <v-row
          no-gutters
        >
          <v-col cols="8" class="text-subtitle-1">
            <v-icon>
              {{ filetypeIcon(attachment) }}
            </v-icon>
            <span class="text-caption">
              <template v-if="isPublic || !attachment.isUpload">
                <a :href="attachment.url" target="_blank">
                  {{ attachment.label }}&nbsp;<v-icon small>mdi-open-in-new</v-icon>
                </a>
              </template>
              <template v-else>
                <span>
                  {{ attachment.label }}&nbsp;<v-icon small @click="openAttachment">mdi-link-lock</v-icon>
                </span>
              </template>
            </span>
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <slot name="edit-action" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import DotMenu from '@/components/DotMenu.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    DotMenu,
    BaseExpandableListItem,
    ExpandableText
  }
})
export default class AttachmentListItem extends mixins(AttachmentsMixin) {
  @Prop({
    required: true,
    type: Object
  })
  private attachment!: Attachment

  @Prop({
    required: false,
    type: Boolean,
    default: false
  })
  private isPublic!: boolean

  openAttachment () {
    this.$emit('open-attachment', this.attachment)
  }
}
</script>

<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Rubankumar Moorthy <r.moorthy@fz-juelich.de>
- Forschungszentrum Jülich GmbH (FZJ, https://fz-juelich.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <slot name="edit-action" />
    </template>
    <template
      v-if="attachment.description"
      #expandable
    >
      <v-card-text
        v-if="attachment.description"
        class="py-2"
      >
        {{ attachment.description }}
      </v-card-text>
    </template>
    <template #default>
      <div class="d-flex align-center">
        <span class="text-caption">
          <span @click.stop>
            <ExpandableText v-model="attachment.url" :shorten-at="60" />
          </span>
          <span v-if="attachment.createdAt && attachment.isUpload">
            uploaded at {{ attachment.createdAt | toUtcDateTimeString }}
          </span>
        </span>
        <v-spacer />
      </div>
      <v-row
        no-gutters
      >
        <v-col cols="12" class="text-subtitle-1">
          <v-icon>
            {{ filetypeIcon(attachment) }}
          </v-icon>
          <span class="text-caption">
            <template v-if="isPublic || !attachment.isUpload">
              <a :href="attachment.url" target="_blank" @click.stop>
                {{ attachment.label }}&nbsp;<v-icon small>mdi-open-in-new</v-icon>
              </a>
            </template>
            <template v-else>
              <span>
                {{ attachment.label }}&nbsp;<v-icon small @click.stop="openAttachment">mdi-link-lock</v-icon>
              </span>
            </template>
          </span>
        </v-col>
      </v-row>
    </template>
  </base-expandable-list-item>
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

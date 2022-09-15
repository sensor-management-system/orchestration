<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
            {{ attachment.url | shortenMiddle }}
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
              <a :href="attachment.url" target="_blank">
                {{ attachment.label }}&nbsp;<v-icon small>mdi-open-in-new</v-icon>
              </a>
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

@Component({
  components: {
    DotMenu,
    BaseExpandableListItem
  }
})
export default class DevicesAttachmentListItem extends mixins(AttachmentsMixin) {
  @Prop({
    required: true,
    type: Object
  })
  private attachment!: Attachment

  @Prop({
    required: true
  })
  private deviceId!: string
}
</script>

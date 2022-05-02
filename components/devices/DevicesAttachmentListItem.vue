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
      <v-card-text>
        <v-row>
          <v-avatar class="mt-0 align-self-center">
            <v-icon large>
              {{ filetypeIcon(attachment) }}
            </v-icon>
          </v-avatar>
          <v-col>
            <v-row
              no-gutters
            >
              <v-col>
                <v-card-subtitle>
                  {{ filename(attachment) }}
                </v-card-subtitle>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <DotMenu>
                  <template #actions>
                    <slot name="dot-menu-items" />
                  </template>
                </DotMenu>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                <a v-if="attachment.label" :href="attachment.url" target="_blank">
                  <v-icon color="primary">mdi-open-in-new</v-icon>{{ attachment.label }}
                </a>
                <a v-else :href="attachment.url" target="_blank">
                  <v-icon color="primary">mdi-open-in-new</v-icon>
                </a>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <v-btn
                  v-if="$auth.loggedIn"
                  color="primary"
                  text
                  small
                  nuxt
                  :to="'/devices/' + deviceId + '/attachments/' + attachment.id + '/edit'"
                >
                  Edit
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { mixins, Prop } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'
import DotMenu from '@/components/DotMenu.vue'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
@Component({
  components: { DotMenu }
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

<style scoped>

</style>

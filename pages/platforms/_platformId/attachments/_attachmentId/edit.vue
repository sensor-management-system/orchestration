<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
          {{ filetypeIcon(valueCopy) }}
        </v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-subtitle>
          {{ filename(valueCopy) }}, uploaded at {{ uploadedDateTime(valueCopy) }}
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
              ref="cancelButton"
              text
              small
              :to="'/platforms/' + platformId + '/attachments'"
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
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { mapActions, mapState } from 'vuex'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  computed:mapState('platforms',['platformAttachment']),
  methods:mapActions('platforms',['loadPlatformAttachment','loadPlatformAttachments','updatePlatformAttachment'])
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(AttachmentsMixin) {
  private valueCopy: Attachment = new Attachment()

  async created () {
    await this.loadPlatformAttachment(this.attachmentId)
    this.valueCopy = Attachment.createFromObject(this.platformAttachment)
  }

  get platformId (): string {
    return this.$route.params.platformId
  }
  get attachmentId (): string {
    return this.$route.params.attachmentId
  }

  save () {
    try {
      this.updatePlatformAttachment({
        platformId: this.platformId,
        attachment: this.valueCopy
      })
      this.loadPlatformAttachments(this.platformId)
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    }

  }
}
</script>

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
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/attachments'"
        @save="save"
      />
    </v-card-actions>
    <v-card>
      <v-container>
        <v-row no-gutters>
          <v-avatar class="mt-0 align-self-center">
            <v-icon large>
              {{ filetypeIcon(valueCopy) }}
            </v-icon>
          </v-avatar>
          <v-col>
            <v-row
              no-gutters
            >
              <v-col>
                <v-card-subtitle>
                  {{ filename(valueCopy) }}, uploaded at {{ uploadedDateTime(valueCopy) }}
                </v-card-subtitle>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                <v-text-field
                  v-model="valueCopy.label"
                  label="Label"
                />
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
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
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Attachment } from '@/models/Attachment'
/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  components: { ProgressIndicator, SaveAndCancelButtons },
  middleware: ['auth'],
  computed: mapState('platforms', ['platformAttachment']),
  methods: mapActions('platforms', ['loadPlatformAttachment', 'loadPlatformAttachments', 'updatePlatformAttachment'])
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(AttachmentsMixin) {
  private isSaving = false
  private isLoading = false
  private valueCopy: Attachment = new Attachment()

  async created () {
    try {
      this.isLoading = true
      await this.loadPlatformAttachment(this.attachmentId)
      this.valueCopy = Attachment.createFromObject(this.platformAttachment)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.isLoading = false
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get attachmentId (): string {
    return this.$route.params.attachmentId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    try {
      this.isSaving = true
      await this.updatePlatformAttachment({
        platformId: this.platformId,
        attachment: this.valueCopy
      })
      this.loadPlatformAttachments(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Attachment updated')
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachment')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

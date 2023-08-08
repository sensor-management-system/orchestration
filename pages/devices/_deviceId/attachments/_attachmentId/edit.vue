<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
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
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/attachments'"
        @save="save"
      />
    </v-card-actions>
    <v-card>
      <v-card-text
        class="py-2 px-3"
      >
        <div class="d-flex align-center">
          <span class="text-caption">
            {{ filename(valueCopy) }}<span v-if="valueCopy.createdAt && valueCopy.isUpload">,
              uploaded at {{ valueCopy.createdAt | toUtcDateTimeString }}
            </span>
          </span>
        </div>
        <v-row
          no-gutters
        >
          <v-col cols="8" class="text-subtitle-1">
            <v-icon>
              {{ filetypeIcon(valueCopy) }}
            </v-icon>
            <v-form ref="attachmentsEditForm" class="pb-2" @submit.prevent>
              <v-text-field
                v-model="valueCopy.url"
                :label="valueCopy.isUpload ? 'File': 'URL'"
                required
                class="required"
                type="url"
                placeholder="https://"
                :rules="valueCopy.isUpload ? [] : [rules.required, rules.validUrl]"
                :disabled="valueCopy.isUpload"
              />
              <v-text-field
                v-model="valueCopy.label"
                label="Label"
                required
                class="required"
                :rules="[rules.required]"
              />
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  DevicesState,
  LoadDeviceAttachmentAction,
  LoadDeviceAttachmentsAction,
  UpdateDeviceAttachmentAction
} from '@/store/devices'

import { Attachment } from '@/models/Attachment'

import { Rules } from '@/mixins/Rules'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  components: {
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceAttachment']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceAttachment', 'loadDeviceAttachments', 'updateDeviceAttachment']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(Rules, AttachmentsMixin, CheckEditAccess) {
  private valueCopy: Attachment = new Attachment()

  // vuex definition for typescript check
  deviceAttachment!: DevicesState['deviceAttachment']
  loadDeviceAttachment!: LoadDeviceAttachmentAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  updateDeviceAttachment!: UpdateDeviceAttachmentAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadDeviceAttachment(this.attachmentId)
      if (this.deviceAttachment) {
        this.valueCopy = Attachment.createFromObject(this.deviceAttachment)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get attachmentId (): string {
    return this.$route.params.attachmentId
  }

  async save () {
    if (!(this.$refs.attachmentsEditForm as Vue & { validate: () => boolean }).validate()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      await this.updateDeviceAttachment({
        deviceId: this.deviceId,
        attachment: this.valueCopy
      })
      this.loadDeviceAttachments(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Attachment updated')
      this.$router.push('/devices/' + this.deviceId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

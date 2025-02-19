<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
    <AttachmentBasicDataForm ref="attachmentsEditForm" v-model="valueCopy" />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  DevicesState,
  LoadDeviceAction,
  LoadDeviceAttachmentAction,
  LoadDeviceAttachmentsAction,
  UpdateDeviceAttachmentAction
} from '@/store/devices'

import { Attachment } from '@/models/Attachment'

import { Rules } from '@/mixins/Rules'

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import AttachmentBasicDataForm from '@/components/shared/AttachmentBasicDataForm.vue'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  components: {
    AttachmentBasicDataForm,
    AutocompleteTextInput,
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceAttachment']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceAttachment', 'loadDeviceAttachments', 'updateDeviceAttachment', 'loadDevice']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(Rules, AttachmentsMixin, CheckEditAccess) {
  private valueCopy: Attachment = new Attachment()

  // vuex definition for typescript check
  deviceAttachment!: DevicesState['deviceAttachment']
  loadDevice!: LoadDeviceAction
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
    if (!(this.$refs.attachmentsEditForm as AttachmentBasicDataForm & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      await this.updateDeviceAttachment({
        deviceId: this.deviceId,
        attachment: this.valueCopy
      })
      // update attachment previews
      this.loadDevice({
        deviceId: this.deviceId,
        includeImages: true,
        includeCreatedBy: true,
        includeUpdatedBy: true
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

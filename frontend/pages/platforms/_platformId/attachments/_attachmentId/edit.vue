<!--
SPDX-FileCopyrightText: 2020 - 2023
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/attachments'"
        @save="save"
      />
    </v-card-actions>
    <AttachmentBasicDataForm ref="attachmentsEditForm" v-model="valueCopy" />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  PlatformsState,
  LoadPlatformAttachmentAction,
  LoadPlatformAttachmentsAction,
  UpdatePlatformAttachmentAction,
  LoadPlatformAction
} from '@/store/platforms'

import { Attachment } from '@/models/Attachment'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import { Rules } from '@/mixins/Rules'
import AttachmentBasicDataForm from '@/components/shared/AttachmentBasicDataForm.vue'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  components: { AttachmentBasicDataForm, AutocompleteTextInput, SaveAndCancelButtons },
  middleware: ['auth'],
  computed: {
    ...mapState('platforms', ['platformAttachment']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatformAttachment', 'loadPlatformAttachments', 'updatePlatformAttachment', 'loadPlatform']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(Rules, AttachmentsMixin, CheckEditAccess) {
  private valueCopy: Attachment = new Attachment()

  // vuex definition for typescript check
  platformAttachment!: PlatformsState['platformAttachment']
  loadPlatform!: LoadPlatformAction
  loadPlatformAttachment!: LoadPlatformAttachmentAction
  updatePlatformAttachment!: UpdatePlatformAttachmentAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
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
    return '/platforms/' + this.platformId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadPlatformAttachment(this.attachmentId)
      if (this.platformAttachment) {
        this.valueCopy = Attachment.createFromObject(this.platformAttachment)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
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
      await this.updatePlatformAttachment({
        platformId: this.platformId,
        attachment: this.valueCopy
      })
      // update attachment previews
      this.loadPlatform({
        platformId: this.platformId,
        includeImages: true,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.loadPlatformAttachments(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Attachment updated')
      this.$router.push('/platforms/' + this.platformId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachment')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

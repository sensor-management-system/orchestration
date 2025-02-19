<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/sites/' + siteId + '/attachments'"
        @save="save"
      />
    </v-card-actions>
    <AttachmentBasicDataForm ref="attachmentsEditForm" v-model="valueCopy" />
  </div>
</template>

<script lang="ts">
import { Component, mixins, Watch } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  SitesState,
  LoadSiteAttachmentsAction,
  LoadSiteAttachmentAction,
  UpdateSiteAttachmentAction,
  LoadSiteAction
} from '@/store/sites'

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
    ...mapState('sites', ['siteAttachment']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('sites', ['loadSiteAttachment', 'loadSiteAttachments', 'updateSiteAttachment', 'loadSite']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(Rules, AttachmentsMixin, CheckEditAccess) {
  private valueCopy: Attachment = new Attachment()

  // vuex definition for typescript check
  siteAttachment!: SitesState['siteAttachment']
  loadSite!: LoadSiteAction
  loadSiteAttachment!: LoadSiteAttachmentAction
  loadSiteAttachments!: LoadSiteAttachmentsAction
  updateSiteAttachment!: UpdateSiteAttachmentAction
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
    return '/sites/' + this.siteId + '/attachments'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this site.'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadSiteAttachment(this.attachmentId)
      if (this.siteAttachment) {
        this.valueCopy = Attachment.createFromObject(this.siteAttachment)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId (): string {
    return this.$route.params.siteId
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
      await this.updateSiteAttachment({
        siteId: this.siteId,
        attachment: this.valueCopy
      })
      // update attachment previews
      this.loadSite({
        siteId: this.siteId,
        includeImages: true,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })
      this.loadSiteAttachments(this.siteId)
      this.$store.commit('snackbar/setSuccess', 'Attachment updated')
      this.$router.push('/sites/' + this.siteId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/sites/' + this.siteId + '/attachments', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this site.')
      })
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

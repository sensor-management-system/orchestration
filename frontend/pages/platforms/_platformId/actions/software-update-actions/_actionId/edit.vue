<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-select
      value="Software Update"
      :items="['Software Update']"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="action"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  PlatformsState,
  LoadPlatformSoftwareUpdateActionAction,
  LoadAllPlatformActionsAction,
  LoadPlatformAttachmentsAction,
  UpdatePlatformSoftwareUpdateActionAction
} from '@/store/platforms'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'

@Component({
  components: {
    SaveAndCancelButtons,
    SoftwareUpdateActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: {
    ...mapState('platforms', ['platformSoftwareUpdateAction', 'platformAttachments']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatformSoftwareUpdateAction', 'loadAllPlatformActions', 'loadPlatformAttachments', 'updatePlatformSoftwareUpdateAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformSoftwareUpdateActionEditPage extends mixins(CheckEditAccess) {
  private action: SoftwareUpdateAction = new SoftwareUpdateAction()

  // vuex definition for typescript check
  platformSoftwareUpdateAction!: PlatformsState['platformSoftwareUpdateAction']
  platformAttachments!: PlatformsState['platformAttachments']
  loadPlatformSoftwareUpdateAction!: LoadPlatformSoftwareUpdateActionAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  updatePlatformSoftwareUpdateAction!: UpdatePlatformSoftwareUpdateActionAction
  loadAllPlatformActions!: LoadAllPlatformActionsAction
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
    return '/platforms/' + this.platformId + '/actions'
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

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadPlatformSoftwareUpdateAction(this.actionId),
        this.loadPlatformAttachments(this.platformId)
      ])
      if (this.platformSoftwareUpdateAction) {
        this.action = SoftwareUpdateAction.createFromObject(this.platformSoftwareUpdateAction)
      }
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  async save () {
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.setLoading(true)
      await this.updatePlatformSoftwareUpdateAction({
        platformId: this.platformId,
        softwareUpdateAction: this.action
      })
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', 'Software Update Action updated')
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

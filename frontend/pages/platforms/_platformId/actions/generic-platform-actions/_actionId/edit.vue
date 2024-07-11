<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="action.actionTypeName"
      :items="[action.actionTypeName]"
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
    <GenericActionForm
      ref="genericPlatformActionForm"
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
  LoadPlatformGenericActionAction,
  LoadAllPlatformActionsAction,
  LoadPlatformAttachmentsAction,
  UpdatePlatformGenericActionAction
} from '@/store/platforms'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    GenericActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: {
    ...mapState('platforms', ['platformGenericAction', 'platformAttachments']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatformGenericAction', 'loadAllPlatformActions', 'loadPlatformAttachments', 'updatePlatformGenericAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class EditPlatformAction extends mixins(CheckEditAccess) {
  private action: GenericAction = new GenericAction()

  // vuex definition for typescript check
  platforms!: PlatformsState['platforms']
  platformGenericAction!: PlatformsState['platformGenericAction']
  loadAllPlatformActions!: LoadAllPlatformActionsAction
  loadPlatformGenericAction!: LoadPlatformGenericActionAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  updatePlatformGenericAction!: UpdatePlatformGenericActionAction
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
        this.loadPlatformGenericAction(this.actionId),
        this.loadPlatformAttachments(this.platformId)
      ])
      if (this.platformGenericAction) {
        this.action = GenericAction.createFromObject(this.platformGenericAction)
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
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.setLoading(true)
      await this.updatePlatformGenericAction({ platformId: this.platformId, genericPlatformAction: this.action })
      this.loadAllPlatformActions(this.platformId)
      this.$store.commit('snackbar/setSuccess', `${this.action.actionTypeName} updated`)
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

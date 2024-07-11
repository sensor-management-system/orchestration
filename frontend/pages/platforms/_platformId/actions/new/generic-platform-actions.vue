<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <GenericActionForm
      ref="genericPlatformActionForm"
      v-model="genericPlatformAction"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
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
  AddPlatformGenericActionAction,
  LoadAllPlatformActionsAction
} from '@/store/platforms'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  middleware: ['auth'],
  components: { SaveAndCancelButtons, GenericActionForm },
  computed: mapState('platforms', ['platformAttachments', 'chosenKindOfPlatformAction']),
  methods: {
    ...mapActions('platforms', ['addPlatformGenericAction', 'loadAllPlatformActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewGenericPlatformAction extends mixins(CheckEditAccess) {
  private genericPlatformAction: GenericAction = new GenericAction()

  // vuex definition for typescript check
  platformAttachements!: PlatformsState['platformAttachments']
  chosenKindOfPlatformAction!: PlatformsState['chosenKindOfPlatformAction']
  addPlatformGenericAction!: AddPlatformGenericActionAction
  loadAllPlatformActions!: LoadAllPlatformActionsAction
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

  created () {
    if (this.chosenKindOfPlatformAction === null) {
      this.$router.push('/platforms/' + this.platformId + '/actions')
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  async save () {
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfPlatformAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfPlatformAction?.uri || ''

    try {
      this.setLoading(true)
      await this.addPlatformGenericAction({ platformId: this.platformId, genericPlatformAction: this.genericPlatformAction })
      this.loadAllPlatformActions(this.platformId)
      const successMessage = this.genericPlatformAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
